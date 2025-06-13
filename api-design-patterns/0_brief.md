# Lecture: Clean API Design with FastAPI

## Title
**Separating Endpoint Logic from Business Logic in FastAPI**

## Introduction 
- "Design principle that will make your FastAPI code cleaner, easier to test, and much more scalable."
- State goals:
  - Keep endpoints focused on HTTP layer
  - Delegate processing to clean, reusable service layers
  - Apply this with FastAPI + SQLAlchemy + Celery

---

## Why Separation of Concerns Matters 
- Keeps code **readable** – less cognitive load per function
- Enables **testing** – test logic without HTTP server
- Improves **reusability** – services reused in scripts, CLI, or other endpoints
- Supports **teamwork** – API devs and logic devs can work independently

---

## What Should Stay in Endpoints 
FastAPI endpoints (route handlers) should:

- Validate and parse request data (via Pydantic)
- Handle authentication/authorization
- Call into services (business logic)
- Convert exceptions into `HTTPException`
- Return Pydantic models or shaped responses

**Key principle:** Endpoints orchestrate, **don’t calculate**.

---

## What Goes in the Business Logic Layer 
The service layer (e.g. `UserService`, `ItemService`) should:

- Implement core domain logic and rules
- Perform DB interactions (via SQLAlchemy or repository)
- Trigger background jobs (e.g. Celery)
- Raise domain-specific exceptions (not HTTP)
- Return clean result objects or Pydantic-compatible outputs

**Reminder:** Services are framework-agnostic. They don’t import FastAPI.

---

## Example Project Structure
```
app/
├── api/            # Route handlers (FastAPI endpoints)
├── services/       # Business logic classes/functions
├── models/         # SQLAlchemy ORM models
├── schemas/        # Pydantic input/output schemas
├── tasks/          # Celery background jobs
└── main.py         # App entrypoint
```

**Tip:** Group files by domain (feature-first), not just layer.

---

## Anti-Patterns (with quick examples)
- **Fat endpoints** doing DB queries, logic, and response all at once
- **Mixing FastAPI and SQLAlchemy logic** in same function
- **Raising HTTPException inside service layer**
- **Not using background tasks** for long-running work

---

## Live Coding Demo
Walk through examples

---

## Q&A
- Small discussions or questions

---

## Transition to Exercises

---

## Recap
- Endpoints = thin controllers
- Services = business rules
- Celery = background workers
- Structure = key to long-term maintainability

---


