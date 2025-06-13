## 2. `AsyncClient`

* When your test functions are themselves `async def`, you’ll need an async client.

    ```python
    import pytest
    from httpx import AsyncClient

    @pytest.mark.asyncio
    async def test_read_main_async():
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/")
            assert response.status_code == 200
            assert response.json() == {"msg": "Hello World"}
    ```

 * **When to use which client:**

  * Use `TestClient` in regular (synchronous) `def` test functions.
  * Use `AsyncClient` inside `async def` test functions when you manage the event loop yourself.

* #### ⚠️ Important Notes

    * You must always `await` requests.  

    * `@pytest.mark.asyncio` is **not a built-in pytest featur**

    * It is provided by the third-party `pytest-asyncio` plugin.

    * You need to use `@pytest.mark.asyncio` to support `async def` tests

    * By default, pytest does not know how to run `async def` functions, `pytest` sees `test_read_main_async()` as just a coroutine object, and has no idea how to run it.

        So instead of failing or ignoring the test, pytest will:

        1. Detect the coroutine

        2. Start an **event loop**

        3. Await the coroutine

    * when we say app=app, by deafult there is a transport=ASGITransport(app=app), which lead as to send the in memory request no need for real network 

---
