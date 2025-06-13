## TestClient in FastAPI

FastAPI provides a powerful, easy-to-use testing layer built on Starlette’s ASGI utilities. we can test our API endpoints without starting a real server.

### 1. `TestClient`

* **What it is:** A synchronous client that simulates HTTP requests against FastAPI app in memory.
* **Why use it:** No need to spin up an actual server; requests are handled by calling ASGI app functions directly under the hood.

    ```python
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    app = FastAPI()


    @app.get("/")
    async def read_main():
        return {"msg": "Hello World"}


    client = TestClient(app)


    def test_read_main():
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"msg": "Hello World"}
    ```

#### Additional Features

* **Setting headers per request**

  ```python
  response = client.get("/", headers={"Authorization": "Bearer token"})
  ```

* **Sending files in tests**

  ```python
  with open("example.txt", "rb") as f:
      response = client.post("/form", files={"file": f})
  ```

* **Also we can send json body, params, and set cookies**

* **⚠️Async endpoint handling**
  Even if your endpoint functions are `async`, you can call `client.get()` or `client.post()` without `await`. The `TestClient` runs the async code in an internal event loop for you.

  ---

## References

* [FastAPI Testing Tutorial](https://fastapi.tiangolo.com/tutorial/testing/)
