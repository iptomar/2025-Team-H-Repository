from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models import User as UserModel
from app.schemas import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return session.exec(select(UserModel).offset(skip).limit(limit)).all()


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse)
def create_user(user_in: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(UserModel).where(UserModel.username == user_in.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = pwd_context.hash(user_in.password)
    user_obj = UserModel(
        username=user_in.username,
        password_hash=hashed_password,
        role=user_in.role,
        school_id=user_in.school_id,
        course_id=user_in.course_id,
    )
    session.add(user_obj)
    session.commit()
    session.refresh(user_obj)
    return user_obj


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_in: UserUpdate, session: Session = Depends(get_session)):
    user = session.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_in.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password_hash"] = pwd_context.hash(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(user, key, value)

    session.commit()
    session.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}
