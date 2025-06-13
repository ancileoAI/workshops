# Testing in FastAPI

## Why Testing?

* **Catch bugs early**
  It’s cheaper to fix bugs during development than in production.
* **Ensure code quality**
  Tests help maintain clean, working code even as our app grows (spreate businis logic from endpoint).
* **Prevent regressions**
  When we change something, tests help us avoid breaking what used to work.

* **usful for CI/CD**
  As automated tests run every time someone pushes code. If something breaks, the build fails, preventing bad code from being merged.

---

## Simple Example

```python
def add(a: int, b: int) -> int:
    return a + b


def test_add():
    assert add(2, 3) == 5
```

⚠️`assert` It raises a generic AssertionError so the test either fail or pass that's why we only use it when writing tests not for production as it can be disabled with Python's `-O` (optimize) flag..
