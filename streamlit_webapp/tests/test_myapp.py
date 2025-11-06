import pytest
from streamlit.testing.v1 import AppTest
import sys
import os

# Add the parent directory to the Python path so we can import the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_myapp_initial_state():
    """Test the initial state of the app"""
    at = AppTest.from_file(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "myapp.py"))
    at.run()
    
    # Check title and welcome message
    assert "My Streamlit Web App" in at.title[0].value
    assert "Welcome to my web application built with Streamlit!" in at.markdown[0].value

def test_myapp_empty_name_warning():
    """Test warning message when no name is entered"""
    at = AppTest.from_file(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "myapp.py"))
    at.run()
    
    # Find button widget by key and click it
    at.button(key="say_hello").click()
    at.run()
    
    # Check if warning message is displayed
    assert "Please enter your name." in at.warning[0].value

def test_myapp_greeting():
    """Test greeting message with name input"""
    at = AppTest.from_file(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "myapp.py"))
    at.run()
    
    # Set the name value and click the button
    at.text_input(key="name").input("John").run()
    at.button(key="say_hello").click()
    at.run()
    
    # Check if greeting message is displayed
    assert "Hello, John! Welcome to the app." in at.success[0].value