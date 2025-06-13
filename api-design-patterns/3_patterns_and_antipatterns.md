# FastAPI Patterns vs. Anti-Patterns

## Good Patterns (Do’s)

### 1. **Keep Endpoints Thin**
**Do:** Keep FastAPI route functions short and readable.

```python
@router.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(user, db)
```

### 2. **Use Service Layers for Logic**
**Do:** Move logic into services or domain-specific classes.

```python
class UserService:
    def create_user(self, user: UserCreate, db: Session):
        if db.query(User).filter(User.email == user.email).first():
            raise UserAlreadyExists()
        user = User(**user.dict())
        db.add(user)
        db.commit()
        return user
```

### 3. **Raise Custom Exceptions in Services**
**Do:** Define domain-specific exceptions and raise those inside your business logic.

```python
class UserAlreadyExists(Exception):
    pass
```

### 4. **Translate Exceptions at the Endpoint**
**Do:** Catch service errors and convert them to HTTP responses.

```python
try:
    return user_service.create_user(user, db)
except UserAlreadyExists:
    raise HTTPException(status_code=400, detail="User already exists")
```

### 5. **Use Background Tasks or Celery**
**Do:** Offload time-consuming or async-unfriendly work.

```python
send_welcome_email_task.delay(user.email)
```

---

## Anti-Patterns (Don'ts)

### 1. **Fat Endpoints**
**Don't:** Do everything in the route.

```python
@router.post("/register")
def register(user: UserCreate):
    db = SessionLocal()
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(400, "User exists")
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    send_email_sync(new_user.email)  # Blocking call
    return new_user
```

### 2. **Mixing HTTP with Business Logic**
**Don't:** Raise `HTTPException` inside your core logic.

```python
# Bad
def create_user(user):
    if user_exists(user):
        raise HTTPException(400, "Already exists")
```

Use domain exceptions instead.

### 3. **Directly Returning ORM Objects**
**Don't:** Return raw SQLAlchemy models.

```python
return db_user  # leaks internal fields like password
```

Use Pydantic schemas instead.

### 4. **Skipping Dependency Injection**
**Don't:** Instantiate DB sessions or services manually everywhere.

```python
# Bad
db = SessionLocal()
service = UserService()
```

Use `Depends(get_db)` and `Depends(get_user_service)` where needed.

---

## Is it OK to raise HTTPException inside a dependency?

**Answer:** Yes, in most cases it is **acceptable and idiomatic** to raise `HTTPException` inside a FastAPI dependency function. This is especially true for request-level concerns such as:

- Authentication failures (e.g., invalid token)
- Authorization rejections (e.g., insufficient permissions)
- Request validation issues tied to contextual checks

**Example:**

```python
from fastapi import Depends, HTTPException, status

def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_and_verify_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user
```

Here, the dependency is acting like a gatekeeper for the route. Since dependencies are part of the HTTP layer, raising `HTTPException` aligns with FastAPI's design.

**Caveat:** Do **not** raise `HTTPException` inside your core service logic. Limit it to dependencies and route-level functions.

---

## Clean Design Summary

| Do | Don’t |
|------|---------|
| Delegate to service layer | Write all logic in endpoint |
| Raise custom exceptions | Raise HTTPException in core logic |
| Use Celery for background jobs | Block on long tasks in request thread |
| Return Pydantic models | Return ORM objects |
| Use DI via Depends | Create services/sessions manually |

