from sqlalchemy import Column, String
from app.database import Base
from pydantic import BaseModel, EmailStr


class User(Base):
    __tablename__ = "users"

    email = Column(String(255), primary_key=True, index=True)
    hashed_password = Column(String(255), nullable=False)


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserInDB(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True
