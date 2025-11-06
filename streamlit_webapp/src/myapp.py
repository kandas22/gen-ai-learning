import streamlit as st

st.title("My Streamlit Web App")
st.write("Welcome to my web application built with Streamlit!")
name = st.text_input("Enter your name:", key="name")
if st.button("Say Hello", key="say_hello"):
    if name:
        st.success(f"Hello, {name}! Welcome to the app.")
    else:
        st.warning("Please enter your name.")

