import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Greeting Form",
    page_icon="👋",
    layout="centered"
)

# Custom CSS to make the button blue
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
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("👋 Welcome! Tell us about yourself")

# Create a form
with st.form("greeting_form"):
    st.subheader("Personal Information")
    
    # Name input
    name = st.text_input(
        "What's your name?",
        placeholder="Enter your name here...",
        help="Please enter your full name"
    )
    
    # Age slider
    age = st.slider(
        "How old are you?",
        min_value=1,
        max_value=120,
        value=25,
        help="Slide to select your age"
    )
    
    # Submit button
    submitted = st.form_submit_button("Generate Greeting", type="primary")

# Display greeting when form is submitted
if submitted:
    if name.strip():
        st.success("Form submitted successfully! ✅")
        
        # Create a personalized greeting based on age
        if age < 13:
            greeting = f"Hello, {name}! 🎈 You're a wonderful kid at {age} years old!"
        elif age < 20:
            greeting = f"Hey {name}! 🌟 Being {age} is an amazing time of life!"
        elif age < 30:
            greeting = f"Hi {name}! 🚀 Welcome! At {age}, you're in your prime!"
        elif age < 50:
            greeting = f"Hello {name}! 💼 Great to meet you at {age} years young!"
        elif age < 70:
            greeting = f"Greetings {name}! 🌺 {age} years of wisdom and counting!"
        else:
            greeting = f"Hello {name}! 👑 {age} years of incredible life experience!"
        
        # Display the greeting in a nice container
        st.markdown("---")
        st.balloons()
        st.markdown(f"### {greeting}")
        
        # Additional fun facts
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Name Length", len(name))
        with col2:
            st.metric("Your Age", f"{age} years")
        with col3:
            days_lived = age * 365
            st.metric("Days Lived", f"~{days_lived:,}")
        
    else:
        st.error("⚠️ Please enter your name before submitting!")

# Add some information at the bottom
st.markdown("---")
st.info("💡 **Tip:** Fill in your details and click 'Generate Greeting' to receive a personalized message!")
