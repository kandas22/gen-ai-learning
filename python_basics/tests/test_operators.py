"""Test cases for Python operators examples."""
import pytest
from python_basics.operators import (
    arithmetic_ops,
    comparison_ops,
    logical_ops,
    bitwise_ops,
    identity_ops,
    membership_ops
)


def test_arithmetic_operators():
    # Test with integers
    results = arithmetic_ops(10, 3)
    assert results["addition"] == 13
    assert results["subtraction"] == 7
    assert results["multiplication"] == 30
    assert results["division"] == pytest.approx(3.3333333)
    assert results["floor_division"] == 3
    assert results["modulus"] == 1
    assert results["power"] == 1000

    # Test with floats
    results = arithmetic_ops(5.0, 2.0)
    assert results["addition"] == 7.0
    assert results["power"] == 25.0


def test_comparison_operators():
    # Test with numbers
    results = comparison_ops(5, 3)
    assert results["equal"] is False
    assert results["not_equal"] is True
    assert results["less_than"] is False
    assert results["greater_than"] is True
    assert results["less_equal"] is False
    assert results["greater_equal"] is True

    # Test with equal values
    results = comparison_ops(5, 5)
    assert results["equal"] is True
    assert results["less_equal"] is True
    assert results["greater_equal"] is True


def test_logical_operators():
    # Test all combinations
    assert logical_ops(True, True)["and"] is True
    assert logical_ops(True, False)["and"] is False
    assert logical_ops(True, False)["or"] is True
    assert logical_ops(False, False)["or"] is False
    
    results = logical_ops(True, False)
    assert results["not_a"] is False
    assert results["not_b"] is True


def test_bitwise_operators():
    # Test with binary numbers
    results = bitwise_ops(60, 13)
    assert results["and"] == 12  # 60 & 13 = 12
    assert results["or"] == 61   # 60 | 13 = 61
    assert results["xor"] == 49  # 60 ^ 13 = 49
    
    # Test shifts
    results = bitwise_ops(8, 0)  # Second argument not used for shifts
    assert results["left_shift"] == 16   # 8 << 1 = 16
    assert results["right_shift"] == 4   # 8 >> 1 = 4


def test_identity_operators():
    # Test with same object
    x = [1, 2, 3]
    y = x  # Same object
    results = identity_ops(x, y)
    assert results["is"] is True
    assert results["is_not"] is False

    # Test with different objects but same value
    y = [1, 2, 3]  # Different object
    results = identity_ops(x, y)
    assert results["is"] is False
    assert results["is_not"] is True


def test_membership_operators():
    test_list = [1, 2, 3, 4, 5]
    
    # Test with element in list
    results = membership_ops(3, test_list)
    assert results["in"] is True
    assert results["not_in"] is False
    
    # Test with element not in list
    results = membership_ops(6, test_list)
    assert results["in"] is False
    assert results["not_in"] is True

    # Test with string
    results = membership_ops('h', "hello")
    assert results["in"] is True
    assert results["not_in"] is False