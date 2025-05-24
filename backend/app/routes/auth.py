from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.models.models import User, UserRole
from datetime import datetime
from typing import Optional
import hashlib
import uuid
from pydantic import BaseModel
from app.database import get_session 

router = APIRouter(prefix="/auth", tags=["auth"])

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Pydantic models for request/response
class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole
    school_id: Optional[int] = None
    course_id: Optional[int] = None

class UserResponse(BaseModel):
    user_id: int
    username: str
    role: UserRole
    school_id: Optional[int]
    course_id: Optional[int]

class Token(BaseModel):
    access_token: str
    token_type: str

# Helper functions
def hash_password(password: str) -> str:
    """Hash password using SHA-256 (simple, not recommended for production)."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password by comparing hashes."""
    return hash_password(plain_password) == hashed_password

def generate_token() -> str:
    """Generate a unique token using UUID."""
    return str(uuid.uuid4())

async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    """Retrieve the current user based on the token."""
    user = session.exec(select(User).where(User.token == token)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Ensure the user is active."""
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Endpoints
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, session: Session = Depends(get_session)):
    """Register a new user."""
    # Check if username already exists
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Validate role constraints based on User model
    if user.role == UserRole.School_Timetable_Committee and user.school_id is None:
        raise HTTPException(status_code=400, detail="School Timetable Committee members must have a school_id")
    if user.role == UserRole.Course_Timetable_Committee and user.course_id is None:
        raise HTTPException(status_code=400, detail="Course Timetable Committee members must have a course_id")

    # Create new user
    db_user = User(
        username=user.username,
        password_hash=hash_password(user.password),
        role=user.role,
        school_id=user.school_id,
        course_id=user.course_id,
        token=generate_token()  # Generate initial token
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return UserResponse(
        user_id=db_user.user_id,
        username=db_user.username,
        role=db_user.role,
        school_id=db_user.school_id,
        course_id=db_user.course_id
    )

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """Authenticate user and generate a new token."""
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate new token and update user
    new_token = generate_token()
    user.token = new_token
    session.add(user)
    session.commit()

    return Token(
        access_token=new_token,
        token_type="bearer"
    )

@router.get("/token_checker", response_model=UserResponse)
async def token_checker(current_user: User = Depends(get_current_active_user)):
    """Verify token and return user details."""
    return UserResponse(
        user_id=current_user.user_id,
        username=current_user.username,
        role=current_user.role,
        school_id=current_user.school_id,
        course_id=current_user.course_id
    )