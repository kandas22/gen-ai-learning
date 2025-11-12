import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Expense Splitter",
    page_icon="💰",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stButton > button {
        background-color: #0066CC;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        transition: background-color 0.3s;
    }
    .stButton > button:hover {
        background-color: #0052A3;
    }
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("💰 Expense Splitter")
st.markdown("---")

# Initialize session state
if 'people_data' not in st.session_state:
    st.session_state.people_data = []

# Sidebar for inputs
with st.sidebar:
    st.header("📝 Enter Expense Details")
    
    # Total amount input
    total_amount = st.number_input(
        "Total Amount (₹)",
        min_value=0.0,
        value=0.0,
        step=100.0,
        help="Enter the total amount spent"
    )
    
    # Number of people
    num_people = st.number_input(
        "Number of People",
        min_value=1,
        max_value=20,
        value=1,
        step=1,
        help="How many people are splitting the expense?"
    )
    
    st.markdown("---")
    st.subheader("👥 Add People Details (Optional)")
    
    # Dynamic form for people
    people_list = []
    contributions = {}
    
    for i in range(num_people):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(
                f"Person {i+1} Name",
                value=f"Person {i+1}",
                key=f"name_{i}",
                help="Enter name (optional)"
            )
        with col2:
            contribution = st.number_input(
                f"Contribution (₹)",
                min_value=0.0,
                value=0.0,
                step=100.0,
                key=f"contrib_{i}",
                help="Amount this person already paid"
            )
        
        people_list.append(name if name.strip() else f"Person {i+1}")
        contributions[name if name.strip() else f"Person {i+1}"] = contribution

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Expense Summary")
    
    if total_amount > 0 and num_people > 0:
        # Calculate equal share
        equal_share = total_amount / num_people
        
        # Calculate balances
        balances = {}
        total_contributed = sum(contributions.values())
        
        for person in people_list:
            contribution = contributions.get(person, 0.0)
            balance = contribution - equal_share
            balances[person] = {
                'contribution': contribution,
                'equal_share': equal_share,
                'balance': balance
            }
        
        # Display summary metrics
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric("Total Amount", f"₹{total_amount:,.2f}")
        with metric_col2:
            st.metric("Equal Share per Person", f"₹{equal_share:,.2f}")
        with metric_col3:
            st.metric("Total Contributed", f"₹{total_contributed:,.2f}")
        
        # Check if contributions match total
        if abs(total_contributed - total_amount) > 0.01:
            if total_contributed < total_amount:
                st.warning(f"⚠️ Total contributions (₹{total_contributed:,.2f}) is less than total amount (₹{total_amount:,.2f}). "
                          f"Difference: ₹{total_amount - total_contributed:,.2f} needs to be accounted for.")
            else:
                st.warning(f"⚠️ Total contributions (₹{total_contributed:,.2f}) exceeds total amount (₹{total_amount:,.2f}). "
                          f"Excess: ₹{total_contributed - total_amount:,.2f}")
        
        st.markdown("---")
        
        # Create results dataframe
        results_data = []
        for person, data in balances.items():
            results_data.append({
                'Person': person,
                'Contributed': data['contribution'],
                'Equal Share': data['equal_share'],
                'Balance': data['balance']
            })
        
        df = pd.DataFrame(results_data)
        
        # Display results table
        st.subheader("💵 Who Owes / Gets Back")
        
        # Format the dataframe for display
        display_df = df.copy()
        display_df['Contributed'] = display_df['Contributed'].apply(lambda x: f"₹{x:,.2f}")
        display_df['Equal Share'] = display_df['Equal Share'].apply(lambda x: f"₹{x:,.2f}")
        display_df['Balance'] = display_df['Balance'].apply(lambda x: f"₹{x:,.2f}")
        display_df['Status'] = df['Balance'].apply(
            lambda x: "💰 Gets Back" if x > 0.01 else ("💸 Owes" if x < -0.01 else "✅ Settled")
        )
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Detailed breakdown
        st.markdown("---")
        st.subheader("📋 Detailed Breakdown")
        
        for person, data in balances.items():
            balance = data['balance']
            if balance > 0.01:
                st.success(f"✅ **{person}** gets back **₹{balance:,.2f}** "
                          f"(paid ₹{data['contribution']:,.2f}, owes ₹{data['equal_share']:,.2f})")
            elif balance < -0.01:
                st.error(f"❌ **{person}** owes **₹{abs(balance):,.2f}** "
                        f"(paid ₹{data['contribution']:,.2f}, owes ₹{data['equal_share']:,.2f})")
            else:
                st.info(f"✅ **{person}** is settled (paid exactly ₹{data['equal_share']:,.2f})")

with col2:
    st.subheader("📈 Utilization Graphs")
    
    if total_amount > 0 and num_people > 0:
        # Graph 1: Contributions vs Equal Share
        st.markdown("#### Contribution Comparison")
        
        graph_df = pd.DataFrame({
            'Person': people_list,
            'Contributed': [balances[p]['contribution'] for p in people_list],
            'Equal Share': [balances[p]['equal_share'] for p in people_list]
        })
        
        fig1 = go.Figure()
        
        fig1.add_trace(go.Bar(
            name='Contributed',
            x=graph_df['Person'],
            y=graph_df['Contributed'],
            marker_color='#2ecc71',
            text=[f"₹{x:,.0f}" for x in graph_df['Contributed']],
            textposition='auto'
        ))
        
        fig1.add_trace(go.Bar(
            name='Equal Share',
            x=graph_df['Person'],
            y=graph_df['Equal Share'],
            marker_color='#3498db',
            text=[f"₹{x:,.0f}" for x in graph_df['Equal Share']],
            textposition='auto'
        ))
        
        fig1.update_layout(
            barmode='group',
            height=300,
            xaxis_title="Person",
            yaxis_title="Amount (₹)",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig1, use_container_width=True)
        
        # Graph 2: Balance Chart
        st.markdown("#### Balance Overview")
        
        balance_df = pd.DataFrame({
            'Person': people_list,
            'Balance': [balances[p]['balance'] for p in people_list]
        })
        
        # Color based on positive/negative balance
        colors = ['#e74c3c' if x < 0 else '#2ecc71' for x in balance_df['Balance']]
        
        fig2 = go.Figure()
        
        fig2.add_trace(go.Bar(
            x=balance_df['Person'],
            y=balance_df['Balance'],
            marker_color=colors,
            text=[f"₹{x:,.0f}" for x in balance_df['Balance']],
            textposition='auto'
        ))
        
        # Add zero line
        fig2.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        fig2.update_layout(
            height=300,
            xaxis_title="Person",
            yaxis_title="Balance (₹)",
            showlegend=False
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # Graph 3: Pie chart of contributions
        if total_contributed > 0:
            st.markdown("#### Contribution Distribution")
            
            contrib_df = pd.DataFrame({
                'Person': people_list,
                'Contribution': [balances[p]['contribution'] for p in people_list]
            })
            contrib_df = contrib_df[contrib_df['Contribution'] > 0]
            
            if len(contrib_df) > 0:
                fig3 = px.pie(
                    contrib_df,
                    values='Contribution',
                    names='Person',
                    title="",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig3.update_traces(textposition='inside', textinfo='percent+label')
                fig3.update_layout(height=300, showlegend=False)
                st.plotly_chart(fig3, use_container_width=True)

# Footer
st.markdown("---")
st.info("💡 **Tip:** Enter the total amount and number of people. Optionally add names and individual contributions to see who owes or gets back money!")

