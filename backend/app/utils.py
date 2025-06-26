from passlib.context import CryptContext
from typing import Optional
from sqlmodel import Session
from app.database import get_db
from app.models.models import User
from app.models.models import Class
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"])


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def calculate_total_hours_for_subject(subject_id: int, session):
    classes = session.query(Class).filter(Class.subject_id == subject_id).all()
    total_minutes = 0
    for cls in classes:
        start = datetime.combine(datetime.today(), cls.start_time)
        end = datetime.combine(datetime.today(), cls.end_time)
        total_minutes += int((end - start).total_seconds() // 60)
    return total_minutes / 60  # convert to hours

