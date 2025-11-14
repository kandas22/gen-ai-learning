# BMI Calculator - Day 4 Challenge

A professional BMI (Body Mass Index) Calculator built with Streamlit that calculates and categorizes your BMI based on height and weight inputs.

## Features

- **User-Friendly Inputs**: Number inputs for height (cm) and weight (kg)
- **Accurate BMI Calculation**: Uses the standard BMI formula
- **BMI Categories**: Classifies results into 4 categories:
  - Underweight (BMI < 18.5)
  - Normal (BMI 18.5 - 24.9)
  - Overweight (BMI 25 - 29.9)
  - Obese (BMI ≥ 30)
- **Visual Feedback**: Color-coded results with emojis
- **Health Recommendations**: Personalized advice for each category
- **Calculation Details**: Expandable section showing the math
- **Reference Table**: Quick view of all BMI categories
- **Responsive Design**: Clean, professional interface

## Prerequisites

- Python 3.7 or higher
- Streamlit

## Installation

Install Streamlit if you haven't already:

```bash
pip install streamlit
```

## Usage

Run the BMI Calculator:

```bash
streamlit run bmi_calculator.py
```

The app will open in your browser at `http://localhost:8501`.

## How to Use

1. **Enter your height** in centimeters (cm)
2. **Enter your weight** in kilograms (kg)
3. **Click "Calculate BMI"** button
4. View your results:
   - BMI value displayed prominently
   - Category classification with emoji
   - Health description and recommendations
   - BMI categories reference chart
   - Detailed calculation breakdown

## BMI Categories Explained

| Category | BMI Range | Health Status |
|----------|-----------|---------------|
| **Underweight** | < 18.5 | May indicate malnutrition or health issues |
| **Normal** | 18.5 - 24.9 | Healthy weight range |
| **Overweight** | 25 - 29.9 | Increased health risk |
| **Obese** | ≥ 30 | High health risk |

## Technical Details

### BMI Formula

```
BMI = Weight (kg) / Height² (m²)
```

### Example Calculation

- Height: 170 cm = 1.70 m
- Weight: 70 kg
- BMI = 70 / (1.70)² = 70 / 2.89 = 24.2 (Normal)

## Features Breakdown

### Input Validation
- Height range: 50-250 cm
- Weight range: 20-300 kg
- Step increments: 0.1 for precision

### Visual Design
- Color-coded result cards:
  - Blue border for Underweight
  - Green border for Normal
  - Orange border for Overweight
  - Red border for Obese
- Responsive two-column layout
- Custom styled blue calculate button

### Information Display
- Large BMI value (3em font)
- Category with emoji indicator
- Descriptive health message
- Personalized recommendations
- Four-column metrics for category reference
- Expandable calculation details

## Important Notes

⚠️ **Medical Disclaimer**: 
- BMI is a screening tool, not a diagnostic tool
- It doesn't measure body fat directly
- Doesn't account for:
  - Muscle mass
  - Bone density
  - Body composition
  - Age and gender differences
- Always consult healthcare professionals for personalized health advice

## Customization

You can customize the BMI categories by modifying the conditions in the script:

```python
if bmi < 18.5:
    category = "Underweight"
elif 18.5 <= bmi < 25:
    category = "Normal"
# ... and so on
```

## Screenshots Features

- Clean, professional medical-themed interface
- Real-time calculation
- Color-coded visual feedback
- Detailed metrics display
- Educational information section

## Run Command

```bash
cd Python_15_Days_Challenge/Day4
streamlit run bmi_calculator.py
```

## License

Free to use and modify for learning purposes.

---

**Challenge Completed**: Day 4 of 15 Days Python Streamlit Challenge ✅
