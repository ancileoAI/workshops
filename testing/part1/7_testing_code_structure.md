### Testing Structure by FastAPI

- In our project we already use it 

```text
your_project/
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── user.py 
│   └── services/
│       └── user_service.py # Business logic

├── tests/
│   ├── unit/
│   │   └── services/
│   │       └── test_user_service.py

│   ├── integration/
│   │   └── api/
│   │       └── routes/
│   │           └── test_user.py

│   └── conftest.py    # Shared fixtures ( DB session, clients, dependencies overrides)


