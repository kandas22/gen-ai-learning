import pandas as pd
import os
from datetime import datetime

DATA_FILE = "workouts.csv"

def initialize_data():
    """Initializes the CSV file if it doesn't exist."""
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["Date", "Exercise", "Sets", "Reps", "Weight", "Duration", "Distance"])
        df.to_csv(DATA_FILE, index=False)

def load_data():
    """Loads workout data from CSV."""
    initialize_data()
    try:
        df = pd.read_csv(DATA_FILE)
        
        # Schema Migration: Add missing columns if they don't exist
        expected_columns = ["Date", "Exercise", "Sets", "Reps", "Weight", "Duration", "Distance"]
        for col in expected_columns:
            if col not in df.columns:
                df[col] = 0 if col in ["Sets", "Reps", "Weight", "Duration", "Distance"] else None
        
        # Ensure Date is datetime for sorting/plotting
        if not df.empty:
            df['Date'] = pd.to_datetime(df['Date'])
        return df
    except Exception as e:
        return pd.DataFrame(columns=["Date", "Exercise", "Sets", "Reps", "Weight", "Duration", "Distance"])

def save_workout(exercise, sets, reps, weight, duration=0, distance=0):
    """Saves a new workout entry."""
    initialize_data()
    
    # Load existing data to check for schema updates (or just rely on append if schema matches)
    # Ideally we should ensure the file has the right columns before appending.
    # Calling load_data() ensures migration happens if needed.
    load_data() 
    
    new_entry = pd.DataFrame({
        "Date": [datetime.now()],
        "Exercise": [exercise],
        "Sets": [sets],
        "Reps": [reps],
        "Weight": [weight],
        "Duration": [duration],
        "Distance": [distance]
    })
    # Append to CSV without reading the whole file if possible, but for simplicity and consistency with load, we append mode
    new_entry.to_csv(DATA_FILE, mode='a', header=False, index=False)

def get_common_exercises():
    """Returns a dictionary of common gym exercises and their types."""
    return {
        "Bench Press": "strength",
        "Squat": "strength",
        "Deadlift": "strength",
        "Overhead Press": "strength",
        "Barbell Row": "strength",
        "Pull Up": "strength",
        "Dumbbell Press": "strength",
        "Dumbbell Row": "strength",
        "Lateral Raise": "strength",
        "Bicep Curl": "strength",
        "Tricep Extension": "strength",
        "Leg Press": "strength",
        "Leg Extension": "strength",
        "Leg Curl": "strength",
        "Calf Raise": "strength",
        "Plank": "duration",
        "Crunch": "strength",
        "Russian Twist": "strength",
        "Running": "cardio",
        "Cycling": "cardio",
        "Jump Rope": "duration",
        "Other": "strength"
    }

def get_exercise_type(exercise_name):
    """Returns the type of the exercise."""
    exercises = get_common_exercises()
    return exercises.get(exercise_name, "strength")
