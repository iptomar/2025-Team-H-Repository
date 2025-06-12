# backend/app/schemas/subject.py

from pydantic import BaseModel

class SubjectBase(BaseModel):
    name: str
    course_id: int
    weekly_required_hours: int = 2

class SubjectCreate(SubjectBase):
    pass

class SubjectRead(SubjectBase):
    subject_id: int

    class Config:
        orm_mode = True
