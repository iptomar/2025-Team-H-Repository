from passlib.context import CryptContext
from typing import Optional
from sqlmodel import Session
from app.database import get_db
from app.models.models import User

pwd_context = CryptContext(schemes=["bcrypt"])


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()
