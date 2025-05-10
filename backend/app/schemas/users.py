from typing import Optional
from pydantic import BaseModel, constr
from enum import Enum


class UserRole(str, Enum):
    Administrator = "Administrator"
    School_Timetable_Committee = "School_Timetable_Committee"
    Course_Timetable_Committee = "Course_Timetable_Committee"
    Teacher = "Teacher"


class UserBase(BaseModel):
    username: str
    role: UserRole
    school_id: Optional[int] = None
    course_id: Optional[int] = None


class UserCreate(UserBase):
    password: constr(min_length=6)


class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    role: Optional[UserRole]
    school_id: Optional[int]
    course_id: Optional[int]


class UserResponse(UserBase):
    user_id: int

    class Config:
        orm_mode = True
