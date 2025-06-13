## Mocking External Services in Tests

### Why Mock?

* Call external **APIs**
* Communicate with **databases**, **file storage**, or **other microservices**
* Rely on **slow**, **unreliable**, or **costly** services

Mocking allows to **simulate** the behavior of these services during tests, without actually calling them. This makes tests:

* **Faster**
* **More reliable**
* **Deterministic** (always return the same thing)

---

### How to Mock in Python

Use the `unittest.mock` module (built into Python):

```python
from unittest.mock import patch, AsyncMock
```

You can use:

* `patch()` to **replace** a function, method, or object
* `AsyncMock` to mock **async** functions

---

### Example: Mocking an External API Call


```python
# my_app/services/weather.py
import httpx

async def get_weather_data(city: str):
    response = await httpx.get(f"https://weather.api/{city}")
    return response.json()
```

```python
## my_app/main.py
from fastapi import FastAPI
from my_app.services.weather import get_weather_data

app = FastAPI()

@app.get("/weather/{city}")
async def weather(city: str):
    data = await get_weather_data(city)
    return {"city": city, "forecast": data}
```

```python
# tests/test_weather.py

from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from my_app.main import app

def test_mock_weather_service():
    mock_data = {"temp": "22C", "status": "sunny"}
    # Because get_weather_data is async, we use AsyncMock instead of Mock to properly mock async behavior.
    with patch("my_app.services.weather.get_weather_data", new=AsyncMock(return_value=mock_data)):
        client = TestClient(app)
        response = client.get("/weather/malaysia")
        assert response.status_code == 200
        assert response.json() == {
            "city": "malaysia",
            "forecast": mock_data
        }
```

---

### Notes

* **Use `AsyncMock`** for mocking `async def` functions.
* Always **import the path as used in the module being tested**.
* You can mock **return values**, or raise **exceptions**.

---
