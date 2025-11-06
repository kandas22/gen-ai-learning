"""Example demonstrating Python control flows in action."""
from python_basics.control_flows import (
    if_else_examples,
    for_loop_examples,
    while_loop_examples,
    match_case_examples,
    exception_handling_examples
)


def main():
    # If-else examples
    print("\nIf-Else Examples:")
    print("Testing with number 5:", if_else_examples(5))
    print("Testing with string 'hello':", if_else_examples("hello"))
    
    # For loop examples
    print("\nFor Loop Examples:")
    numbers = [1, 2, 3, 4, 5]
    print(f"Testing with {numbers}:")
    result = for_loop_examples(numbers)
    print("Iterations:", result["iterations"])
    print("Enumerated:", result["enumerated"])
    print("Filtered (even numbers):", result["filtered"])
    print("Transformed (doubled):", result["transformed"])
    
    # While loop examples
    print("\nWhile Loop Examples:")
    result = while_loop_examples(1, 5)
    print("Basic counting:", result["counting"])
    print("With break:", result["break_example"])
    print("With continue (odd numbers):", result["continue_example"])
    
    # Match-case examples
    print("\nMatch-Case Examples:")
    test_values = [42, "hello", [1, 2], [], [1], {"name": "test"}]
    for value in test_values:
        result = match_case_examples(value)
        print(f"Testing {value!r}:", result)
    
    # Exception handling examples
    print("\nException Handling Examples:")
    test_values = [2, 0, "invalid", "  ", "valid"]
    for value in test_values:
        result = exception_handling_examples(value)
        print(f"Testing {value!r}:", result)


if __name__ == "__main__":
    main()