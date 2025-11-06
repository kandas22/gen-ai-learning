import streamlit as st

st.title('Simple Calculator')

# Input fields for two numbers
num1 = st.number_input('Enter first number:', value=0.0, key="num1")
num2 = st.number_input('Enter second number:', value=0.0, key="num2")

# Operation selection
operation = st.selectbox(
    'Select operation:',
    ('Addition', 'Subtraction', 'Multiplication', 'Division'),
    key="operation")

# Calculate button
if st.button('Calculate', key="calculate"):
    if operation == 'Addition':
        result = num1 + num2
        st.success(f'{num1} + {num2} = {result}')
    elif operation == 'Subtraction':
        result = num1 - num2
        st.success(f'{num1} - {num2} = {result}')
    elif operation == 'Multiplication':
        result = num1 * num2
        st.success(f'{num1} × {num2} = {result}')
    elif operation == 'Division':
        if num2 != 0:
            result = num1 / num2
            st.success(f'{num1} ÷ {num2} = {result}')
        else:
            st.error('Error: Division by zero!')

# Add some usage instructions
st.markdown('---')
st.markdown('''
### How to use:
1. Enter the first number
2. Enter the second number
3. Select the desired operation
4. Click "Calculate" to see the result
''')

# Add some styling
st.markdown('''
<style>
div.stButton > button {
    width: 100%;
    background-color: #4CAF50;
    color: white;
}
div.stButton > button:hover {
    background-color: #45a049;
}
</style>
''', unsafe_allow_html=True)
