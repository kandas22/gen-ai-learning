"""
KaviHealthCare Patient Profile Management Streamlit App
Modular app using SQLite for persistence with separated database layer.

Fields:
- first_name (required)
- last_name (required)
- phone (required, digits)
- email (optional, validated if provided)
- address (required)

Features:
- User authentication with login page
- Admin can create users
- Only authorized users can access the app
- Add / Edit / Delete patients
- Search + filter
- Export CSV
- Simple validation and user feedback
"""

from typing import Tuple
import pandas as pd
import streamlit as st
import validators
from io import BytesIO
from datetime import datetime
import os
from whatsapp_sender import send_whatsapp_pdf

# Import ReportLab for PDF generation
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("Warning: reportlab not available. PDF generation will be disabled.")

# Import database operations from separate package
from database import (
    get_connection,
    init_db,
    init_users_table,
    insert_patient,
    update_patient,
    delete_patient,
    fetch_all_patients,
    fetch_patient_by_id,
    authenticate_user,
    create_user,
    fetch_all_users,
    delete_user,
    user_exists,
    init_lab_tests_tables,
    get_all_lab_tests,
    get_lab_tests_by_category,
    order_lab_test,
    update_lab_test_result,
    fetch_patient_lab_tests,
    fetch_all_lab_tests_orders,
    delete_lab_test_order,
    fetch_lab_test_by_id
)

# -----------------------
# Validation helpers
# -----------------------
def validate_phone(phone: str) -> Tuple[bool, str]:
    s = phone.strip()
    # Allow + and digits and spaces/hyphens. But require at least 7 digits (adjustable)
    digits = "".join(ch for ch in s if ch.isdigit())
    if len(digits) < 7 or len(digits) > 15:
        return False, "Phone must contain between 7 and 15 digits."
    # Simple pattern check
    return True, ""

def validate_email(email: str) -> Tuple[bool, str]:
    if email.strip() == "":
        return True, ""  # optional
    if validators.email(email):
        return True, ""
    return False, "Invalid email address."

# -----------------------
# Utility helpers
# -----------------------
def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")

# -----------------------
# Authentication UI
# -----------------------
def login_page():
    """Display login page and handle authentication."""
    st.set_page_config(page_title="KaviHealthCare Login", page_icon="🩺", layout="centered")
    
    st.title("🩺 KaviHealthCare")
    st.subheader("The Medical Innovation Lab of Tomorrow, Built Today.")
    
    st.markdown("---")
    st.markdown("### Login")
    
    with st.form("login_form"):
        username = st.text_input("Username", max_chars=50)
        password = st.text_input("Password", type="password", max_chars=50)
        submit = st.form_submit_button("Login")
        
        if submit:
            if not username or not password:
                st.error("Please enter both username and password.")
            else:
                conn = get_connection()
                init_users_table(conn)
                user = authenticate_user(conn, username, password)
                
                if user:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = user["username"]
                    st.session_state["role"] = user["role"]
                    st.success(f"Welcome, {user['username']}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
    
    st.markdown("---")
    st.info("💡 Use admin credentials to login to the KaviHealthCare system")

def user_management_section(conn):
    """Admin section for managing users."""
    st.sidebar.markdown("---")
    st.sidebar.header("👥 User Management")
    
    if st.sidebar.button("Manage Users"):
        st.session_state["show_user_management"] = True
    
    if st.session_state.get("show_user_management", False):
        st.markdown("---")
        st.subheader("👥 User Management (Admin Only)")
        
        tab1, tab2 = st.tabs(["Create User", "View Users"])
        
        with tab1:
            st.markdown("### Create New User")
            with st.form("create_user_form"):
                new_username = st.text_input("Username", max_chars=50)
                new_password = st.text_input("Password", type="password", max_chars=50)
                confirm_password = st.text_input("Confirm Password", type="password", max_chars=50)
                create_submit = st.form_submit_button("Create User")
                
                if create_submit:
                    errors = []
                    if not new_username.strip():
                        errors.append("Username is required.")
                    elif len(new_username.strip()) < 3:
                        errors.append("Username must be at least 3 characters.")
                    elif user_exists(conn, new_username):
                        errors.append("Username already exists.")
                    
                    if not new_password:
                        errors.append("Password is required.")
                    elif len(new_password) < 3:
                        errors.append("Password must be at least 3 characters.")
                    
                    if new_password != confirm_password:
                        errors.append("Passwords do not match.")
                    
                    if errors:
                        for err in errors:
                            st.error(err)
                    else:
                        user_id = create_user(conn, new_username, new_password, st.session_state["username"])
                        st.success(f"User '{new_username}' created successfully! (ID: {user_id})")
        
        with tab2:
            st.markdown("### Existing Users")
            users_df = fetch_all_users(conn)
            
            if users_df.empty:
                st.info("No users found.")
            else:
                st.dataframe(users_df, use_container_width=True)
                
                # Delete user option (except admin)
                deletable_users = users_df[users_df["username"] != "admin"]
                if not deletable_users.empty:
                    st.markdown("#### Delete User")
                    selected_user_id = st.selectbox(
                        "Select user to delete",
                        options=deletable_users["id"].tolist(),
                        format_func=lambda x: deletable_users[deletable_users["id"] == x]["username"].values[0]
                    )
                    
                    if st.button("🗑️ Delete Selected User", type="secondary"):
                        delete_user(conn, selected_user_id)
                        st.success("User deleted successfully!")
                        st.rerun()


# -----------------------
# PDF Generation Helper
# -----------------------
def generate_lab_report_pdf(patient_data: dict, tests_df: pd.DataFrame) -> bytes:
    """
    Generate a PDF lab report for a patient.
    
    Args:
        patient_data: Dictionary containing patient information
        tests_df: DataFrame containing lab test results
        
    Returns:
        PDF file as bytes
    """
    if not REPORTLAB_AVAILABLE:
        raise ImportError("reportlab library is not installed. Please install it with: pip install reportlab")
    
    # Create PDF buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#7f8c8d'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Header
    elements.append(Paragraph("🩺 KaviHealthCare", title_style))
    elements.append(Paragraph("Laboratory Test Report", title_style))
    elements.append(Paragraph("The Medical Innovation Lab of Tomorrow, Built Today", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2c3e50'), spaceAfter=20))
    
    # Patient Information
    elements.append(Paragraph("Patient Information", heading_style))
    
    patient_info_data = [
        ["Patient ID:", str(patient_data['id'])],
        ["Name:", f"{patient_data['first_name']} {patient_data['last_name']}"],
        ["Phone:", patient_data['phone']],
        ["Email:", patient_data['email'] or 'N/A'],
        ["Address:", patient_data['address']],
        ["Report Generated:", datetime.now().strftime("%B %d, %Y %I:%M %p")]
    ]
    
    patient_table = Table(patient_info_data, colWidths=[2*inch, 4.5*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c3e50')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.white)
    ]))
    
    elements.append(patient_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Test Results
    elements.append(Paragraph("Test Results", heading_style))
    
    # Prepare test data for table
    test_table_data = [['Test Name', 'Test Date', 'Status', 'Result', 'Reference Range', 'Notes']]
    
    for _, test in tests_df.iterrows():
        result_display = f"{test['result_value'] or '-'} {test['result_unit'] or ''}".strip()
        if result_display == '-':
            result_display = 'Pending'
        
        test_table_data.append([
            test['test_name'],
            test['test_date'],
            test['test_status'],
            result_display,
            test['reference_range'] or '-',
            test['notes'][:30] + '...' if test['notes'] and len(test['notes']) > 30 else (test['notes'] or '-')
        ])
    
    # Create test results table
    test_table = Table(test_table_data, colWidths=[1.8*inch, 0.9*inch, 0.8*inch, 1*inch, 1.2*inch, 1*inch])
    
    # Style the test table
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
    ]
    
    # Add color coding for status
    for i, row in enumerate(tests_df.itertuples(), start=1):
        if row.test_status == 'Completed':
            table_style.append(('TEXTCOLOR', (2, i), (2, i), colors.HexColor('#27ae60')))
        elif row.test_status == 'Pending':
            table_style.append(('TEXTCOLOR', (2, i), (2, i), colors.HexColor('#f39c12')))
        elif row.test_status == 'Cancelled':
            table_style.append(('TEXTCOLOR', (2, i), (2, i), colors.HexColor('#e74c3c')))
    
    test_table.setStyle(TableStyle(table_style))
    elements.append(test_table)
    
    # Signature section
    elements.append(Spacer(1, 0.5*inch))
    signature_data = [
        ["_" * 30, "_" * 30],
        ["Technician Signature", "Doctor Signature"],
        ["Date: _______________", "Date: _______________"]
    ]
    
    signature_table = Table(signature_data, colWidths=[3*inch, 3*inch])
    signature_table.setStyle(TableStyle([
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 1), (-1, 1), 8),
    ]))
    
    elements.append(signature_table)
    
    # Footer
    elements.append(Spacer(1, 0.3*inch))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#2c3e50'), spaceBefore=10))
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#7f8c8d'),
        alignment=TA_CENTER,
        spaceAfter=4
    )
    
    elements.append(Paragraph("<b>KaviHealthCare Laboratory</b>", footer_style))
    elements.append(Paragraph(f"This is a computer-generated report. Total tests in report: {len(tests_df)}", footer_style))
    elements.append(Paragraph("For any queries, please contact our lab at lab@kavihealthcare.com", footer_style))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    return buffer.getvalue()


# -----------------------
# Streamlit UI
# -----------------------
def main():
    # Initialize session state
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    # Show login page if not authenticated
    if not st.session_state["authenticated"]:
        login_page()
        return
    
    # Main application (only for authenticated users)
    st.set_page_config(page_title="Patient Profiles", page_icon="🩺", layout="wide")

    conn = get_connection()
    init_db(conn)
    init_users_table(conn)
    init_lab_tests_tables(conn)

    # Header with logout button
    col1, col2 = st.columns([5, 1])
    with col1:
        st.title("🩺 The Medical Innovation Lab of Tomorrow, Built Today.")
        st.write("Create, search, edit, and export patient profiles. Email is optional.")
    with col2:
        st.write("")  # Add some spacing
        st.markdown(f"""
        <div style='text-align: right;'>
            <p style='margin: 0; margin-bottom: 5px; font-weight: bold; font-size: 14px;'>User: {st.session_state['username']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Logout", type="primary", use_container_width=True):
            st.session_state["authenticated"] = False
            st.session_state.pop("username", None)
            st.session_state.pop("role", None)
            st.session_state.pop("show_user_management", None)
            st.rerun()

    # Sidebar - actions and search
    st.sidebar.header("Actions")
    action = st.sidebar.radio("Select action", ["Add patient", "View & manage patients", "Lab Tests", "Import (CSV)"], index=1)
    
    # Show user management for admin
    if st.session_state.get("role") == "admin":
        user_management_section(conn)

    # For search/filter
    st.sidebar.markdown("---")
    st.sidebar.header("Search / Filter")
    q_name = st.sidebar.text_input("Name contains (first or last)")
    q_phone = st.sidebar.text_input("Phone contains")
    q_email = st.sidebar.text_input("Email contains")
    apply_filter = st.sidebar.button("Apply filters")

    # Load data
    df_all = fetch_all_patients(conn)

    # Apply filtering if requested or if any field non-empty
    if apply_filter or any([q_name, q_phone, q_email]):
        df = df_all.copy()
        if q_name:
            mask = df["first_name"].str.contains(q_name, case=False, na=False) | df["last_name"].str.contains(q_name, case=False, na=False)
            df = df[mask]
        if q_phone:
            df = df[df["phone"].str.contains(q_phone, na=False)]
        if q_email:
            df = df[df["email"].fillna("").str.contains(q_email, case=False, na=False)]
    else:
        df = df_all

    # ---------- Add patient ----------
    if action == "Add patient":
        st.subheader("Add new patient")
        with st.form("add_patient_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First name", max_chars=100)
            with col2:
                last_name = st.text_input("Last name", max_chars=100)

            phone = st.text_input("Phone (required)")
            email = st.text_input("Email (optional)")
            address = st.text_area("Address", max_chars=1000, height=120)

            submitted = st.form_submit_button("Add patient")
            if submitted:
                # Validate
                errors = []
                if not first_name.strip():
                    errors.append("First name is required.")
                if not last_name.strip():
                    errors.append("Last name is required.")
                ok_phone, phone_msg = validate_phone(phone)
                if not ok_phone:
                    errors.append(phone_msg)
                ok_email, email_msg = validate_email(email)
                if not ok_email:
                    errors.append(email_msg)
                if not address.strip():
                    errors.append("Address is required.")

                if errors:
                    for e in errors:
                        st.error(e)
                else:
                    pid = insert_patient(conn, first_name, last_name, phone, email or None, address)
                    st.success(f"Patient added (ID: {pid})")
                    # refresh df
                    df_all = fetch_all_patients(conn)
                    df = df_all

    # ---------- View & manage ----------
    elif action == "View & manage patients":
        st.subheader("Patients")

        # Show count and quick export
        col_top = st.columns([1, 1, 1])
        col_top[0].write(f"**Total records:** {len(df_all)}")
        col_top[1].write(f"**Showing:** {len(df)}")
        if not df.empty:
            csv_bytes = df_to_csv_bytes(df)
            col_top[2].download_button("Download visible as CSV", data=csv_bytes, file_name="patients_export.csv", mime="text/csv", key="download_patients_csv")

        st.markdown("---")
        if df.empty:
            st.info("No patient records to show.")
        else:
            # Display table
            # Show limited columns
            display_df = df[["id", "first_name", "last_name", "phone", "email", "address", "created_at"]].copy()
            display_df = display_df.rename(columns={
                "id": "ID",
                "first_name": "First name",
                "last_name": "Last name",
                "phone": "Phone",
                "email": "Email",
                "address": "Address",
                "created_at": "Created at"
            })
            st.dataframe(display_df, use_container_width=True, height=300)

            st.markdown("**Select a patient to edit or delete**")
            selected_id_input = st.text_input(
                "Patient ID", 
                placeholder="Enter patient ID to edit or delete...",
                help="Enter the ID of the patient you want to edit or delete"
            )

            # Fetch selected record
            selected = None
            if selected_id_input:
                try:
                    selected_id = int(selected_id_input)
                    selected = fetch_patient_by_id(conn, selected_id)
                    if not selected:
                        st.error(f"❌ No patient found with ID: {selected_id}")
                except ValueError:
                    st.error("❌ Please enter a valid numeric patient ID")
            
            if selected:
                st.markdown("### Edit patient")
                with st.form("edit_patient_form"):
                    ecol1, ecol2 = st.columns(2)
                    with ecol1:
                        e_first = st.text_input("First name", value=selected["first_name"])
                    with ecol2:
                        e_last = st.text_input("Last name", value=selected["last_name"])

                    e_phone = st.text_input("Phone", value=selected["phone"])
                    e_email = st.text_input("Email (optional)", value=selected["email"] or "")
                    e_address = st.text_area("Address", value=selected["address"], height=120)

                    edit_sub = st.form_submit_button("Save changes")
                    if edit_sub:
                        errs = []
                        if not e_first.strip():
                            errs.append("First name required.")
                        if not e_last.strip():
                            errs.append("Last name required.")
                        ok_phone, phone_msg = validate_phone(e_phone)
                        if not ok_phone:
                            errs.append(phone_msg)
                        ok_email, email_msg = validate_email(e_email)
                        if not ok_email:
                            errs.append(email_msg)
                        if not e_address.strip():
                            errs.append("Address required.")
                        if errs:
                            for e in errs:
                                st.error(e)
                        else:
                            update_patient(conn, selected["id"], e_first, e_last, e_phone, e_email or None, e_address)
                            st.success("Patient updated.")
                            df_all = fetch_all_patients(conn)
                            df = df_all

                st.markdown("#### Danger zone")
                if st.button("Delete this patient"):
                    delete_patient(conn, selected["id"])
                    st.warning("Patient deleted.")
                    df_all = fetch_all_patients(conn)
                    df = df_all

    # ---------- Lab Tests ----------
    elif action == "Lab Tests":
        st.subheader("🧪 Medical Lab Tests Management")
        
        lab_tab1, lab_tab2, lab_tab3, lab_tab4 = st.tabs(["Order Lab Test", "View All Orders", "Update Results", "Print Report"])
        
        with lab_tab1:
            st.markdown("### Order Lab Test for Patient")
            
            if df_all.empty:
                st.warning("No patients found. Please add a patient first.")
            else:
                # Patient ID filter (outside form for real-time filtering)
                st.markdown("#### Step 1: Find Patient")
                patient_id_input = st.text_input(
                    "Enter Patient ID",
                    placeholder="Enter patient ID to search...",
                    help="Enter the patient ID to view details and order tests"
                )
                
                selected_patient = None
                patient_data = None
                
                if patient_id_input:
                    try:
                        patient_id = int(patient_id_input)
                        patient_data = fetch_patient_by_id(conn, patient_id)
                        
                        if patient_data:
                            selected_patient = patient_id
                            # Display patient details
                            st.success(f"✅ Patient Found!")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Patient ID", patient_data["id"])
                                st.write(f"**Name:** {patient_data['first_name']} {patient_data['last_name']}")
                            with col2:
                                st.write(f"**Phone:** {patient_data['phone']}")
                                st.write(f"**Email:** {patient_data['email'] or 'N/A'}")
                            with col3:
                                st.write(f"**Address:** {patient_data['address']}")
                        else:
                            st.error(f"❌ No patient found with ID: {patient_id}")
                    except ValueError:
                        st.error("❌ Please enter a valid numeric patient ID")
                
                st.markdown("---")
                
                # Only show test selection if patient is found
                if selected_patient:
                    with st.form("order_lab_test_form"):
                        st.markdown("#### Step 2: Select Tests")
                        
                        # Get tests by category
                        tests_by_category = get_lab_tests_by_category(conn)
                        
                        selected_tests = []
                        
                        # Create columns for test categories
                        col_count = 3
                        cols = st.columns(col_count)
                        
                        categories = list(tests_by_category.keys())
                        for idx, category in enumerate(categories):
                            with cols[idx % col_count]:
                                st.markdown(f"**{category}**")
                                category_tests = tests_by_category[category]
                                
                                # Create multiselect for each category
                                selected = st.multiselect(
                                    f"{category} Tests",
                                    options=category_tests,
                                    key=f"tests_{category}",
                                    label_visibility="collapsed"
                                )
                                selected_tests.extend(selected)
                        
                        st.markdown("---")
                        st.markdown("#### Step 3: Test Details")
                        
                        # Test date and notes
                        test_date = st.date_input("Test Date", value=pd.Timestamp.now())
                        notes = st.text_area("Notes (optional)", max_chars=500)
                        
                        submit_order = st.form_submit_button("Order Selected Tests", type="primary")
                        
                        if submit_order:
                            if not selected_tests:
                                st.error("Please select at least one test.")
                            else:
                                ordered_count = 0
                                for test_name in selected_tests:
                                    order_lab_test(
                                        conn,
                                        selected_patient,
                                        test_name,
                                        str(test_date),
                                        st.session_state["username"],
                                        notes
                                    )
                                    ordered_count += 1
                                st.success(f"Successfully ordered {ordered_count} test(s) for patient ID {selected_patient}!")
                else:
                    st.info("👆 Enter a patient ID above to start ordering lab tests")
        
        with lab_tab2:
            st.markdown("### All Lab Test Orders")
            
            all_orders = fetch_all_lab_tests_orders(conn)
            
            if all_orders.empty:
                st.info("No lab test orders found.")
            else:
                # Add filters
                filter_col1, filter_col2, filter_col3 = st.columns(3)
                with filter_col1:
                    filter_patient = st.text_input("Filter by patient name")
                with filter_col2:
                    filter_test = st.text_input("Filter by test name")
                with filter_col3:
                    filter_status = st.selectbox("Filter by status", ["All", "Pending", "Completed", "Cancelled"])
                
                # Apply filters
                filtered_orders = all_orders.copy()
                if filter_patient:
                    filtered_orders = filtered_orders[
                        filtered_orders["patient_name"].str.contains(filter_patient, case=False, na=False)
                    ]
                if filter_test:
                    filtered_orders = filtered_orders[
                        filtered_orders["test_name"].str.contains(filter_test, case=False, na=False)
                    ]
                if filter_status != "All":
                    filtered_orders = filtered_orders[filtered_orders["test_status"] == filter_status]
                
                st.write(f"**Total orders:** {len(all_orders)} | **Showing:** {len(filtered_orders)}")
                
                # Display table
                display_cols = ["id", "patient_name", "test_name", "test_date", "test_status", 
                               "result_value", "result_unit", "ordered_by", "created_at"]
                display_df = filtered_orders[display_cols].copy()
                display_df = display_df.rename(columns={
                    "id": "ID",
                    "patient_name": "Patient",
                    "test_name": "Test Name",
                    "test_date": "Test Date",
                    "test_status": "Status",
                    "result_value": "Result",
                    "result_unit": "Unit",
                    "ordered_by": "Ordered By",
                    "created_at": "Created At"
                })
                
                st.dataframe(display_df, use_container_width=True, height=400)
                
                # Export option
                csv_bytes = df_to_csv_bytes(filtered_orders)
                st.download_button(
                    "Download as CSV",
                    data=csv_bytes,
                    file_name="lab_test_orders.csv",
                    mime="text/csv",
                    key="download_lab_orders_csv"
                )
        
        with lab_tab3:
            st.markdown("### Update Lab Test Results")
            
            all_orders = fetch_all_lab_tests_orders(conn)
            
            if all_orders.empty:
                st.info("No lab test orders found.")
            else:
                # Filter to show pending tests
                pending_orders = all_orders[all_orders["test_status"] == "Pending"]
                
                if pending_orders.empty:
                    st.info("No pending tests to update.")
                else:
                    selected_test_id = st.selectbox(
                        "Select Test to Update",
                        options=pending_orders["id"].tolist(),
                        format_func=lambda x: f"ID {x}: {pending_orders[pending_orders['id'] == x]['patient_name'].values[0]} - {pending_orders[pending_orders['id'] == x]['test_name'].values[0]} ({pending_orders[pending_orders['id'] == x]['test_date'].values[0]})"
                    )
                    
                    selected_test_data = fetch_lab_test_by_id(conn, selected_test_id)
                    
                    if selected_test_data:
                        st.markdown(f"**Patient ID:** {selected_test_data['patient_id']}")
                        st.markdown(f"**Test:** {selected_test_data['test_name']}")
                        st.markdown(f"**Test Date:** {selected_test_data['test_date']}")
                        st.markdown(f"**Current Status:** {selected_test_data['test_status']}")
                        
                        with st.form("update_result_form"):
                            new_status = st.selectbox(
                                "Status",
                                options=["Pending", "Completed", "Cancelled"],
                                index=["Pending", "Completed", "Cancelled"].index(selected_test_data["test_status"])
                            )
                            
                            result_value = st.text_input(
                                "Result Value",
                                value=selected_test_data["result_value"] or ""
                            )
                            
                            result_unit = st.text_input(
                                "Result Unit (e.g., mg/dL, mmol/L)",
                                value=selected_test_data["result_unit"] or ""
                            )
                            
                            reference_range = st.text_input(
                                "Reference Range (e.g., 70-100 mg/dL)",
                                value=selected_test_data["reference_range"] or ""
                            )
                            
                            update_notes = st.text_area(
                                "Additional Notes",
                                value=selected_test_data["notes"] or "",
                                max_chars=500
                            )
                            
                            submit_update = st.form_submit_button("Update Test Result")
                            
                            if submit_update:
                                update_lab_test_result(
                                    conn,
                                    selected_test_id,
                                    new_status,
                                    result_value if result_value else None,
                                    result_unit if result_unit else None,
                                    reference_range if reference_range else None,
                                    update_notes if update_notes else None
                                )
                                st.success("Test result updated successfully!")
                                st.rerun()
        
        with lab_tab4:
            st.markdown("### 🖨️ Print Lab Test Report")
            
            # Input for patient ID
            st.markdown("#### Enter Patient ID to Generate Report")
            report_patient_id = st.text_input(
                "Patient ID",
                placeholder="Enter patient ID...",
                key="print_report_patient_id"
            )
            
            if report_patient_id:
                try:
                    patient_id = int(report_patient_id)
                    patient_data = fetch_patient_by_id(conn, patient_id)
                    
                    if patient_data:
                        # Fetch patient's lab tests
                        patient_tests = fetch_patient_lab_tests(conn, patient_id)
                        
                        if patient_tests.empty:
                            st.warning(f"No lab tests found for Patient ID: {patient_id}")
                        else:
                            # Filter options
                            col1, col2 = st.columns(2)
                            with col1:
                                status_filter = st.selectbox(
                                    "Filter by Status",
                                    options=["All", "Completed", "Pending", "Cancelled"],
                                    key="report_status_filter"
                                )
                            with col2:
                                date_filter = st.date_input(
                                    "Filter by Test Date (optional)",
                                    value=None,
                                    key="report_date_filter"
                                )
                            
                            # Apply filters
                            filtered_tests = patient_tests.copy()
                            if status_filter != "All":
                                filtered_tests = filtered_tests[filtered_tests["test_status"] == status_filter]
                            if date_filter:
                                filtered_tests = filtered_tests[filtered_tests["test_date"] == str(date_filter)]
                            
                            if filtered_tests.empty:
                                st.info("No tests match the selected filters.")
                            else:
                                st.success(f"Found {len(filtered_tests)} test(s) for this patient")
                                
                                # Check if reportlab is available
                                if not REPORTLAB_AVAILABLE:
                                    st.error("❌ PDF generation is not available.")
                                    st.error("Please install reportlab: `pip install reportlab`")
                                    st.info("You can still view the test data below:")
                                    display_cols = ["test_name", "test_date", "test_status", "result_value", "result_unit"]
                                    display_df = filtered_tests[display_cols].copy()
                                    display_df.columns = ["Test Name", "Test Date", "Status", "Result", "Unit"]
                                    st.dataframe(display_df, use_container_width=True, height=300)
                                else:
                                    # Generate PDF
                                    try:
                                        pdf_bytes = generate_lab_report_pdf(patient_data, filtered_tests)
                                        
                                        # Display PDF preview info
                                        st.info("📄 PDF Report generated successfully!")
                                        
                                        # Show summary
                                        st.markdown("### Report Summary")
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("Patient ID", patient_data['id'])
                                        with col2:
                                            st.metric("Total Tests", len(filtered_tests))
                                        with col3:
                                            completed = len(filtered_tests[filtered_tests['test_status'] == 'Completed'])
                                            st.metric("Completed", completed)
                                        
                                        st.markdown("---")
                                        
                                        # Download and Send Options
                                        st.markdown("### Send Report to Patient")
                                        
                                        # Action buttons
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.download_button(
                                                label="📥 Download PDF Report",
                                                data=pdf_bytes,
                                                file_name=f"lab_report_patient_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                                mime="application/pdf",
                                                use_container_width=True,
                                                type="secondary",
                                                key=f"download_pdf_report_{patient_id}"
                                            )
                                        
                                        # View/Print PDF button
                                        with col2:
                                            import base64
                                            b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                                            pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
                                            
                                            if st.button("👁️ View/Print PDF", use_container_width=True, type="secondary"):
                                                st.session_state["show_pdf_viewer"] = True
                                                st.session_state["pdf_display_html"] = pdf_display
                                                st.rerun()
                                        
                                        # WhatsApp Send Option
                                        with col3:
                                            # Store PDF in session for WhatsApp send
                                            if st.button("📱 Send via WhatsApp", use_container_width=True, type="primary"):
                                                st.session_state["whatsapp_mode"] = True
                                                st.session_state["pdf_data"] = pdf_bytes
                                                st.session_state["patient_phone"] = patient_data['phone']
                                                st.session_state["patient_name"] = f"{patient_data['first_name']} {patient_data['last_name']}"
                                                st.session_state["patient_id_for_whatsapp"] = patient_id
                                                st.rerun()
                                        
                                        # PDF Viewer Section
                                        if st.session_state.get("show_pdf_viewer", False):
                                            st.markdown("---")
                                            st.markdown("#### 📄 PDF Preview")
                                            st.info("💡 Use your browser's print function (Ctrl+P / Cmd+P) to print this report directly")
                                            
                                            # Display PDF
                                            st.markdown(st.session_state.get("pdf_display_html", ""), unsafe_allow_html=True)
                                            
                                            # Close viewer button
                                            if st.button("✖️ Close Viewer", use_container_width=True):
                                                st.session_state["show_pdf_viewer"] = False
                                                st.rerun()
                                        
                                        # WhatsApp Send Section with pywhatkit
                                        if st.session_state.get("whatsapp_mode", False):
                                            st.markdown("---")
                                            st.markdown("#### 📱 Send Report via WhatsApp")
                                            
                                            with st.form("whatsapp_send_form"):
                                                # Patient phone number (pre-filled)
                                                whatsapp_phone = st.text_input(
                                                    "Patient Phone Number",
                                                    value=st.session_state.get("patient_phone", ""),
                                                    help="Enter phone number with country code (e.g., +919711172197)"
                                                )
                                                
                                                # Report summary message
                                                completed_tests = len(filtered_tests[filtered_tests['test_status'] == 'Completed'])
                                                pending_tests = len(filtered_tests[filtered_tests['test_status'] == 'Pending'])
                                                
                                                default_message = f"""Dear {st.session_state.get("patient_name", "Patient")},

Your lab test report is ready!

Report Summary:
- Total Tests: {len(filtered_tests)}
- Completed: {completed_tests}
- Pending: {pending_tests}

Please check the attached PDF report.

For any queries, contact KaviHealthCare Lab.

Best regards,
KaviHealthCare Team"""
                                                
                                                message_text = st.text_area(
                                                    "Message to Patient",
                                                    value=default_message,
                                                    height=200,
                                                    help="Message that will be sent with the PDF report"
                                                )
                                                
                                                col1, col2 = st.columns(2)
                                                with col1:
                                                    send_whatsapp = st.form_submit_button("📤 Send via WhatsApp", type="primary", use_container_width=True)
                                                with col2:
                                                    cancel_whatsapp = st.form_submit_button("❌ Cancel", use_container_width=True)
                                            
                                            # Handle form submission outside the form
                                            if cancel_whatsapp:
                                                st.session_state["whatsapp_mode"] = False
                                                st.session_state["sending_status"] = None
                                                st.rerun()
                                            
                                            if send_whatsapp:
                                                if not whatsapp_phone.strip():
                                                    st.error("Please enter a valid phone number")
                                                else:
                                                    # Clean phone number
                                                    clean_phone = whatsapp_phone.strip()
                                                    if not clean_phone.startswith('+'):
                                                        clean_phone = '+' + ''.join(filter(str.isdigit, clean_phone))
                                                    
                                                    # Show processing message
                                                    with st.spinner("📱 Sending WhatsApp message with PDF via Twilio..."):
                                                        try:
                                                            # Get PDF data from session
                                                            pdf_data = st.session_state.get("pdf_data", b'')
                                                            patient_id_temp = st.session_state.get("patient_id_for_whatsapp", patient_id)
                                                            pdf_filename = f"lab_report_patient_{patient_id_temp}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                                                            
                                                            # Send via Twilio WhatsApp API
                                                            success, result_message = send_whatsapp_pdf(
                                                                to_phone=clean_phone,
                                                                pdf_bytes=pdf_data,
                                                                message_text=message_text,
                                                                pdf_filename=pdf_filename
                                                            )
                                                            
                                                            if success:
                                                                st.success(f"""
✅ WhatsApp message sent successfully!

**Details:**
- Recipient: {clean_phone}
- PDF uploaded to temporary hosting
- Message delivered via Twilio WhatsApp API

The report should be delivered to the patient within seconds.
                                                                """)
                                                                
                                                                # Provide download option as backup
                                                                st.download_button(
                                                                    label="📥 Download PDF Again (if needed)",
                                                                    data=pdf_data,
                                                                    file_name=pdf_filename,
                                                                    mime="application/pdf",
                                                                    use_container_width=True,
                                                                    key=f"download_pdf_backup_{st.session_state.get('patient_id_for_whatsapp', patient_id)}"
                                                                )
                                                                
                                                                st.session_state["sending_status"] = "sent"
                                                            else:
                                                                st.error(f"""
❌ Failed to send WhatsApp message

**Error:** {result_message}

**Troubleshooting:**
- Check your Twilio credentials (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
- Verify the phone number format (include country code, e.g., +919711172197)
- Ensure your Twilio WhatsApp sender number is configured
- Check that your Twilio account has WhatsApp enabled

Download the PDF below and send manually if needed.
                                                                """)
                                                                
                                                                # Provide download option on error
                                                                st.download_button(
                                                                    label="📥 Download PDF Report",
                                                                    data=pdf_data,
                                                                    file_name=pdf_filename,
                                                                    mime="application/pdf",
                                                                    use_container_width=True,
                                                                    key=f"download_pdf_error_{st.session_state.get('patient_id_for_whatsapp', patient_id)}"
                                                                )
                                                            
                                                        except Exception as e:
                                                            st.error(f"""
❌ Unexpected error: {str(e)}

**Troubleshooting:**
- Ensure Twilio library is installed: `pip install twilio`
- Check your internet connection
- Verify Twilio credentials are set correctly
- Download the PDF below and send manually
                                                            """)
                                                            
                                                            # Provide download option on error
                                                            st.download_button(
                                                                label="📥 Download PDF Report",
                                                                data=st.session_state.get("pdf_data", b''),
                                                                file_name=f"lab_report_patient_{st.session_state.get('patient_id_for_whatsapp', patient_id)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                                                mime="application/pdf",
                                                                use_container_width=True,
                                                                key=f"download_pdf_error_{st.session_state.get('patient_id_for_whatsapp', patient_id)}"
                                                            )
                                            
                                            # Close button
                                            if st.session_state.get("sending_status") == "sent":
                                                if st.button("✅ Done", use_container_width=True, type="primary"):
                                                    st.session_state["whatsapp_mode"] = False
                                                    st.session_state["sending_status"] = None
                                                    st.rerun()
                                        
                                        # Show test details
                                        st.markdown("---")
                                        st.markdown("### Tests Included in Report")
                                        display_cols = ["test_name", "test_date", "test_status", "result_value", "result_unit"]
                                        display_df = filtered_tests[display_cols].copy()
                                        display_df.columns = ["Test Name", "Test Date", "Status", "Result", "Unit"]
                                        st.dataframe(display_df, use_container_width=True, height=300)
                                        
                                    except Exception as e:
                                        st.error(f"Error generating PDF: {str(e)}")
                                        st.error("Please ensure reportlab is properly installed.")
                                        st.code("pip install reportlab")
                                        
                                        # Show data anyway
                                        st.info("Here's the test data:")
                                        display_cols = ["test_name", "test_date", "test_status", "result_value", "result_unit"]
                                        display_df = filtered_tests[display_cols].copy()
                                        display_df.columns = ["Test Name", "Test Date", "Status", "Result", "Unit"]
                                        st.dataframe(display_df, use_container_width=True, height=300)
                    else:
                        st.error(f"❌ No patient found with ID: {patient_id}")
                except ValueError:
                    st.error("❌ Please enter a valid numeric patient ID")

    # ---------- Import CSV ----------
    elif action == "Import (CSV)":
        st.subheader("Import patients from CSV")
        st.markdown("CSV must have columns: first_name, last_name, phone, email (optional), address")
        uploaded = st.file_uploader("Upload CSV", type=["csv"])
        if uploaded:
            try:
                csv_df = pd.read_csv(uploaded)
            except Exception as e:
                st.error(f"Couldn't read CSV: {e}")
                csv_df = None

            if csv_df is not None:
                st.write("Preview (first 10 rows):")
                st.dataframe(csv_df.head(10))
                if st.button("Import rows"):
                    required_cols = {"first_name", "last_name", "phone", "address"}
                    if not required_cols.issubset(set(csv_df.columns.str.lower())):
                        st.error(f"CSV missing required columns. Required: {required_cols}")
                    else:
                        imported = 0
                        errors = []
                        for idx, row in csv_df.iterrows():
                            # Normalize column names to lower for reading
                            r = {k.lower(): (v if not pd.isna(v) else "") for k, v in row.items()}
                            fn = r.get("first_name", "")
                            ln = r.get("last_name", "")
                            ph = r.get("phone", "")
                            em = r.get("email", "")
                            addr = r.get("address", "")
                            ok_phone, phone_msg = validate_phone(str(ph))
                            ok_email, email_msg = validate_email(str(em) if em is not None else "")
                            if not fn or not ln or not addr or not ok_phone or not ok_email:
                                errors.append(f"Row {idx+1}: validation failed.")
                                continue
                            insert_patient(conn, str(fn), str(ln), str(ph), str(em) if em else None, str(addr))
                            imported += 1
                        st.success(f"Imported {imported} rows. {len(errors)} rows skipped.")
                        if errors:
                            st.write("Sample errors:")
                            st.write(errors[:10])
                        df_all = fetch_all_patients(conn)
                        df = df_all

    # Footer: Show raw DB preview (collapsible)
    st.markdown("---")
    with st.expander("Raw database preview (for debugging)"):
        st.write("Full table:")
        st.dataframe(df_all)

if __name__ == "__main__":
    main()
