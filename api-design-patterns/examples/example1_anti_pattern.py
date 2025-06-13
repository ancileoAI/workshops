from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from passlib.hash import bcrypt

app = FastAPI()
Base = declarative_base()
engine = create_engine("sqlite:///./test.db")
SessionLocal = lambda: Session(bind=engine)


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


@app.post("/register")
def register(user: UserCreate):
    db = SessionLocal()

    # 1. Validation and logic mixed into endpoint
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Password hashing logic in endpoint
    hashed_pw = bcrypt.hash(user.password)

    # 3. DB model creation here
    new_user = User(email=user.email, name=user.name, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    # 4. Synchronous side effect (no background task)
    send_welcome_email(new_user.email)  # imaginary blocking function

    return {
        "id": new_user.id,
        "email": new_user.email,
        "name": new_user.name,
    }


def send_welcome_email(email: str):
    print(f"Sending welcome email to {email}...")

