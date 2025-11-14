import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="BMI Calculator",
    page_icon="⚕️",
    layout="centered"
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
    .bmi-card {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 20px 0;
    }
    .underweight {
        background-color: #E3F2FD;
        border: 2px solid #2196F3;
    }
    .normal {
        background-color: #E8F5E9;
        border: 2px solid #4CAF50;
    }
    .overweight {
        background-color: #FFF3E0;
        border: 2px solid #FF9800;
    }
    .obese {
        background-color: #FFEBEE;
        border: 2px solid #F44336;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("⚕️ BMI Calculator")
st.markdown("### Calculate Your Body Mass Index")
st.markdown("---")

# Create columns for better layout
col1, col2 = st.columns(2)

with col1:
    # Height input
    height = st.number_input(
        "Height (cm)",
        min_value=50.0,
        max_value=250.0,
        value=170.0,
        step=0.1,
        help="Enter your height in centimeters"
    )

with col2:
    # Weight input
    weight = st.number_input(
        "Weight (kg)",
        min_value=20.0,
        max_value=300.0,
        value=70.0,
        step=0.1,
        help="Enter your weight in kilograms"
    )

# Calculate button
if st.button("Calculate BMI", type="primary"):
    # Convert height from cm to meters
    height_m = height / 100
    
    # Calculate BMI
    bmi = weight / (height_m ** 2)
    
    # Determine BMI category
    if bmi < 18.5:
        category = "Underweight"
        color_class = "underweight"
        emoji = "😟"
        description = "You may need to gain some weight. Consult a healthcare professional."
        recommendation = "Consider a balanced diet with adequate calories and nutrients."
    elif 18.5 <= bmi < 25:
        category = "Normal"
        color_class = "normal"
        emoji = "😊"
        description = "You have a healthy weight. Keep up the good work!"
        recommendation = "Maintain your current lifestyle with balanced diet and regular exercise."
    elif 25 <= bmi < 30:
        category = "Overweight"
        color_class = "overweight"
        emoji = "😐"
        description = "You may want to consider losing some weight."
        recommendation = "Try incorporating more physical activity and a balanced diet."
    else:
        category = "Obese"
        color_class = "obese"
        emoji = "😟"
        description = "You should consider consulting a healthcare professional."
        recommendation = "Seek professional guidance for a healthy weight loss plan."
    
    # Display results
    st.markdown("---")
    st.markdown("## Your Results")
    
    # BMI Value in large text
    st.markdown(f"""
        <div class='bmi-card {color_class}'>
            <h1 style='margin: 0; font-size: 3em;'>{bmi:.1f}</h1>
            <h2 style='margin: 10px 0;'>{emoji} {category}</h2>
            <p style='margin: 5px 0; font-size: 1.1em;'>{description}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Additional information
    st.markdown("### 💡 Recommendation")
    st.info(recommendation)
    
    # BMI Categories Reference
    st.markdown("### 📊 BMI Categories")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Underweight", "< 18.5", delta="Low" if category == "Underweight" else None)
    with col2:
        st.metric("Normal", "18.5 - 24.9", delta="Healthy" if category == "Normal" else None)
    with col3:
        st.metric("Overweight", "25 - 29.9", delta="High" if category == "Overweight" else None)
    with col4:
        st.metric("Obese", "≥ 30", delta="Very High" if category == "Obese" else None)
    
    # Show calculation details
    with st.expander("📐 Calculation Details"):
        st.write(f"**Height:** {height} cm = {height_m:.2f} m")
        st.write(f"**Weight:** {weight} kg")
        st.write(f"**Formula:** BMI = Weight (kg) / Height² (m²)")
        st.write(f"**Calculation:** {weight} / ({height_m:.2f})² = {bmi:.2f}")

# Information section
st.markdown("---")
st.markdown("### ℹ️ About BMI")
st.markdown("""
Body Mass Index (BMI) is a measure of body fat based on height and weight. 
It's a screening tool that can indicate whether a person is underweight, at a healthy weight, 
overweight, or obese.

**Note:** BMI is a useful indicator but doesn't directly measure body fat. 
Factors like muscle mass, bone density, and overall body composition aren't considered.
Always consult healthcare professionals for personalized health advice.
""")
