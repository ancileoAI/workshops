## Testing Dependencies with Overrides

### Introduction

There are some scenarios where we might want to **override a dependency during testing**.
For example, we might not want the original dependency (or any of its sub-dependencies) to run, especially if:

* The dependency calls an **external service**
* It’s **slow** or **costly**
* We want to return a **mocked response** just for testing

Instead, we can **override the dependency** to use a test version that returns a controlled results.

---

### How It Works

FastAPI provides an attribute:

```python
app.dependency_overrides
```

This is a simple dictionary that maps:

* The **original dependency function** → to the
* **Override function** used only in tests

FastAPI will call the override during the test instead of the real function.

---

### Example

```python
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

# Original dependency
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return {"message": "Hello Items!", "params": commons}

# Override dependency for testing
async def override_dependency(q: str | None = None):
    return {"q": q, "skip": 5, "limit": 10}

# Apply the override
app.dependency_overrides[common_parameters] = override_dependency

client = TestClient(app)
response = client.get("/items/")
print(response.json())
```

---
also you can check `Claim-agent-ai/backend/auth/tests/conftest.py`

[Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/#use-cases-external-service)

