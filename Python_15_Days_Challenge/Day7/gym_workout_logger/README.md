# Gym Workout Logger 🏋️‍♂️

A simple and beautiful Streamlit application to log your gym workouts and track your progress over time.

## Features

- **Log Workouts**: Record exercise name, sets, reps, and weight.
- **Data Persistence**: Workouts are saved to a local CSV file (`workouts.csv`).
- **Visual Progress**: View a weekly progress graph for each exercise.
- **Light UI**: Clean and modern interface.

## Installation

1.  **Clone the repository** (if applicable) or navigate to the project folder.
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the application**:
    ```bash
    streamlit run app.py
    ```
2.  **Open your browser**: The app will typically run at `http://localhost:8501`.
3.  **Start Logging**: Use the sidebar to enter your workout details and click "Log Workout".
4.  **View Progress**: Check the table for recent entries and select an exercise to see your weight progression graph.

## Technologies

- Python
- Streamlit
- Pandas
- Plotly
