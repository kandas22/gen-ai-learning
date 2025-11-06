# Python Basics Learning Project

A comprehensive learning project covering Python operators and data types with practical examples and test cases.

## Project Structure

```
python_basics/
│
├── src/python_basics/
│   ├── __init__.py         # Package exports
│   ├── operators.py        # Operator examples
│   └── datatypes.py        # Data type examples
│
├── examples/
│   ├── operator_examples.py   # Operator demos
│   └── datatype_examples.py   # Data type demos
│
├── tests/
│   ├── test_operators.py     # Operator tests
│   └── test_datatypes.py     # Data type tests
│
├── requirements.txt       # Project dependencies
└── README.md            # This file
```

## Topics Covered

### 1. Python Operators
- **Arithmetic:** +, -, *, /, //, %, **
- **Comparison:** ==, !=, >, <, >=, <=
- **Logical:** and, or, not
- **Bitwise:** &, |, ^, ~, <<, >>
- **Identity:** is, is not
- **Membership:** in, not in

### 2. Python Data Types
- **Numbers:** int, float, complex
- **Strings:** methods, slicing, operations
- **Lists:** mutable sequences, methods
- **Tuples:** immutable sequences
- **Dictionaries:** key-value pairs
- **Sets:** unique collections
- **Type Conversions:** between different types

### 3. Control Flow Statements
- **If-Else:** conditional branching, ternary operators
- **For Loops:** iteration, enumeration, comprehensions
- **While Loops:** conditional loops, break, continue
- **Match-Case:** pattern matching (Python 3.10+)
- **Exception Handling:** try-except-else-finally

## Step-by-Step Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/kandas22/gen-ai-learning.git
cd gen-ai-learning/python_basics
```

### 2. Set Up Python Environment
```bash
# Create a virtual environment
python -m venv .venv

# Activate the environment:
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\\Scripts\\activate
```

### 3. Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt
```

## Running the Examples

### 1. Operator Examples
```bash
# Make sure you're in the python_basics directory
cd python_basics  # if not already there

# Run operator examples
PYTHONPATH=./src python examples/operator_examples.py
```

You'll see demonstrations of:
- Arithmetic calculations (+, -, *, /, etc.)
- Comparison operations (==, !=, >, <, etc.)
- Logical operations (and, or, not)
- Bitwise operations (&, |, ^, etc.)
- Identity checks (is, is not)
- Membership tests (in, not in)

### 2. Data Type Examples
```bash
# Run data type examples
PYTHONPATH=./src python examples/datatype_examples.py
```

You'll learn about:
- Numbers (int, float, complex)
- String methods and slicing
- List operations and methods
- Tuple immutability
- Dictionary key-value operations
- Set operations
- Type conversion techniques

### 3. Control Flow Examples
```bash
# Run control flow examples
PYTHONPATH=./src python examples/control_flow_examples.py
```

This demonstrates:
- If-else conditional branching
- For loops with enumeration and filtering
- While loops with break/continue
- Match-case pattern matching
- Exception handling patterns

## Running and Testing

### Step 1: Run Individual Examples

1. **Operator Examples**
   ```bash
   PYTHONPATH=./src python examples/operator_examples.py
   ```

2. **Data Type Examples**
   ```bash
   PYTHONPATH=./src python examples/datatype_examples.py
   ```

3. **Control Flow Examples**
   ```bash
   PYTHONPATH=./src python examples/control_flow_examples.py
   ```

### Step 2: Run Tests

1. **Run All Tests**
   ```bash
   # Test everything
   PYTHONPATH=./src pytest -v tests/
   ```

2. **Run Topic-Specific Tests**
   ```bash
   # Test operators
   PYTHONPATH=./src pytest -v tests/test_operators.py

   # Test data types
   PYTHONPATH=./src pytest -v tests/test_datatypes.py

   # Test control flows
   PYTHONPATH=./src pytest -v tests/test_control_flows.py
   ```

### Step 3: Check Test Coverage

1. **Basic Coverage Report**
   ```bash
   PYTHONPATH=./src pytest -v --cov=python_basics tests/
   ```

2. **Detailed Coverage Analysis**
   ```bash
   # Show line-by-line coverage
   PYTHONPATH=./src pytest -v --cov=python_basics --cov-report=term-missing tests/

   # Generate HTML coverage report
   PYTHONPATH=./src pytest -v --cov=python_basics --cov-report=html tests/
   ```

## Quick Code Examples

### 1. Operators
```python
from python_basics.operators import arithmetic_ops, logical_ops

# Arithmetic operations
print(arithmetic_ops(10, 3))
# Output: {'addition': 13, 'subtraction': 7, 'multiplication': 30, ...}

# Logical operations
print(logical_ops(True, False))
# Output: {'and': False, 'or': True, 'not_a': False, 'not_b': True}
```

### 2. Data Types
```python
from python_basics.datatypes import string_operations, list_operations

# String operations
print(string_operations("Hello Python"))
# Output: {'length': 11, 'upper': 'HELLO PYTHON', 'lower': 'hello python', ...}

# List operations
print(list_operations())
# Output: {'original': [1, 2, 3, 4, 5], 'reversed': [5, 4, 3, 2, 1], ...}
```

### 3. Control Flows
```python
from python_basics.control_flows import if_else_examples, for_loop_examples

# Conditional logic
print(if_else_examples(42))
# Output: {'sign': 'positive', 'type': 'even number', 'is_numeric': 'numeric'}

# Loop operations
print(for_loop_examples([1, 2, 3, 4]))
# Output: {'iterations': [1, 2, 3, 4], 'filtered': [2, 4], ...}
```

## Development Guidelines

### Project Organization
- Source code is in `src/python_basics/`
- Examples are in `examples/`
- Tests are in `tests/`
- All functions include type hints
- Comprehensive docstrings

### Code Style
- Follow PEP 8 guidelines
- Use type hints for better code understanding
- Write descriptive docstrings
- Include examples in docstrings

### Testing
- Write tests for new features
- Maintain high test coverage
- Run tests before commits
- Include edge cases in tests

## Troubleshooting

### Common Issues
1. **Import Errors**
   - Ensure PYTHONPATH is set correctly
   - Verify virtual environment is activated
   - Check file locations match import statements

2. **Test Failures**
   - Update dependencies
   - Check Python version compatibility
   - Verify file paths in tests

3. **Coverage Issues**
   - Install pytest-cov package
   - Run from correct directory
   - Check package names in coverage command

## Requirements

- Python 3.6+
- pytest==7.4.3
- pytest-cov==4.1.0

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure everything works
5. Submit a pull request

