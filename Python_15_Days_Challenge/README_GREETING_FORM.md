# Greeting Form - Streamlit App

A simple Streamlit application that collects user information and displays a personalized greeting.

## 15 Days Challenge Progress

Track your daily progress through the Python Streamlit challenge!

| Day | Challenge | Status | Date Completed | Description |
|-----|-----------|--------|----------------|-------------|
| 1 | Greeting Form | ✅ Completed | Nov 11, 2025 | Built a form with name input, age slider, and personalized greeting display |
| 2 | TBD | ⏳ Pending | - | Coming soon... |
| 3 | TBD | ⏳ Pending | - | Coming soon... |
| 4 | TBD | ⏳ Pending | - | Coming soon... |
| 5 | TBD | ⏳ Pending | - | Coming soon... |
| 6 | TBD | ⏳ Pending | - | Coming soon... |
| 7 | TBD | ⏳ Pending | - | Coming soon... |
| 8 | TBD | ⏳ Pending | - | Coming soon... |
| 9 | TBD | ⏳ Pending | - | Coming soon... |
| 10 | TBD | ⏳ Pending | - | Coming soon... |
| 11 | TBD | ⏳ Pending | - | Coming soon... |
| 12 | TBD | ⏳ Pending | - | Coming soon... |
| 13 | TBD | ⏳ Pending | - | Coming soon... |
| 14 | TBD | ⏳ Pending | - | Coming soon... |
| 15 | TBD | ⏳ Pending | - | Coming soon... |

**Progress: 1/15 Days Completed (6.67%)** 🎉

---

## Features

- **Name Input**: Text field to enter your name
- **Age Slider**: Interactive slider to select age (1-120 years)
- **Personalized Greetings**: Age-appropriate greetings based on user input
- **Fun Metrics**: Displays name length, age, and estimated days lived
- **Interactive UI**: Clean form with validation and celebration effects

## Prerequisites

- Python 3.7 or higher
- Streamlit

## Installation

Install the required dependency:

```bash
pip install streamlit
```

## Usage

Run the Streamlit app:

```bash
streamlit run greeting_form.py
```

The app will open in your default web browser (typically at `http://localhost:8501`).

## How to Use

1. Enter your name in the text field
2. Use the slider to select your age
3. Click "Generate Greeting" button
4. View your personalized greeting with fun metrics!

## Features Breakdown

### Form Components
- **Text Input**: For entering name with placeholder text
- **Slider**: Age selection from 1 to 120 years
- **Submit Button**: Triggers form validation and greeting generation

### Greeting Logic
The app provides age-appropriate greetings:
- Under 13: Kid-friendly greeting
- 13-19: Teenage greeting
- 20-29: Young adult greeting
- 30-49: Professional greeting
- 50-69: Wisdom-focused greeting
- 70+: Life experience celebration

### Additional Metrics
- Name character count
- Current age display
- Approximate days lived calculation

## Customization

You can customize the greetings by modifying the age ranges and messages in the script:

```python
if age < 13:
    greeting = "Your custom message here"
```

## Screenshots

The app includes:
- Clean, centered layout
- Form validation
- Success messages
- Balloon animation on submission
- Three-column metrics display

## Notes

- Name field cannot be empty (validation included)
- Age defaults to 25 if not adjusted
- Balloons appear on successful submission
- Days lived calculation is approximate (365 days/year)

## License

Free to use and modify for learning purposes.
