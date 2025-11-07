"""
Patient Profile Management Streamlit App
Modular app using SQLite for persistence with separated database layer.

Fields:
- first_name (required)
- last_name (required)
- phone (required, digits)
- email (optional, validated if provided)
- address (required)

Features:
- Add / Edit / Delete
- Search + filter
- Export CSV
- Simple validation and user feedback
"""

from typing import Tuple
import pandas as pd
import streamlit as st
import validators

# Import database operations from separate package
from database import (
    get_connection,
    init_db,
    insert_patient,
    update_patient,
    delete_patient,
    fetch_all_patients,
    fetch_patient_by_id
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
# Streamlit UI
# -----------------------
def main():
    st.set_page_config(page_title="Patient Profiles", page_icon="🩺", layout="wide")

    conn = get_connection()
    init_db(conn)

    st.title("🩺 Patient Profile Management")
    st.write("Create, search, edit, and export patient profiles. Email is optional.")

    # Sidebar - actions and search
    st.sidebar.header("Actions")
    action = st.sidebar.radio("Select action", ["Add patient", "View & manage patients", "Import (CSV)"], index=1)

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
            col_top[2].download_button("Download visible as CSV", data=csv_bytes, file_name="patients_export.csv", mime="text/csv")

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
            selected_id = st.selectbox("Patient ID", options=display_df["ID"].tolist())

            # Fetch selected record
            selected = fetch_patient_by_id(conn, int(selected_id))
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
