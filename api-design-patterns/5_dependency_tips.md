# FastAPI Dependency Injection Tips

Practical tips for using FastAPI’s `Depends` system to keep your code clean, testable, and modular — especially when separating endpoint and business logic.

It has the added benefit that you can also replace all your dependencies with mocks and test your code without having to instantiate a huge chain of dependencies.

---

## What to Use Dependencies For

- **Database sessions**
- **Authenticated users**
- **Service class instances**
- **Shared config or clients (e.g., Redis, S3, Email)**

---

## Example: Injecting a Database Session

```python
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Usage in endpoint or another dependency:

```python
@router.get("/items/")
def list_items(db: Session = Depends(get_db)):
    ...
```

---

## Example: Injecting a Service Layer

```python
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

@router.post("/users/")
def register_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(user)
```

- Keeps route clean  
- Easy to override in tests

---

## Don’t Do This

- Instantiate DB sessions or services manually:
  ```python
  db = SessionLocal()
  service = UserService(db)
  ```

- Call `Depends(...)` inside functions:
  ```python
  def my_func():
      db = Depends(get_db)  # Wrong!
  ```

- Use global DB or client instances inside business logic

---

## Reusability Tip

Services or utilities created via `Depends` can be reused across:
- Routes
- Background tasks (if launched via route)
- Other dependencies

You can even **chain** dependencies:

```python
def get_authorized_user(
    user: User = Depends(get_current_user)
) -> User:
    if not user.is_active:
        raise HTTPException(403)
    return user
```

---

## Tip for Testing

Override dependencies in tests:

```python
app.dependency_overrides[get_db] = lambda: test_session
app.dependency_overrides[get_user_service] = lambda: FakeUserService()
```

---

## Summary

| Do This | Avoid This |
|-----------|--------------|
| Use `Depends` for shared logic | Manual instantiation |
| Inject services per-request | Globals for stateful objects |
| Chain dependencies when needed | Using `Depends()` inside regular functions |
| Override in tests | Coupling logic to framework state |

