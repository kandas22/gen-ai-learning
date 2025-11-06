"""Example demonstrating Python data types in action."""
# Local implementations for demonstration purposes

def number_types():
    return {
        "int": 42,
        "float": 3.14,
        "complex": 2 + 3j
    }

def string_operations(text):
    return {
        "upper": text.upper(),
        "lower": text.lower(),
        "strip": text.strip(),
        "replace": text.replace("Python", "AI")
    }

def list_operations():
    lst = [1, 2, 3, 4]
    lst.append(5)
    return {
        "original": [1, 2, 3, 4],
        "appended": lst,
        "reversed": lst[::-1]
    }

def tuple_operations():
    tup = (1, 2, 3)
    return {
        "original": tup,
        "count_2": tup.count(2),
        "index_3": tup.index(3)
    }

def dict_operations():
    d = {"a": 1, "b": 2}
    d["c"] = 3
    return {
        "original": {"a": 1, "b": 2},
        "updated": d,
        "keys": list(d.keys())
    }

def set_operations():
    s = {1, 2, 3}
    s.add(4)
    return {
        "original": {1, 2, 3},
        "added": s,
        "union": s.union({5, 6})
    }

def type_conversion_examples(value):
    return {
        "to_str": str(value),
        "to_int": int(value) if isinstance(value, (str, float, bool)) and str(value).isdigit() else None,
        "to_bool": bool(value)
    }


def main():
    # Number Types
    print("Number Types:")
    print(number_types())
    print()

    # String Operations
    print("String Operations:")
    text = "  Hello Python World  "
    print(f"Operating on text: '{text}'")
    print(string_operations(text))
    print()

    # List Operations
    print("List Operations:")
    print(list_operations())
    print()

    # Tuple Operations
    print("Tuple Operations:")
    print(tuple_operations())
    print()

    # Dictionary Operations
    print("Dictionary Operations:")
    print(dict_operations())
    print()

    # Set Operations
    print("Set Operations:")
    print(set_operations())
    print()

    # Type Conversions
    print("Type Conversion Examples:")
    print("String '123':", type_conversion_examples("123"))
    print("Integer 456:", type_conversion_examples(456))
    print("Boolean True:", type_conversion_examples(True))
    print("None value:", type_conversion_examples(None))


if __name__ == "__main__":
    main()