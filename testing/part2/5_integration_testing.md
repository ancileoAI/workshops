## Integration testing

### The philosophy of integration testing

Integration tests verify that **independently developed components work together correctly**. While unit tests verify "we built the parts right," integration tests verify "the parts fit together."

**Key principles:**
- **Test the contracts between components**, not their internal workings
- **Focus on boundaries** where components interact
- **Use real implementations** instead of mocks (where feasible)
- **Accept slower execution** in exchange for higher confidence
- **Test the paths data travels** through your system

### What to integration test

**API endpoints**
```python
def test_create_user_endpoint():
    response = client.post("/users", json={
        "email": "test@example.com",
        "password": "secure123"
    })
    
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    
    # Verify user was actually created in database
    user = db.query(User).filter_by(email="test@example.com").first()
    assert user is not None
```

**Why API integration tests matter:**
- **Contract validation**: ensures API contracts match client expectations
- **Middleware verification**: tests authentication, validation, error handling
- **Serialization testing**: catches issues with data transformation
- **Full request cycle**: tests routing, parsing, and response formatting
- **Database state verification**: confirms side effects actually occurred

**Critical API testing concepts:**
- Test **error responses** as thoroughly as success cases
- Verify **idempotency** for operations that should be idempotent
- Test **pagination**, **filtering**, and **sorting** at scale
- Validate **API versioning** behavior
- Check **rate limiting** and **authentication** integration

**Database Operations**
```python
def test_user_repository():
    # Test with real database (test database)
    repo = UserRepository(test_db)
    
    # Create
    user = repo.create(email="test@example.com")
    assert user.id is not None
    
    # Read
    fetched = repo.get(user.id)
    assert fetched.email == "test@example.com"
    
    # Update
    repo.update(user.id, name="Updated Name")
    updated = repo.get(user.id)
    assert updated.name == "Updated Name"
```

**Database integration testing principles:**
- **Transaction boundaries**: test rollback behavior on errors
- **Constraint validation**: foreign keys, unique constraints, check constraints
- **Query performance**: use EXPLAIN to catch N+1 queries
- **Concurrent access**: test optimistic/pessimistic locking
- **Migration testing**: ensure schema changes don't break existing code

**The database testing pyramid:**
```
Real production DB (never test here!)
    ↓
Production-like DB (same version, similar data volume)
    ↓
Test database (same engine, empty/minimal data)
    ↓
In-memory database (fast but may hide issues)
```

**External service integration**
```python
@pytest.mark.integration
def test_payment_processing():
    # Use test/sandbox environment
    payment_service = PaymentService(api_key=TEST_API_KEY)
    
    result = payment_service.charge(
        amount=1000,  # $10.00
        card_token="tok_test_visa"
    )
    
    assert result.success == True
    assert result.transaction_id is not None
```

**External service testing strategies:**
- **Sandbox environments**: use provider's test environments when available
- **Contract testing**: verify your assumptions about external API behavior
- **Fault injection**: test timeout, error, and partial failure scenarios
- **Rate limit handling**: ensure graceful degradation
- **Circuit breaker testing**: verify fallback behavior

### Integration test design patterns

**The test data builder pattern:**
Build complex test scenarios incrementally:
```python
class TestDataBuilder:
    def with_user(self, **attributes)
    def with_order(self, **attributes)
    def with_payment(self, **attributes)
    def build(self)
```

**The test harness pattern:**
Create a simplified environment that mimics production:
- Containerized dependencies (Docker Compose)
- Embedded servers (in-memory Redis, embedded Kafka)
- Stubbed external services (WireMock, LocalStack)

**The journey test pattern:**
Test complete user journeys through the system:
1. User registration → 2. Email verification → 3. Profile completion → 4. First purchase

### Test fixtures and data

**Using fixtures**:
```python
@pytest.fixture
def test_user():
    user = User(email="fixture@example.com")
    db.session.add(user)
    db.session.commit()
    
    yield user  # Test runs here
    
    # Cleanup
    db.session.delete(user)
    db.session.commit()

def test_user_orders(test_user):
    order = create_order(test_user, items=[...])
    assert order.user_id == test_user.id
```

**Fixture design principles:**

**Scope management:**
- **Function scope**: Fresh data for each test (slowest, most isolated)
- **Class scope**: Shared within test class (faster, some coupling)
- **Module scope**: Shared within file (faster, more coupling)
- **Session scope**: Shared across all tests (fastest, most coupling)

**The fixture hierarchy:**
```python
@pytest.fixture(scope="session")
def database_engine():
    # Created once per test run
    
@pytest.fixture(scope="module")
def database_schema(database_engine):
    # Created once per test module
    
@pytest.fixture(scope="function")
def database_session(database_schema):
    # Fresh session per test
    
@pytest.fixture(scope="function")
def test_user(database_session):
    # Fresh user per test
```

**Advanced fixture patterns:**
- **Parameterized fixtures**: Test with different configurations
- **Factory fixtures**: Create multiple instances with variations
- **Composite fixtures**: Combine fixtures for complex scenarios
- **Dynamic fixtures**: Generate based on test requirements

### Integration testing anti-patterns

**Testing too much:**
- Don't test framework functionality
- Don't test database engine behavior
- Don't test external service implementation

**Testing too little:**
- Missing error path testing
- Ignoring performance characteristics
- Skipping concurrent access scenarios

**Environment mismatch:**
- SQLite in tests, PostgreSQL in production
- Different library versions
- Missing middleware or configurations

### Performance considerations

**Integration test performance optimization:**
- **Parallel execution**: Run independent tests concurrently
- **Smart fixtures**: Reuse expensive setups when safe
- **Lazy loading**: Only create data when needed
- **Transaction rollback**: Faster than delete/recreate
- **Test segmentation**: Run critical tests first

**When slow tests are worth it:**
- Critical business flows
- Complex integration points
- High-risk changes
- Regulatory compliance
