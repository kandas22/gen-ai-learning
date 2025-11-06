import pytest
from streamlit.testing.v1 import AppTest
import sys
import os

# Add the parent directory to the Python path so we can import the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_calculator_addition():
    """Test the calculator's addition functionality"""
    at = AppTest.from_file(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "calculator.py"))
    at.run()
    
    # Set input values using keys
    at.number_input(key="num1").set_value(5.0)
    at.number_input(key="num2").set_value(3.0)
    at.selectbox(key="operation").set_value("Addition")
    at.button(key="calculate").click()
    at.run()
    
    # Check if result is displayed correctly
    assert "5.0 + 3.0 = 8.0" in at.success[0].value

def test_calculator_division():
    """Test the calculator's division functionality"""
    at = AppTest.from_file(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "calculator.py"))
    at.run()
    
    # Test normal division
    at.number_input(key="num1").set_value(10.0)
    at.number_input(key="num2").set_value(2.0)
    at.selectbox(key="operation").set_value("Division")
    at.button(key="calculate").click()
    at.run()
    
    # Check if result is displayed correctly
    assert "10.0 ÷ 2.0 = 5.0" in at.success[0].value

def test_calculator_division_by_zero():
    """Test division by zero error handling"""
    at = AppTest.from_file(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "calculator.py"))
    at.run()
    
    # Test division by zero
    at.number_input(key="num1").set_value(10.0)
    at.number_input(key="num2").set_value(0.0)
    at.selectbox(key="operation").set_value("Division")
    at.button(key="calculate").click()
    at.run()
    
    # Check if error message is displayed
    assert "Error: Division by zero!" in at.error[0].value

def test_calculator_multiplication():
    """Test the calculator's multiplication functionality"""
    at = AppTest.from_file(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "calculator.py"))
    at.run()
    
    at.number_input(key="num1").set_value(4.0)
    at.number_input(key="num2").set_value(3.0)
    at.selectbox(key="operation").set_value("Multiplication")
    at.button(key="calculate").click()
    at.run()
    
    assert "4.0 × 3.0 = 12.0" in at.success[0].value

def test_calculator_subtraction():
    """Test the calculator's subtraction functionality"""
    at = AppTest.from_file(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "calculator.py"))
    at.run()
    
    at.number_input(key="num1").set_value(7.0)
    at.number_input(key="num2").set_value(3.0)
    at.selectbox(key="operation").set_value("Subtraction")
    at.button(key="calculate").click()
    at.run()
    
    assert "7.0 - 3.0 = 4.0" in at.success[0].value