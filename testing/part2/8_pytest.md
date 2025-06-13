# Unit Testing with pytest

### pytest vs unittest
```python
# unittest (built-in)
import unittest

class TestCalculator(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(2 + 2, 4)
        
    def setUp(self):
        self.calc = Calculator()

# pytest (third-party)
def test_addition():
    assert 2 + 2 == 4

def test_calculator():
    calc = Calculator()
    assert calc.add(2, 2) == 4
```

### pytest Advantages
- **Simple syntax**: Use plain `assert` statements
- **Better error messages**: Clear failure information
- **Powerful fixtures**: Flexible setup/teardown
- **Rich plugin ecosystem**: Coverage, mock, parallel execution
- **Parametrization**: Run same test with different inputs
- **Discovery**: Automatically finds tests

## Getting Started with pytest

### Installation
```bash
pip install pytest
pip install pytest-cov  # For coverage reports
pip install pytest-mock # For mocking support
pip install pytest-snapshot # For snapshot testing
```

### Test Discovery Rules
pytest automatically finds tests that follow these patterns:
- Files: `test_*.py` or `*_test.py`
- Classes: `Test*` (and no `__init__` method)
- Functions: `test_*`

### Running Tests
```bash
# Run all tests
pytest

# Run specific file
pytest test_calculator.py

# Run specific test
pytest test_calculator.py::test_addition

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=myproject
```

### pytest Assertions
```python
def test_assertions():
    # Basic assertions
    assert 1 == 1
    assert 2 > 1
    assert "hello" in "hello world"
    assert [1, 2, 3] == [1, 2, 3]
    
    # Testing exceptions
    with pytest.raises(ValueError):
        int("not a number")
    
    # Testing exceptions with message
    with pytest.raises(ValueError, match="invalid literal"):
        int("not a number")
    
    # Approximate equality for floats
    assert 0.1 + 0.2 == pytest.approx(0.3)
```

### Better Error Messages
```python
def test_dictionary_comparison():
    expected = {"name": "Alice", "age": 30, "city": "New York"}
    actual = {"name": "Alice", "age": 25, "city": "Boston"}
    
    assert actual == expected
    
    # pytest shows exactly what differs:
    # AssertionError: assert {'age': 25, 'city': 'Boston', 'name': 'Alice'} == {'age': 30, 'city': 'New York', 'name': 'Alice'}
    # Skipping 1 identical items, use -vv to show
    # Differing items:
    # {'age': 25} != {'age': 30}
    # {'city': 'Boston'} != {'city': 'New York'}
```

## Test Organization

### File Structure
```
project/
├── src/
├────── calc/
│        ├── calculator.py
│        ├── calculator.py
│        └── models.py
├── tests/
├────── calc/
│   │    ├── test_calculator.py
│   │    ├── test_models.py
│   ├── conftest.py          # Shared fixtures
│   └── integration/
│       └── test_api.py
├── pytest.ini              # Configuration
└── requirements.txt
```

### Test Class Organization
```python
class TestCalculator:
    """Group related tests together"""
    
    def test_addition(self):
        calc = Calculator()
        assert calc.add(2, 3) == 5
    
    def test_subtraction(self):
        calc = Calculator()
        assert calc.subtract(5, 3) == 2
    
    def test_division_by_zero(self):
        calc = Calculator()
        with pytest.raises(ZeroDivisionError):
            calc.divide(10, 0)
```

## Fixtures: Setup and Teardown

### Basic Fixtures
```python
import pytest

@pytest.fixture
def calculator():
    """Provide a Calculator instance for tests"""
    return Calculator()

def test_addition(calculator):
    assert calculator.add(2, 3) == 5

def test_multiplication(calculator):
    assert calculator.multiply(4, 5) == 20
```

### Fixture Scopes
```python
@pytest.fixture(scope="function")  # Default: new instance per test
def database_transaction():
    return start_transaction()

@pytest.fixture(scope="class")     # One instance per test class
def expensive_resource():
    return create_expensive_resource()

@pytest.fixture(scope="module")    # One instance per test file
def database_connection():
    return connect_to_database()

@pytest.fixture(scope="session")   # One instance per test session
def application_config():
    return load_config()
```

### Setup and Teardown
```python
@pytest.fixture
def temp_file():
    # Setup
    file_path = create_temp_file()
    
    # Provide the resource
    yield file_path
    
    # Teardown (runs after test completes)
    cleanup_temp_file(file_path)

def test_file_operations(temp_file):
    write_to_file(temp_file, "test data")
    content = read_from_file(temp_file)
    assert content == "test data"
```

## Parametrized Tests 🔄

### Testing Multiple Inputs
```python
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (1, 1, 2),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_addition(a, b, expected):
    calc = Calculator()
    assert calc.add(a, b) == expected
```

### More Complex Parametrization
```python
@pytest.mark.parametrize("input_data,expected", [
    ({"name": "Alice", "age": 30}, "Alice is 30 years old"),
    ({"name": "Bob", "age": 25}, "Bob is 25 years old"),
    ({"name": "Charlie"}, "Charlie's age is unknown"),
])
def test_format_person(input_data, expected):
    result = format_person(input_data)
    assert result == expected
```

### Testing Edge Cases
```python
@pytest.mark.parametrize("invalid_input", [
    None,
    "",
    "not-a-number",
    [],
    {},
])
def test_parse_number_invalid_input(invalid_input):
    with pytest.raises(ValueError):
        parse_number(invalid_input)
```

## Test Markers

### Built-in Markers
```python
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
def test_walrus_operator():
    pass

@pytest.mark.xfail(reason="Known bug, fix in progress")
def test_known_issue():
    assert broken_function() == expected_result
```

### Custom Markers
```python
# pytest.ini
[tool:pytest]
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests

# In tests
@pytest.mark.slow
def test_complex_calculation():
    pass

@pytest.mark.integration
def test_database_integration():
    pass

# Run only specific markers
# pytest -m "not slow"          # Skip slow tests
# pytest -m "unit"              # Run only unit tests
# pytest -m "integration"       # Run only integration tests
```

## Configuration

### pytest.ini
```ini
[tool:pytest]
# Test discovery
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Output options
addopts = 
    -v
    --strict-markers
    --disable-warnings
    --cov=src
    --cov-report=html
    --cov-report=term-missing

# Custom markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

### conftest.py
```python
# tests/conftest.py - Shared fixtures across all tests
import pytest
from myapp import create_app, init_database

@pytest.fixture(scope="session")
def app():
    """Create application for testing"""
    app = create_app(testing=True)
    with app.app_context():
        init_database()
        yield app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture(autouse=True)
def clean_database():
    """Automatically clean database after each test"""
    yield  # Run the test
    # Cleanup after test
    clear_test_data()
```

## Best Practices

### Test Naming
```python
# Good: Descriptive names
def test_user_creation_with_valid_email():
    pass

def test_login_fails_with_invalid_password():
    pass

def test_order_total_calculation_includes_tax():
    pass

# Bad: Vague names
def test_user():
    pass

def test_login():
    pass

def test_calculation():
    pass
```

### One Concept Per Test
```python
# Good: Single responsibility
def test_user_creation_sets_username():
    user = User("alice")
    assert user.username == "alice"

def test_user_creation_sets_default_active_status():
    user = User("alice")
    assert user.is_active is True

# Bad: Testing multiple concepts
def test_user_creation():
    user = User("alice")
    assert user.username == "alice"
    assert user.is_active is True
    assert user.created_at is not None
    assert len(user.roles) == 0
```


## Common Anti-patterns ❌

### Testing Implementation Details
```python
# Bad: Testing internal implementation
def test_sort_uses_quicksort():
    sorter = Sorter()
    assert sorter.algorithm == "quicksort"

# Good: Testing behavior
def test_sort_returns_sorted_list():
    sorter = Sorter()
    result = sorter.sort([3, 1, 4, 1, 5])
    assert result == [1, 1, 3, 4, 5]
```

### Over-mocking
```python
# Bad: Mocking everything
def test_user_service(mocker):
    mock_db = mocker.Mock()
    mock_validator = mocker.Mock()
    mock_logger = mocker.Mock()
    # ... too many mocks

# Good: Mock only external dependencies
def test_user_service(mock_database):
    service = UserService(mock_database)
    result = service.create_user("alice")
    assert result.username == "alice"
```
