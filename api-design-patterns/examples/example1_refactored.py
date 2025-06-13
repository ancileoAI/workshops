"""
Improved version of the endpoint:
- Route: handles HTTP request/response only
- Service: handles business logic and DB interaction
- Task: offloads email to Celery
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from passlib.hash import bcrypt
from celery import Celery

# Setup usually /main.py and /db 
app = FastAPI()
Base = declarative_base()
engine = create_engine("sqlite:///./test.db")
SessionLocal = lambda: Session(bind=engine)

celery_app = Celery("tasks", broker="redis://localhost:6379/0")

# Models and Schemas in /schemas
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)

class UserCreate(BaseModel):
    email: str
    name: str
    password: str

class UserRead(BaseModel):
    id: int
    email: str
    name: str

    class Config:
        orm_mode = True

# Celery Task in /tasks
@celery_app.task
def send_welcome_email(email: str):
    print(f"[Celery] Sending welcome email to {email}")

# Business Logic /services
class UserAlreadyExists(Exception):
    pass

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, data: UserCreate) -> User:
        if self.db.query(User).filter(User.email == data.email).first():
            raise UserAlreadyExists()

        hashed_pw = bcrypt.hash(data.password)
        user = User(email=data.email, name=data.name, hashed_password=hashed_pw)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        send_welcome_email.delay(user.email)

        return user

# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)

# Route
@app.post("/register", response_model=UserRead)
def register(user_in: UserCreate, user_service: UserService = Depends(get_user_service)):
    try:
        user = user_service.create_user(user_in)
        return user
    except UserAlreadyExists:
        raise HTTPException(status_code=400, detail="Email already registered")

