"""Test cases for Python control flow examples."""
import pytest
from python_basics.control_flows import (
    if_else_examples,
    for_loop_examples,
    while_loop_examples,
    match_case_examples,
    exception_handling_examples
)


def test_if_else_examples():
    # Test with positive number
    result = if_else_examples(5)
    assert result["sign"] == "positive"
    assert result["type"] == "odd number"
    assert result["is_numeric"] == "numeric"
    
    # Test with negative number
    result = if_else_examples(-2)
    assert result["sign"] == "negative"
    assert result["type"] == "even number"
    
    # Test with zero
    result = if_else_examples(0)
    assert result["sign"] == "zero"
    assert result["type"] == "even number"
    
    # Test with non-numeric
    result = if_else_examples("test")
    assert result["type"] == "not a number, it's str"
    assert result["is_numeric"] == "non-numeric"


def test_for_loop_examples():
    # Test with list of numbers
    result = for_loop_examples([1, 2, 3, 4])
    assert result["iterations"] == [1, 2, 3, 4]
    assert "index 0: 1" in result["enumerated"]
    assert result["filtered"] == [2, 4]  # Even numbers
    assert result["transformed"] == [2.0, 4.0, 6.0, 8.0]
    
    # Test with string
    result = for_loop_examples("abc")
    assert result["iterations"] == ['a', 'b', 'c']
    assert "index 1: b" in result["enumerated"]
    
    # Test with range
    result = for_loop_examples(range(3))
    assert result["iterations"] == [0, 1, 2]
    assert result["filtered"] == [0, 2]  # Even numbers


def test_while_loop_examples():
    result = while_loop_examples(1, 5)
    
    assert result["counting"] == [1, 2, 3, 4, 5]
    assert result["break_example"] == [1, 2, 3, 4, 5]
    assert result["continue_example"] == [1, 3, 5]  # Odd numbers
    
    # Test with zero iterations
    result = while_loop_examples(5, 1)
    assert result["counting"] == []
    assert result["break_example"] == []


def test_match_case_examples():
    # Test with different types
    assert match_case_examples(42)["type"] == "number"
    assert match_case_examples("hello")["type"] == "string"
    assert match_case_examples([1, 2])["type"] == "list"
    assert match_case_examples({})["type"] == "dictionary"
    
    # Test list patterns
    assert match_case_examples([])["pattern"] == "empty list"
    assert match_case_examples([1])["pattern"] == "single item: 1"
    assert match_case_examples([1, 2])["pattern"] == "pair: 1, 2"
    assert "starts with" in match_case_examples([1, 2, 3])["pattern"]


def test_exception_handling_examples():
    # Test normal division
    result = exception_handling_examples(2)
    assert result["division"] == 5.0  # 10/2
    assert result["conversion"] == "conversion successful"
    assert result["converted_value"] == 2.0
    
    # Test division by zero
    result = exception_handling_examples(0)
    assert result["division"] == "division by zero!"
    
    # Test invalid conversion
    result = exception_handling_examples("abc")
    assert result["conversion"] == "conversion failed"
    
    # Test empty string validation
    result = exception_handling_examples("   ")
    assert result["validation"] == "Empty string!"
    
    # Test valid string
    result = exception_handling_examples("valid")
    assert result["validation"] == "valid input"