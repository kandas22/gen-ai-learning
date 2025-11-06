"""Test cases for Python data types examples."""
import pytest
from python_basics.datatypes import (
    number_types,
    string_operations,
    list_operations,
    tuple_operations,
    dict_operations,
    set_operations,
    type_conversion_examples
)


def test_number_types():
    numbers = number_types()
    
    assert isinstance(numbers["integer"], int)
    assert isinstance(numbers["float"], float)
    assert isinstance(numbers["complex"], complex)
    
    assert numbers["integer"] == 42
    assert numbers["float"] == pytest.approx(3.14159)
    assert numbers["complex"] == complex(1, 2)
    assert numbers["negative"] == -17
    assert numbers["zero"] == 0


def test_string_operations():
    result = string_operations("  Hello World  ")
    
    assert result["length"] == 13
    assert result["upper"] == "  HELLO WORLD  "
    assert result["lower"] == "  hello world  "
    assert result["capitalized"] == "  hello world  "
    assert result["stripped"] == "Hello World"
    assert result["split_words"] == ["Hello", "World"]
    
    # Test with different string
    result = string_operations("banana")
    assert result["replaced"] == "b@n@n@"
    assert result["slice_first_3"] == "ban"
    assert result["slice_last_3"] == "ana"


def test_list_operations():
    result = list_operations()
    
    assert result["original"] == [1, 2, 3, 4, 5]
    assert len(result["mixed_types"]) == 4
    assert isinstance(result["mixed_types"][1], str)
    
    # Test list modifications
    assert result["appended"][-1] == 8
    assert result["sliced"] == [2, 3, 4]
    assert result["reversed"] == [5, 4, 3, 2, 1]
    assert result["sorted_desc"] == [5, 4, 3, 2, 1]


def test_tuple_operations():
    result = tuple_operations()
    
    assert result["point"] == (3, 4)
    assert result["rgb"] == (255, 128, 0)
    assert result["nested"] == ((3, 4), (255, 128, 0))
    assert result["concatenated"] == (3, 4, 255, 128, 0)
    assert result["repeated"] == (3, 4, 3, 4)
    assert result["x_coordinate"] == 3
    assert result["y_coordinate"] == 4


def test_dict_operations():
    result = dict_operations()
    original = result["original"]
    
    assert original["name"] == "Alice"
    assert original["age"] == 30
    assert "Python" in original["skills"]
    
    assert "name" in result["keys"]
    assert "Alice" in result["values"]
    assert ("name", "Alice") in result["items"]
    
    assert result["modified"]["location"] == "New York"
    assert result["get_default"] == "not found"


def test_set_operations():
    result = set_operations()
    
    assert result["set_a"] == {1, 2, 3, 4}
    assert result["set_b"] == {3, 4, 5, 6}
    assert result["union"] == {1, 2, 3, 4, 5, 6}
    assert result["intersection"] == {3, 4}
    assert result["difference"] == {1, 2}
    assert result["symmetric_diff"] == {1, 2, 5, 6}


def test_type_conversion():
    # Test string conversion
    str_result = type_conversion_examples("123")
    assert str_result["to_int"] == 123
    assert str_result["to_float"] == 123.0
    assert str_result["to_bool"] is True
    
    # Test number conversion
    num_result = type_conversion_examples(123)
    assert num_result["to_str"] == "123"
    assert num_result["to_list"] == [123]
    
    # Test bool conversion
    bool_result = type_conversion_examples(True)
    assert bool_result["to_int"] == 1
    assert bool_result["to_str"] == "True"
    
    # Test None handling
    none_result = type_conversion_examples(None)
    assert none_result["to_int"] is None
    assert none_result["to_float"] is None
    assert none_result["to_str"] == "None"
    assert none_result["to_bool"] is False