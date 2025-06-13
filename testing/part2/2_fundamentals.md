## Testing Fundamentals

### The AAA pattern

Generally every test should follow **Arrange, Act, Assert**:

```python
def test_item_creation():
    # Arrange - Set up test data
    item_data = {
        "field1": "field1 data",
        "field2": False
    }
    
    # Act - Perform the action
    item = create_item(item_data)
    
    # Assert - Check the result
    assert item.field1 == "field1 data"
    assert item.field2 == False
```

### What makes a good test?

**F.I.R.S.T. Principles**
- **Fast**: Tests should run quickly
- **Independent**: Tests shouldn't depend on each other
- **Repeatable**: Same result every time
- **Self-Validating**: Pass or fail, no manual checking
- **Timely**: Written just before or after the code

### Test case components

1. **Test Name**: Descriptive, explains what's being tested
2. **Setup**: Prepare test environment
3. **Execution**: Run the code being tested
4. **Verification**: Check results
5. **Teardown**: Clean up after test

### Common pitfalls

**Testing Implementation Details**
```python
# Bad - tests internal implementation
def test_user_password():
    user = User("test@example.com", "password123")
    assert user._hashed_password.startswith("$2b$")  # Don't test internals!
```

✅ **Testing Behavior**
```python
# Good - tests behavior
def test_user_authentication():
    user = User("test@example.com", "password123")
    assert user.check_password("password123") == True
    assert user.check_password("wrongpassword") == False
```

### Naming Conventions

**Test Names Should Be Descriptive**
```python
# Bad
def test_1():
    ...

# Good
def test_user_with_invalid_email_raises_validation_error():
    ...

# Also good - using given/when/then
def test_given_invalid_email_when_creating_user_then_raises_error():
    ...
```

```
python# Good: Descriptive names
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
