"""python_basics package.

Expose modules for learning examples.
"""

from .operators import (
    arithmetic_ops,
    comparison_ops,
    logical_ops,
    bitwise_ops,
    identity_ops,
    membership_ops
)

from .datatypes import (
    number_types,
    string_operations,
    list_operations,
    tuple_operations,
    dict_operations,
    set_operations,
    type_conversion_examples
)

from .control_flows import (
    if_else_examples,
    for_loop_examples,
    while_loop_examples,
    match_case_examples,
    exception_handling_examples
)

__all__ = [
    # Operators
    "arithmetic_ops",
    "comparison_ops", 
    "logical_ops",
    "bitwise_ops",
    "identity_ops",
    "membership_ops",
    
    # Data Types
    "number_types",
    "string_operations",
    "list_operations",
    "tuple_operations",
    "dict_operations",
    "set_operations",
    "type_conversion_examples",
    
    # Control Flows
    "if_else_examples",
    "for_loop_examples",
    "while_loop_examples",
    "match_case_examples",
    "exception_handling_examples"
    "membership_ops"
]