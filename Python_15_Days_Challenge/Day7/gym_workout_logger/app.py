import streamlit as st
import pandas as pd
import plotly.express as px
from data_manager import load_data, save_workout, get_common_exercises, get_exercise_type

# Page configuration
st.set_page_config(
    page_title="Gym Workout Logger",
    page_icon="🏋️‍♂️",
    layout="wide"
)

# Custom CSS for Light UI
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background: #ffffff;
    }
    h1 {
        color: #2c3e50;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #4CAF50;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        color: #4a4a4a;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏋️‍♂️ Gym Workout Logger")
st.markdown("### Track your fitness journey with ease!")

# Sidebar for Input
with st.sidebar:
    st.header("Log a Workout")
    # Exercise Selection
    exercise_option = st.selectbox("Exercise Name", get_common_exercises())
    
    if exercise_option == "Other":
        exercise = st.text_input("Enter Custom Exercise Name", placeholder="e.g., Muscle Up")
    else:
        exercise = exercise_option

    exercise_type = get_exercise_type(exercise_option)
    
    # Initialize variables
    sets = 0
    reps = 0
    weight = 0.0
    duration = 0
    distance = 0.0
    
    if exercise_type == "strength":
        sets = st.number_input("Sets", min_value=1, value=3)
        reps = st.number_input("Reps", min_value=1, value=10)
        weight = st.number_input("Weight (kg)", min_value=0.0, value=20.0, step=2.5)
    elif exercise_type == "duration":
        sets = st.number_input("Sets", min_value=1, value=3)
        duration = st.number_input("Duration (minutes)", min_value=1, value=1)
    elif exercise_type == "cardio":
        duration = st.number_input("Duration (minutes)", min_value=1, value=30)
        distance = st.number_input("Distance (km)", min_value=0.0, value=5.0, step=0.1)
    
    if st.button("Log Workout"):
        if exercise:
            save_workout(exercise, sets, reps, weight, duration, distance)
            
            # Success message based on type
            if exercise_type == "strength":
                st.success(f"Logged: {exercise} - {sets}x{reps} @ {weight}kg")
            elif exercise_type == "duration":
                st.success(f"Logged: {exercise} - {sets} sets for {duration} mins")
            elif exercise_type == "cardio":
                st.success(f"Logged: {exercise} - {distance}km in {duration} mins")
        else:
            st.error("Please enter an exercise name.")

# Main Content Area
col1, col2 = st.columns([1, 2])

# Load Data
df = load_data()

with col1:
    st.subheader("Recent Workouts")
    if not df.empty:
        # Sort by Date descending
        df_display = df.sort_values(by="Date", ascending=False)
        st.dataframe(df_display, use_container_width=True)
    else:
        st.info("No workouts logged yet. Start by adding one from the sidebar!")

with col2:
    st.subheader("Weekly Progress")
    if not df.empty:
        # Filter for specific exercise to show progress
        exercises = df['Exercise'].unique()
        selected_exercise = st.selectbox("Select Exercise to View Progress", exercises)
        
        if selected_exercise:
            exercise_data = df[df['Exercise'] == selected_exercise].copy()
            exercise_data = exercise_data.sort_values(by="Date")
            
            # Create Line Chart
            fig = px.line(
                exercise_data, 
                x="Date", 
                y="Weight", 
                title=f"Weight Progression for {selected_exercise}",
                markers=True,
                labels={"Weight": "Weight (kg)", "Date": "Date"}
            )
            fig.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(color="#2c3e50")
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Log some workouts to see your progress graph!")

st.markdown("---")
st.caption("Built with Streamlit & ❤️")
