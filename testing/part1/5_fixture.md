## Fixture

## What is a Fixture
- A reusable piece of setup code for your tests.
- used to prepare some state, object, or environment before your test run

### Why Use Fixtures?

Instead of repeating setup code in every test, you define a fixture **once** and reuse it.

- DRY (Don't Repeat Yourself)
    
- Centralized setup logic
    
- Can be shared across many test files

### Simple Example

```python
import pytest

@pytest.fixture
def sample_data():
    return {"name": "Alice", "age": 30}

def test_user_age(sample_data):
    assert sample_data["age"] == 30

```
- More meaningful example 

    ```python
    # usually inside the conftest file (will see about it later) we do this 

    # conftest.py
    import pytest
    from fastapi.testclient import TestClient
    from my_app.main import app

    @pytest.fixture
    def client():
        return TestClient(app)
    ```
- then in any place we can do the following :

    ```python
    # tests/test_users.py
    def test_homepage(client):
        response = client.get("/")
        assert response.status_code == 200
    ```

### Fixture Scope

we can control **how often** a fixture runs:

- `function` – every test (default)
    
- `module` – once per test file
    
- `session` – once per entire test session


### Notes
- you can make a fixture run automatically (without needing to declare it in each test) no need to pass them explicitly to the test.

| Scope      | Runs...                    | Good for                        |
| ---------- | -------------------------- | ------------------------------- |
| `function` | Before each test (default) | Isolated logic                  |
| `module`   | Once per test file         | Reuse across tests in file      |
| `session`  | Once per entire test run   | DB setup, config, caching       |
| `autouse`  | Auto-runs in background    | cleanup
| `async`    | Async setup/teardown       | Async clients, DBs, services    |


Example for `Claim-agent-ai`
```python

# Each test runs in an isolated DB transaction that’s automatically rolled back, so tests don’t affect each other
@pytest_asyncio.fixture(scope="function", autouse=True)
async def transactional_session(setup_database) -> AsyncSession:
    async with sessionmanager.session() as session:
        try:
            await session.begin()
            await init_db(session)
            yield session
        finally:
            await session.rollback() # Rolls back the transaction after the test, no data is persisted.
            await session.close()
```