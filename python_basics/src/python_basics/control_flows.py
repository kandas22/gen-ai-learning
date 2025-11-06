"""Python control flow examples and utility functions."""
from typing import Any, List, Dict, Optional, Union


def if_else_examples(value: Any) -> Dict[str, Any]:
    """Demonstrate if-else control flow with various conditions."""
    result = {}
    
    # Basic if-else
    if value > 0:
        result["sign"] = "positive"
    elif value < 0:
        result["sign"] = "negative"
    else:
        result["sign"] = "zero"
    
    # Multiple conditions
    if isinstance(value, (int, float)):
        if value % 2 == 0:
            result["type"] = "even number"
        else:
            result["type"] = "odd number"
    else:
        result["type"] = f"not a number, it's {type(value).__name__}"
    
    # Conditional expression (ternary operator)
    result["is_numeric"] = "numeric" if isinstance(value, (int, float)) else "non-numeric"
    
    return result


def for_loop_examples(sequence: Union[List, str, range]) -> Dict[str, Any]:
    """Demonstrate for loop variations and operations."""
    result = {
        "original": sequence,
        "iterations": [],
        "enumerated": [],
        "filtered": [],
        "transformed": []
    }
    
    # Basic for loop with collection
    for item in sequence:
        result["iterations"].append(item)
    
    # Enumerated for loop
    for index, item in enumerate(sequence):
        result["enumerated"].append(f"index {index}: {item}")
    
    # For loop with filtering
    for item in sequence:
        if isinstance(item, (int, float)) and item % 2 == 0:
            result["filtered"].append(item)
    
    # For loop with transformation
    for item in sequence:
        try:
            transformed = float(item) * 2
            result["transformed"].append(transformed)
        except (ValueError, TypeError):
            continue
    
    return result


def while_loop_examples(start: int, condition: int) -> Dict[str, List[int]]:
    """Demonstrate while loop patterns and controls."""
    result = {
        "counting": [],
        "break_example": [],
        "continue_example": []
    }
    
    # Basic while loop
    count = start
    while count <= condition:
        result["counting"].append(count)
        count += 1
    
    # While loop with break
    count = start
    while True:
        if count > condition:
            break
        result["break_example"].append(count)
        count += 1
    
    # While loop with continue
    count = start
    while count <= condition:
        count += 1
        if count % 2 == 0:  # Skip even numbers
            continue
        result["continue_example"].append(count)
    
    return result


def match_case_examples(value: Any) -> Dict[str, str]:
    """Demonstrate match-case statement (Python 3.10+)."""
    result = {}
    
    # Basic match-case
    match value:
        case int() | float():
            result["type"] = "number"
        case str():
            result["type"] = "string"
        case list():
            result["type"] = "list"
        case dict():
            result["type"] = "dictionary"
        case _:
            result["type"] = "other"
    
    # Match with patterns
    match value:
        case []:
            result["pattern"] = "empty list"
        case [x]:
            result["pattern"] = f"single item: {x}"
        case [x, y]:
            result["pattern"] = f"pair: {x}, {y}"
        case [x, *rest]:
            result["pattern"] = f"starts with {x}, followed by {len(rest)} items"
        case _:
            result["pattern"] = "not a list"
    
    return result


def exception_handling_examples(value: Any) -> Dict[str, str]:
    """Demonstrate exception handling patterns."""
    result = {}
    
    # Try-except
    try:
        result["division"] = 10 / value
    except ZeroDivisionError:
        result["division"] = "division by zero!"
    except TypeError:
        result["division"] = "invalid operand!"
    
    # Try-except-else-finally
    try:
        num = float(value)
        result["conversion"] = "conversion successful"
    except ValueError:
        result["conversion"] = "conversion failed"
    else:
        result["converted_value"] = num
    finally:
        result["process"] = "completed"
    
    # Custom exception handling
    class ValidationError(Exception):
        pass
    
    try:
        if isinstance(value, str) and not value.strip():
            raise ValidationError("Empty string!")
        result["validation"] = "valid input"
    except ValidationError as e:
        result["validation"] = str(e)
    
    return result