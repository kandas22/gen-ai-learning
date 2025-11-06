"""Python operators examples and utility functions demonstrating different operator types."""
from typing import Any, Union, List


def arithmetic_ops(a: Union[int, float], b: Union[int, float]) -> dict:
    """Demonstrate arithmetic operators.
    
    Returns a dict with results of: +, -, *, /, //, %, **
    """
    return {
        "addition": a + b,
        "subtraction": a - b,
        "multiplication": a * b,
        "division": a / b,
        "floor_division": a // b,
        "modulus": a % b,
        "power": a ** b
    }


def comparison_ops(a: Any, b: Any) -> dict:
    """Demonstrate comparison operators.
    
    Returns a dict with results of: ==, !=, <, >, <=, >=
    """
    return {
        "equal": a == b,
        "not_equal": a != b,
        "less_than": a < b,
        "greater_than": a > b,
        "less_equal": a <= b,
        "greater_equal": a >= b
    }


def logical_ops(a: bool, b: bool) -> dict:
    """Demonstrate logical operators.
    
    Returns a dict with results of: and, or, not
    """
    return {
        "and": a and b,
        "or": a or b,
        "not_a": not a,
        "not_b": not b
    }


def bitwise_ops(a: int, b: int) -> dict:
    """Demonstrate bitwise operators.
    
    Returns a dict with results of: &, |, ^, ~, <<, >>
    """
    return {
        "and": a & b,
        "or": a | b,
        "xor": a ^ b,
        "not_a": ~a,
        "left_shift": a << 1,  # Shift left by 1
        "right_shift": a >> 1  # Shift right by 1
    }


def identity_ops(a: Any, b: Any) -> dict:
    """Demonstrate identity operators.
    
    Returns a dict with results of: is, is not
    """
    return {
        "is": a is b,
        "is_not": a is not b
    }


def membership_ops(item: Any, sequence: List[Any]) -> dict:
    """Demonstrate membership operators.
    
    Returns a dict with results of: in, not in
    """
    return {
        "in": item in sequence,
        "not_in": item not in sequence
    }