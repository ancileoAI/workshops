# Advanced Testing Patterns

## Advanced Fixtures

### Fixture Dependencies
```python
@pytest.fixture
def database():
    db = create_test_database()
    yield db
    db.close()

@pytest.fixture
def user_repository(database):
    return UserRepository(database)

@pytest.fixture
def user_service(user_repository):
    return UserService(user_repository)

def test_user_creation(user_service):
    user = user_service.create_user("alice@example.com")
    assert user.email == "alice@example.com"
```

### Factory Fixtures
```python
@pytest.fixture
def user_factory():
    """Factory to create users with different attributes"""
    def _create_user(name="Alice", email=None, age=25):
        if email is None:
            email = f"{name.lower()}@example.com"
        return User(name=name, email=email, age=age)
    return _create_user

def test_user_creation_variations(user_factory):
    # Create different users easily
    admin = user_factory("Admin", "admin@company.com", 35)
    teenager = user_factory("Teen", age=16)
    default_user = user_factory()
    
    assert admin.name == "Admin"
    assert teenager.age == 16
    assert default_user.email == "alice@example.com"
```

### Fixture Cleanup Patterns
```python
@pytest.fixture
def temp_directory():
    """Create and cleanup temporary directory"""
    import tempfile
    import shutil
    
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)

@pytest.fixture
def mock_external_api():
    """Mock external API with cleanup"""
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"status": "ok"}
        yield mock_get
    # Automatic cleanup when exiting context
```

### Autouse Fixtures
```python
@pytest.fixture(autouse=True)
def reset_singletons():
    """Automatically reset singletons before each test"""
    DatabaseConnection.reset()
    ConfigManager.reset()
    yield
    # Cleanup after test

@pytest.fixture(autouse=True, scope="session")
def setup_test_environment():
    """Set up test environment once per session"""
    os.environ['TESTING'] = 'true'
    yield
    del os.environ['TESTING']
```

## Mocking and Test Doubles

### Types of Test Doubles
- **Dummy**: Objects passed around but never used
- **Fake**: Working implementations with shortcuts
- **Stub**: Provides canned answers to calls
- **Spy**: Records information about calls
- **Mock**: Pre-programmed with expectations

### Basic Mocking with pytest-mock
```python
def test_user_service_calls_email_service(mocker):
    # Mock the email service
    mock_email_service = mocker.Mock()
    user_service = UserService(email_service=mock_email_service)
    
    # Test the functionality
    user_service.register_user("alice@example.com")
    
    # Verify the interaction
    mock_email_service.send_welcome_email.assert_called_once_with("alice@example.com")
```

### Patching External Dependencies
```python
def test_weather_service_api_call(mocker):
    # Patch the external API call
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "temperature": 25,
        "condition": "sunny"
    }
    
    mocker.patch('requests.get', return_value=mock_response)
    
    # Test your code
    weather_service = WeatherService()
    result = weather_service.get_weather("London")
    
    assert result["temperature"] == 25
    assert result["condition"] == "sunny"
```

### Advanced Mock Configurations
```python
def test_database_operations(mocker):
    # Mock with side effects
    mock_db = mocker.Mock()
    mock_db.save.side_effect = [True, DatabaseError("Connection lost"), True]
    
    service = DataService(mock_db)
    
    # First call succeeds
    assert service.save_data("data1") is True
    
    # Second call fails
    with pytest.raises(DatabaseError):
        service.save_data("data2")
    
    # Third call succeeds again
    assert service.save_data("data3") is True
    
    # Verify call count
    assert mock_db.save.call_count == 3
```

### Spy Pattern - Partial Mocking
```python
def test_cache_hit_optimization(mocker):
    # Spy on the expensive operation
    cache_service = CacheService()
    spy_expensive_op = mocker.spy(cache_service, '_expensive_calculation')
    
    # First call should trigger calculation
    result1 = cache_service.get_result("key1")
    assert spy_expensive_op.call_count == 1
    
    # Second call with same key should use cache
    result2 = cache_service.get_result("key1")
    assert spy_expensive_op.call_count == 1  # Still 1, not 2
    assert result1 == result2
```

## Property-Based Testing

### Introduction to Hypothesis
```python
from hypothesis import given, strategies as st

@given(st.integers())
def test_absolute_value_properties(x):
    """Test mathematical properties of abs()"""
    result = abs(x)
    
    # Property 1: abs(x) is always non-negative
    assert result >= 0
    
    # Property 2: abs(abs(x)) == abs(x)
    assert abs(result) == result
    
    # Property 3: abs(x) * sign(x) == x (when x != 0)
    if x != 0:
        sign = 1 if x > 0 else -1
        assert result * sign == x
```

### Testing Business Logic Properties
```python
@given(st.lists(st.integers(), min_size=1))
def test_sort_function_properties(numbers):
    """Test properties of our sorting function"""
    sorted_numbers = our_sort_function(numbers)
    
    # Property 1: Result has same length
    assert len(sorted_numbers) == len(numbers)
    
    # Property 2: Result contains same elements
    assert sorted(sorted_numbers) == sorted(numbers)
    
    # Property 3: Result is actually sorted
    assert sorted_numbers == sorted(sorted_numbers)
    
    # Property 4: Is stable for equal elements
    # (requires more complex setup for meaningful test)
```

### Custom Strategies
```python
# Define custom data generators
email_strategy = st.builds(
    lambda name, domain: f"{name}@{domain}",
    name=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('L', 'N'))),
    domain=st.sampled_from(['gmail.com', 'yahoo.com', 'company.com'])
)

@given(email_strategy)
def test_email_validation(email):
    """Test email validation with generated emails"""
    assert is_valid_email(email) is True
    assert '@' in email
    assert email.count('@') == 1
```

## Test Organization Patterns

### Page Object Pattern (for UI tests)
```python
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
    
    def enter_username(self, username):
        self.driver.find_element("id", "username").send_keys(username)
        return self
    
    def enter_password(self, password):
        self.driver.find_element("id", "password").send_keys(password)
        return self
    
    def click_login(self):
        self.driver.find_element("id", "login-btn").click()
        return DashboardPage(self.driver)

def test_successful_login(browser):
    login_page = LoginPage(browser)
    dashboard = (login_page
                .enter_username("testuser")
                .enter_password("password123")
                .click_login())
    
    assert dashboard.is_logged_in()
```

### Builder Pattern for Test Data
```python
class UserBuilder:
    def __init__(self):
        self.user_data = {
            'name': 'Default User',
            'email': 'user@example.com',
            'age': 25,
            'is_active': True
        }
    
    def with_name(self, name):
        self.user_data['name'] = name
        return self
    
    def with_email(self, email):
        self.user_data['email'] = email
        return self
    
    def inactive(self):
        self.user_data['is_active'] = False
        return self
    
    def build(self):
        return User(**self.user_data)

def test_user_scenarios():
    # Clean, readable test data creation
    admin = UserBuilder().with_name("Admin").with_email("admin@company.com").build()
    inactive_user = UserBuilder().inactive().build()
    
    assert admin.name == "Admin"
    assert not inactive_user.is_active
```

### Test Categories with Markers
```python
# conftest.py
def pytest_configure(config):
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "slow: Slow tests")
    config.addinivalue_line("markers", "external: Tests requiring external services")

# In test files
@pytest.mark.unit
def test_calculate_tax():
    pass

@pytest.mark.integration
@pytest.mark.slow
def test_database_migration():
    pass

@pytest.mark.external
def test_payment_gateway():
    pass

# Run specific categories:
# pytest -m unit           # Only unit tests
# pytest -m "not slow"     # Skip slow tests
# pytest -m "integration and not external"  # Integration but not external
```

## Data-Driven Testing

### CSV Data Sources
```python
import csv
import pytest

def load_test_data(filename):
    """Load test data from CSV file"""
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)

# test_data.csv:
# input,expected,description
# "hello world","world hello","basic reversal"
# "a","a","single character"
# "","","empty string"

@pytest.mark.parametrize("test_case", load_test_data("test_data.csv"))
def test_reverse_words_from_csv(test_case):
    result = reverse_words(test_case['input'])
    assert result == test_case['expected'], test_case['description']
```

### JSON Test Scenarios
```python
import json

@pytest.fixture
def user_scenarios():
    with open('user_test_scenarios.json') as f:
        return json.load(f)

def test_user_validation_scenarios(user_scenarios):
    for scenario in user_scenarios['validation_tests']:
        user_data = scenario['input']
        expected_valid = scenario['expected_valid']
        
        is_valid = validate_user(user_data)
        assert is_valid == expected_valid, f"Failed: {scenario['description']}"
```

## Error Testing Patterns

### Testing Exception Details
```python
def test_division_by_zero_error():
    with pytest.raises(ZeroDivisionError, match="division by zero"):
        divide(10, 0)

def test_validation_error_details():
    with pytest.raises(ValidationError) as exc_info:
        validate_age(-5)
    
    # Check exception details
    error = exc_info.value
    assert "Age must be positive" in str(error)
    assert error.field == "age"
    assert error.value == -5
```

### Testing Error Recovery
```python
def test_retry_mechanism(mocker):
    # Mock that fails twice, then succeeds
    mock_api = mocker.Mock()
    mock_api.call.side_effect = [
        ConnectionError("Network error"),
        ConnectionError("Network error"),
        {"status": "success"}
    ]
    
    service = ResilientService(mock_api, max_retries=3)
    result = service.make_call()
    
    assert result == {"status": "success"}
    assert mock_api.call.call_count == 3
```

## Performance Testing

### Timing Tests
```python
import time
import pytest

def test_algorithm_performance():
    large_dataset = generate_large_dataset(10000)
    
    start_time = time.time()
    result = our_algorithm(large_dataset)
    end_time = time.time()
    
    # Should complete within 1 second
    assert end_time - start_time < 1.0
    assert len(result) == 10000

@pytest.mark.timeout(5)  # Requires pytest-timeout
def test_operation_timeout():
    # This test will fail if it takes longer than 5 seconds
    result = potentially_slow_operation()
    assert result is not None
```

### Memory Usage Testing
```python
import psutil
import os

def test_memory_usage():
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Perform memory-intensive operation
    large_data = create_large_data_structure()
    process_data(large_data)
    
    # Clean up
    del large_data
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # Memory increase should be reasonable (less than 100MB)
    assert memory_increase < 100 * 1024 * 1024
```
