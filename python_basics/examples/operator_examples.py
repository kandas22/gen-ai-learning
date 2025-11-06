"""Example demonstrating Python operators in action."""
from python_basics.operators import (
    arithmetic_ops,
    comparison_ops,
    logical_ops,
    bitwise_ops,
    membership_ops
)


def main():
    # Arithmetic operators
    print("Arithmetic Operators:")
    print(arithmetic_ops(10, 3))
    print()

    # Comparison operators
    print("Comparison Operators:")
    print(comparison_ops(5, 3))
    print()

    # Logical operators
    print("Logical Operators:")
    print(logical_ops(True, False))
    print()

    # Bitwise operators
    print("Bitwise Operators (with 60 & 13):")
    print(bitwise_ops(60, 13))
    print()

    # Membership operators
    print("Membership Operators:")
    test_list = [1, 2, 3, 4, 5]
    print(f"Testing with list {test_list}:")
    print("Testing 3:", membership_ops(3, test_list))
    print("Testing 7:", membership_ops(7, test_list))


if __name__ == "__main__":
    main()