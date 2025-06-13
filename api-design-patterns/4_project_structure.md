# Recommended Project Structure for FastAPI Applications

A clean, modular project structure supports:
- Better separation of concerns
- Easier testing and onboarding
- Scalable team collaboration
- Easier future migrations (e.g., changing DB, framework)

---

## Layered Structure by Responsibility

```
app/
├── api/              # FastAPI route handlers
│   └── users.py
├── services/         # Business logic (domain services)
│   └── user_service.py
├── models/           # SQLAlchemy models
│   └── user.py
├── schemas/          # Pydantic schemas (input/output)
│   └── user.py
├── tasks/            # Celery tasks or background job logic
│   └── email.py
├── db/               # DB connection, session & dependencies
│   └── session.py
├── core/             # App setup, config, utilities
│   └── config.py
└── main.py           # FastAPI app instantiation and route registration
```

---

## Directory Responsibilities

### `api/`
- One file per feature or router (e.g., `users.py`, `auth.py`)
- Route functions use `Depends` to resolve services
- Thin functions: receive input, call service, return output

### `services/`
- Implements business rules and logic
- Handles database interactions
- Coordinates Celery tasks
- Pure Python — no FastAPI-specific imports

### `models/`
- SQLAlchemy ORM classes
- Reflect your database schema

### `schemas/`
- Pydantic models for input/output validation
- Clean API boundaries (no sensitive fields like passwords)

### `tasks/`
- Celery or FastAPI background task logic
- Decouples slow work from the request cycle

### `db/`
- Contains session and engine creation
- `get_db()` dependency lives here

### `core/`
- Configuration, settings loading
- Any cross-cutting utility functions

---

## Best Practices

- Group features together (e.g., `users`, `claims`, `reports`)
- Keep models, services, routes separate per feature if needed
- Avoid `utils/` folders that become junk drawers
- Use `__init__.py` files to help with relative imports if needed
- Aim for consistency — folders should look the same across features

---

## Example Use in Code

```python
# api/users.py
@router.post("/register", response_model=UserRead)
def register(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    return user_service.create_user(user)
```

```python
# services/user_service.py
class UserService:
    def create_user(self, data: UserCreate) -> User:
        ...
```

```python
# db/session.py
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

