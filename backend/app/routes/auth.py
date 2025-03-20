from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User, UserCreate, UserInDB
from app.utils import get_db, get_password_hash, get_user, verify_password
from typing import Dict

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserInDB)
def register(user: UserCreate, db: Session = Depends(get_db)) -> UserInDB:
    db_user = get_user(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=Dict[str, str])
def login(user: UserCreate, db: Session = Depends(get_db)) -> Dict[str, str]:
    db_user = get_user(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Login successful", "email": user.email}
