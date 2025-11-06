"""Python data types examples and utility functions."""
from typing import Any, List, Dict, Set, Tuple, Union, Optional


def number_types() -> Dict[str, Union[int, float, complex]]:
    """Demonstrate different number types in Python."""
    return {
        "integer": 42,
        "float": 3.14159,
        "complex": complex(1, 2),  # 1 + 2j
        "negative": -17,
        "zero": 0,
    }


def string_operations(text: str) -> Dict[str, Any]:
    """Demonstrate string operations and methods."""
    return {
        "length": len(text),
        "upper": text.upper(),
        "lower": text.lower(),
        "capitalized": text.capitalize(),
        "stripped": text.strip(),
        "split_words": text.split(),
        "replaced": text.replace("a", "@"),
        "slice_first_3": text[:3],
        "slice_last_3": text[-3:],
    }


def list_operations() -> Dict[str, List[Any]]:
    """Demonstrate list operations and methods."""
    numbers = [1, 2, 3, 4, 5]
    mixed_list = [1, "hello", 3.14, True]
    
    # Demonstrate list methods
    numbers_copy = numbers.copy()
    numbers_copy.append(6)
    numbers_copy.extend([7, 8])
    
    return {
        "original": numbers,
        "mixed_types": mixed_list,
        "appended": numbers_copy,
        "sliced": numbers[1:4],
        "reversed": numbers[::-1],
        "sorted_desc": sorted(numbers, reverse=True),
    }


def tuple_operations() -> Dict[str, Any]:
    """Demonstrate tuple operations."""
    point = (3, 4)
    rgb = (255, 128, 0)
    
    return {
        "point": point,
        "rgb": rgb,
        "nested": (point, rgb),
        "concatenated": point + rgb,
        "repeated": point * 2,
        "x_coordinate": point[0],
        "y_coordinate": point[1],
    }


def dict_operations() -> Dict[str, Any]:
    """Demonstrate dictionary operations."""
    user = {
        "name": "Alice",
        "age": 30,
        "skills": ["Python", "JavaScript"]
    }
    
    # Create a copy for modification
    user_copy = user.copy()
    user_copy["location"] = "New York"
    
    return {
        "original": user,
        "keys": list(user.keys()),
        "values": list(user.values()),
        "items": list(user.items()),
        "modified": user_copy,
        "get_default": user.get("email", "not found"),
    }


def set_operations() -> Dict[str, Any]:
    """Demonstrate set operations."""
    set_a = {1, 2, 3, 4}
    set_b = {3, 4, 5, 6}
    
    return {
        "set_a": set_a,
        "set_b": set_b,
        "union": set_a | set_b,
        "intersection": set_a & set_b,
        "difference": set_a - set_b,
        "symmetric_diff": set_a ^ set_b,
    }


def type_conversion_examples(value: Any) -> Dict[str, Any]:
    """Demonstrate type conversion operations."""
    try:
        return {
            "to_int": int(value) if value is not None else None,
            "to_float": float(value) if value is not None else None,
            "to_str": str(value),
            "to_bool": bool(value),
            "to_list": list(value) if hasattr(value, "__iter__") else [value],
            "original_type": type(value).__name__
        }
    except (ValueError, TypeError):
        return {
            "error": f"Cannot convert {value} to all types",
            "original_type": type(value).__name__
        }