import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os

# Set page configuration
st.set_page_config(
    page_title="Water Intake Tracker",
    page_icon="💧",
    layout="wide"
)

# Custom CSS for styling
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
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #0052A3;
    }
    .water-card {
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    .goal-reached {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .progress-text {
        font-size: 2em;
        font-weight: bold;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Data file path
DATA_FILE = "Python_15_Days_Challenge/Day6/water_data.json"

# Initialize or load data
def load_data():
    """Load water intake data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    """Save water intake data to JSON file"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_today_date():
    """Get today's date as string"""
    return datetime.now().strftime("%Y-%m-%d")

def get_week_dates():
    """Get list of dates for the past 7 days"""
    today = datetime.now()
    return [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]

# Load data
if 'water_data' not in st.session_state:
    st.session_state.water_data = load_data()

# Title and header
st.title("💧 Water Intake Tracker")
st.markdown("### Stay Hydrated! Track Your Daily Water Consumption")
st.markdown("---")

# Daily goal in ml
DAILY_GOAL = 3000  # 3 liters = 3000 ml

# Get today's date
today = get_today_date()

# Initialize today's data if not exists
if today not in st.session_state.water_data:
    st.session_state.water_data[today] = 0

# Current intake
current_intake = st.session_state.water_data[today]
progress_percentage = min((current_intake / DAILY_GOAL) * 100, 100)
goal_reached = current_intake >= DAILY_GOAL

# Main layout - 3 columns
col1, col2, col3 = st.columns([2, 3, 2])

with col1:
    st.markdown("### 📊 Today's Progress")
    
    # Progress display
    if goal_reached:
        st.markdown(f"""
            <div class='water-card goal-reached'>
                <h2>🎉 Goal Reached!</h2>
                <div class='progress-text'>{current_intake} ml</div>
                <p>You've reached your 3L goal!</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class='water-card'>
                <h2>💧 Current Intake</h2>
                <div class='progress-text'>{current_intake} ml</div>
                <p>{DAILY_GOAL - current_intake} ml to go!</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Progress bar
    st.progress(progress_percentage / 100)
    st.markdown(f"**{progress_percentage:.1f}%** of daily goal")
    
    # Quick info
    st.info(f"🎯 Daily Goal: {DAILY_GOAL} ml (3 Liters)")
    
    # Statistics
    st.markdown("### 📈 Statistics")
    st.metric("Today's Total", f"{current_intake} ml")
    st.metric("Remaining", f"{max(0, DAILY_GOAL - current_intake)} ml")
    st.metric("Goal Progress", f"{progress_percentage:.1f}%")

with col2:
    st.markdown("### 💧 Log Water Intake")
    
    # Quick add buttons
    st.markdown("#### Quick Add")
    quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)
    
    with quick_col1:
        if st.button("🥤 250ml\nGlass", key="add_250"):
            st.session_state.water_data[today] += 250
            save_data(st.session_state.water_data)
            st.rerun()
    
    with quick_col2:
        if st.button("🍶 500ml\nBottle", key="add_500"):
            st.session_state.water_data[today] += 500
            save_data(st.session_state.water_data)
            st.rerun()
    
    with quick_col3:
        if st.button("💧 750ml\nLarge", key="add_750"):
            st.session_state.water_data[today] += 750
            save_data(st.session_state.water_data)
            st.rerun()
    
    with quick_col4:
        if st.button("🥛 1000ml\nLiter", key="add_1000"):
            st.session_state.water_data[today] += 1000
            save_data(st.session_state.water_data)
            st.rerun()
    
    st.markdown("---")
    
    # Custom amount
    st.markdown("#### Custom Amount")
    custom_amount = st.number_input(
        "Enter custom amount (ml)",
        min_value=50,
        max_value=2000,
        value=250,
        step=50,
        help="Enter any custom water amount"
    )
    
    col_add, col_remove, col_reset = st.columns(3)
    
    with col_add:
        if st.button("➕ Add", type="primary", use_container_width=True):
            st.session_state.water_data[today] += custom_amount
            save_data(st.session_state.water_data)
            st.success(f"Added {custom_amount} ml!")
            st.rerun()
    
    with col_remove:
        if st.button("➖ Remove", use_container_width=True):
            st.session_state.water_data[today] = max(0, st.session_state.water_data[today] - custom_amount)
            save_data(st.session_state.water_data)
            st.warning(f"Removed {custom_amount} ml")
            st.rerun()
    
    with col_reset:
        if st.button("🔄 Reset Today", use_container_width=True):
            st.session_state.water_data[today] = 0
            save_data(st.session_state.water_data)
            st.info("Today's intake reset to 0")
            st.rerun()
    
    st.markdown("---")
    
    # Weekly chart
    st.markdown("### 📅 Weekly Hydration Chart")
    
    # Prepare weekly data
    week_dates = get_week_dates()
    week_data = []
    
    for date in week_dates:
        intake = st.session_state.water_data.get(date, 0)
        # Format date as "Mon 18" or "Tue 19"
        dt = datetime.strptime(date, "%Y-%m-%d")
        day_name = dt.strftime("%a %d")
        week_data.append({
            "Date": day_name,
            "Intake (ml)": intake,
            "Full Date": date,
            "Goal Met": "Yes" if intake >= DAILY_GOAL else "No"
        })
    
    df = pd.DataFrame(week_data)
    
    # Create bar chart
    fig = go.Figure()
    
    # Add bars with colors based on goal achievement
    colors = ['#38ef7d' if x >= DAILY_GOAL else '#667eea' for x in df["Intake (ml)"]]
    
    fig.add_trace(go.Bar(
        x=df["Date"],
        y=df["Intake (ml)"],
        marker_color=colors,
        text=df["Intake (ml)"],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Intake: %{y} ml<extra></extra>'
    ))
    
    # Add goal line
    fig.add_hline(
        y=DAILY_GOAL,
        line_dash="dash",
        line_color="red",
        annotation_text="Daily Goal (3000 ml)",
        annotation_position="right"
    )
    
    fig.update_layout(
        title="7-Day Water Intake",
        xaxis_title="Day",
        yaxis_title="Water Intake (ml)",
        height=400,
        showlegend=False,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Weekly summary
    total_week = sum(df["Intake (ml)"])
    avg_week = total_week / 7
    days_goal_met = sum(1 for x in df["Intake (ml)"] if x >= DAILY_GOAL)
    
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    with summary_col1:
        st.metric("Weekly Total", f"{total_week} ml")
    with summary_col2:
        st.metric("Daily Average", f"{avg_week:.0f} ml")
    with summary_col3:
        st.metric("Goals Met", f"{days_goal_met}/7 days")

with col3:
    st.markdown("### 💡 Hydration Tips")
    
    st.info("""
    **Benefits of Staying Hydrated:**
    - 🧠 Improves brain function
    - 💪 Boosts energy levels
    - 🎯 Enhances physical performance
    - 🌟 Promotes healthy skin
    - 🔥 Aids in weight management
    - 🩺 Supports kidney function
    """)
    
    st.success("""
    **Tips to Drink More Water:**
    - Keep a water bottle handy
    - Set hourly reminders
    - Drink before meals
    - Add lemon or fruit for flavor
    - Track your progress daily
    - Make it a habit!
    """)
    
    # Hydration recommendations
    st.markdown("### 🕐 Recommended Schedule")
    st.markdown("""
    - **Morning (6-9 AM)**: 500ml
    - **Mid-Morning (9-12 PM)**: 750ml
    - **Afternoon (12-3 PM)**: 750ml
    - **Evening (3-6 PM)**: 500ml
    - **Night (6-9 PM)**: 500ml
    
    **Total: 3000ml (3 Liters)**
    """)
    
    # Water facts
    with st.expander("💧 Interesting Water Facts"):
        st.markdown("""
        - 60% of your body is water
        - Your brain is 73% water
        - You should drink before feeling thirsty
        - Mild dehydration can affect mood
        - Water helps flush out toxins
        - Proper hydration improves skin elasticity
        """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>💧 Remember: Drink water regularly throughout the day for optimal health!</p>
        <p><small>Data is saved locally in water_data.json</small></p>
    </div>
""", unsafe_allow_html=True)
