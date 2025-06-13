# Common FastAPI Code Smells (and Fixes)

Improve maintainability and clarity by avoiding these common pitfalls in FastAPI apps.

---

## 1. Fat Endpoints

**Problem:** Route handler does all the logic — DB queries, decisions, and response formatting.

```python
@app.post("/users/")
def create_user(user: UserCreate):
    db = SessionLocal()
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(400)
    ...
```

**Fix:** Move logic into `UserService`. Keep endpoint thin.

---

## 2. Raising HTTPException in Business Logic

**Problem:** Service methods raise HTTP-specific exceptions like `HTTPException`.

```python
def create_user():
    raise HTTPException(status_code=400, detail="Conflict")
```

**Fix:** Raise domain-specific exceptions and let route translate.

```python
class UserAlreadyExists(Exception): pass
```

---

## 3. Returning ORM Models in Routes

**Problem:** Leaks internal model structure (e.g., passwords, metadata).

```python
return db_user
```

**Fix:** Use `response_model=UserOut` and return Pydantic schema.

---

## 4. Hardcoding DB Session Everywhere

**Problem:** Creating `SessionLocal()` inside routes/services directly.

**Fix:** Use dependency injection with `Depends(get_db)`

---

## 5. Blocking Code in Async Routes

**Problem:** Long DB queries, external calls or CPU-heavy code blocks event loop.

**Fix:** Use background tasks or Celery for slow operations.

---

## 6. Business Logic in Pydantic Validators

**Problem:** Trying to perform DB queries or heavy logic inside Pydantic models.

**Fix:** Keep validation lightweight; do heavy logic in service layer.

---

## 7. Massive utils.py Files

**Problem:** All helpers dumped into one growing file.

**Fix:** Group utilities by domain (e.g., `auth_utils.py`, `email_utils.py`)

---

## 8. Multiple Responsibilities in a Single Service Method

**Problem:** A service method is doing too much — DB writes, email sending, file creation, etc.

```python
def register_user_and_send_email_and_create_pdf(user_data):
    ...
```

**Fix:** Follow SRP (Single Responsibility Principle). Break down into:
- `UserService.create_user`
- `NotificationService.send_welcome_email`
- `PDFService.generate_user_profile`

---

## 9. Using Magic Strings Everywhere

**Problem:** Scattered status strings, error messages, types, etc.

```python
if task.status == "blocked": ...
```

**Fix:** Use `Enum`s or constants for shared values.

```python
class TaskStatus(str, Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"

if task.status == TaskStatus.BLOCKED:
```

---

## 10. Global Mutable State

**Problem:** Modifying shared lists/dicts at the module level (e.g., for caching, flags).

**Fix:** Use dependency-injected services or proper cache layers (e.g., Redis, context-local objects).

---

## 11. Not Logging Service-Level Errors

**Problem:** Logic fails silently or only logs via `print()`.

**Fix:** Use structured logging.

```python
import logging
logger = logging.getLogger(__name__)

def create_user(...):
    try:
        ...
    except Exception as e:
        logger.error("User creation failed", exc_info=e)
```

---

## 12. Dependency Injection Abuse in Routes

**Problem:** Passing 5+ `Depends(...)` into a single route function makes it unreadable.

```python
def handler(dep1=Depends(...), dep2=Depends(...), ..., dep6=Depends(...)):  # 😵
```

**Fix:** Group related deps into one higher-level dependency or compose in a service.

---

## 13. Static Files, JSON Paths, Secrets in Code

**Problem:** Hardcoded paths or tokens in route or service logic.

```python
with open("data/sample.json") as f: ...
API_KEY = "sk_live_123abc"
```

**Fix:** Use `pydantic.BaseSettings` and inject via `Depends(get_settings)`.

---

## 14. Querying the Same Object Twice

**Problem:**
```python
user = db.query(User).get(user_id)
if not user:
    ...
# later
user = db.query(User).get(user_id)
```

**Fix:** Reuse the object. Consider caching within request scope if needed.

---

## 15. Handling All Exceptions the Same Way

**Problem:** Catching a broad `except Exception:` and raising a generic 500.

**Fix:** Use specific exception types. Register global handlers for known domain exceptions:

```python
@app.exception_handler(EmailAlreadyUsed)
def email_exists_handler(req, exc):
    return JSONResponse(status_code=400, content={"detail": "Email already in use"})
```

---

## 16. Not Testing for Side Effects

**Problem:** A Celery task writes to DB or calls an external API, but tests only assert call count.

**Fix:** Assert the **effect** — e.g., DB record creation, task queue, email in outbox.

---

## "Clean" Code Checklist

- [ ] Are services small and focused?
- [ ] Is exception handling clear and layered?
- [ ] Are Enums/constants used instead of strings?
- [ ] Are secrets/configs loaded via environment or settings?
- [ ] Are logs meaningful and consistent?
- [ ] Are dependencies grouped or composed for complex routes?
- [ ] Are side effects (DB, emails, files) isolated and tested?
- [ ] Are business rules enforced in the service layer, not schema?
