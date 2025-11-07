# Test Suite for Patient Profile Management App

Comprehensive test coverage for the Streamlit healthcare patient management application.

## 📊 Test Coverage

### Test Classes and Scenarios

#### 1. **TestDatabaseOperations** (2 tests)
Tests database initialization and schema:
- ✅ Table creation
- ✅ Column verification

#### 2. **TestPatientCRUD** (12 tests)
Tests Create, Read, Update, Delete operations:
- ✅ Insert patient with all fields
- ✅ Insert patient without optional email
- ✅ Whitespace trimming on insert
- ✅ Fetch patient by ID
- ✅ Handle nonexistent patient
- ✅ Fetch all patients
- ✅ Update patient information
- ✅ Remove email on update
- ✅ Delete patient
- ✅ Delete nonexistent patient (no error)

#### 3. **TestValidation** (11 tests)
Tests input validation logic:

**Phone Validation:**
- ✅ Valid simple phone numbers
- ✅ Phone numbers with formatting (+, -, spaces, parentheses)
- ✅ Too short (< 7 digits)
- ✅ Too long (> 15 digits)
- ✅ Empty phone
- ✅ Non-numeric input

**Email Validation:**
- ✅ Valid email formats
- ✅ Empty email (optional field)
- ✅ Invalid email formats

#### 4. **TestUtilityFunctions** (2 tests)
Tests helper functions:
- ✅ DataFrame to CSV conversion
- ✅ Empty DataFrame handling

#### 5. **TestIntegration** (3 tests)
Tests complete workflows:
- ✅ Full patient lifecycle (create → read → update → delete)
- ✅ Multiple patients with ordering
- ✅ Search/filter scenarios

#### 6. **TestEdgeCases** (4 tests)
Tests boundary conditions:
- ✅ Very long names (100 characters)
- ✅ Special characters (O'Brien, Smith-Jones, +1 (555) format)
- ✅ Unicode/international characters (José, Müller, München)
- ✅ Operations on empty database

## 🚀 Running Tests

### Prerequisites

Ensure virtual environment is activated and dependencies are installed:

```bash
cd /Users/kanda/Learning/GenAI/gen-ai-learning/streamlit_assignment
source .venv/bin/activate
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest tests/test_kavihealthcare.py -v
```

**Expected output:**
```
30 passed in 0.30s
```

### Run Specific Test Class

```bash
# Run only validation tests
pytest tests/test_kavihealthcare.py::TestValidation -v

# Run only CRUD tests
pytest tests/test_kavihealthcare.py::TestPatientCRUD -v

# Run only edge case tests
pytest tests/test_kavihealthcare.py::TestEdgeCases -v
```

### Run Specific Test

```bash
# Run a single test
pytest tests/test_kavihealthcare.py::TestPatientCRUD::test_insert_patient_basic -v
```

### Run with Coverage Report

```bash
# Generate coverage report
pytest tests/test_kavihealthcare.py --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Run with Detailed Output

```bash
# Show print statements and detailed failures
pytest tests/test_kavihealthcare.py -v -s
```

## 📁 Project Structure

```
streamlit_assignment/
│
├── src/
│   └── kavihealthcare.py       # Main application
│
├── tests/
│   └── test_kavihealthcare.py  # Test suite (30 tests)
│
├── requirements.txt             # Dependencies (includes pytest)
├── .venv/                      # Virtual environment
└── README_TESTS.md             # This file
```

## 🔧 Test Configuration

### Dependencies

Tests require:
- `pytest==8.4.2` - Testing framework
- `pytest-cov==7.0.0` - Coverage reporting
- All app dependencies (pandas, streamlit, validators)

### Test Database

Tests use temporary SQLite databases:
- Created automatically for each test
- Isolated between tests
- Cleaned up after each test
- No impact on production database

### Fixtures

The test suite uses pytest fixtures:

```python
@pytest.fixture
def temp_db():
    """Creates isolated temporary database for each test"""
    
@pytest.fixture
def sample_patient_data():
    """Provides consistent test data"""
```

## ✅ Test Results Summary

| Test Category | Tests | Status |
|--------------|-------|--------|
| Database Operations | 2 | ✅ All Pass |
| CRUD Operations | 12 | ✅ All Pass |
| Validation | 11 | ✅ All Pass |
| Utilities | 2 | ✅ All Pass |
| Integration | 3 | ✅ All Pass |
| Edge Cases | 4 | ✅ All Pass |
| **TOTAL** | **30** | **✅ All Pass** |

## 🐛 Debugging Failed Tests

If a test fails:

1. **Run with verbose output:**
   ```bash
   pytest tests/test_kavihealthcare.py::TestName::test_name -v -s
   ```

2. **Check the error message** - pytest provides detailed tracebacks

3. **Verify database state** - tests use isolated temp databases

4. **Check validation logic** - ensure phone/email validation rules match

## 📝 Adding New Tests

To add new tests:

1. **Choose the appropriate test class** or create a new one

2. **Follow the naming convention:**
   ```python
   def test_description_of_what_is_tested(self, fixtures):
       """Docstring explaining the test purpose"""
       # Arrange
       # Act
       # Assert
   ```

3. **Use fixtures** for database and test data

4. **Add assertions** to verify expected behavior

5. **Run the test** to ensure it works:
   ```bash
   pytest tests/test_kavihealthcare.py::TestClass::test_new_test -v
   ```

## 🎯 Testing Best Practices Used

✅ **Isolation** - Each test uses its own temporary database  
✅ **Clarity** - Descriptive test names and docstrings  
✅ **Coverage** - Tests cover happy paths, edge cases, and error handling  
✅ **Fixtures** - Reusable test data and setup  
✅ **Assertions** - Clear, specific assertions  
✅ **Cleanup** - Automatic cleanup of temporary resources  

## 🔍 What's NOT Tested

The following are not covered by unit tests:
- **Streamlit UI** - Requires browser automation (Selenium/Playwright)
- **User interactions** - Button clicks, form submissions
- **Session state** - Streamlit's session management
- **Visual rendering** - Layout and display

For UI testing, consider:
- Manual testing
- Streamlit's testing framework (when available)
- End-to-end testing with Selenium

## 📚 Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)

## 🤝 Contributing

When adding new features to the app:

1. Write tests first (TDD approach)
2. Ensure all existing tests pass
3. Add tests for new functionality
4. Maintain test coverage above 80%

## 📞 Support

If tests fail unexpectedly:
1. Verify virtual environment is activated
2. Ensure all dependencies are installed
3. Check for conflicting database files
4. Review test output for specific error messages

---

**Test Suite Version:** 1.0  
**Last Updated:** 7 November 2025  
**Total Tests:** 30  
**Test Status:** ✅ All Passing
