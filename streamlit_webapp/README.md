# Streamlit Web Applications

This repository contains two Streamlit web applications:
1. Simple Hello World App (`src/myapp.py`)
2. Calculator App (`src/calculator.py`)

## Project Structure

```
streamlit_webapp/
│
├── src/
│   ├── myapp.py        # Hello World application
│   └── calculator.py   # Calculator application
│
├── tests/
│   ├── test_myapp.py
│   └── test_calculator.py
│
├── requirements.txt    # Project dependencies
└── README.md          # This file
```

## Setup Instructions

### 1. Setting up Virtual Environment

```bash
# Navigate to the project directory
cd streamlit_webapp

# Create a new virtual environment
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Running the Applications

#### Hello World App
```bash
# Make sure your virtual environment is activated
streamlit run src/myapp.py
```
This will launch a simple greeting application that:
- Displays a title "Hello World"
- Shows a greeting message
- Has a text input for your name
- Updates the greeting when you enter your name

#### Calculator App
```bash
# Make sure your virtual environment is activated
streamlit run src/calculator.py
```

The calculator application provides:
- Input fields for two numbers
- Selection of basic arithmetic operations:
  - Addition (+)
  - Subtraction (-)
  - Multiplication (×)
  - Division (÷)
- A "Calculate" button to perform the operation
- Clear display of results
- Error handling for division by zero

### 3. Running Tests

To run the tests for both applications:

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_calculator.py
pytest tests/test_myapp.py

# Run tests with verbose output
pytest -v tests/
```

## Dependencies

The main dependencies for this project are:
- streamlit==1.28.1
- pytest==7.4.3
- pytest-asyncio==0.21.1

All dependencies are listed in `requirements.txt`

## Troubleshooting

1. If you see import errors:
   - Make sure your virtual environment is activated
   - Verify all dependencies are installed: `pip list`
   - Check if you're in the correct directory

2. If Streamlit fails to start:
   - Check if port 8501 is already in use
   - Try running with a different port: `streamlit run src/myapp.py --server.port 8502`

3. If tests fail:
   - Ensure you're using the virtual environment's Python
   - Verify the correct path to the source files
   - Check if all widget keys are properly set in the Streamlit apps

## Development Notes

- All interactive elements in the apps have unique keys for testing purposes
- The calculator handles division by zero gracefully
- Test files use Streamlit's testing API (streamlit.testing.v1)
- Both apps include basic styling and user instructions

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a new branch for your feature
3. Add your changes
4. Write or update tests as needed
5. Submit a pull request

Remember to run tests before submitting changes:
```bash
pytest tests/
```