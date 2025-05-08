from pydantic import BaseModel
from datetime import datetime

# Base fields shared by create/update/read
class TimetableBase(BaseModel):
    course_id: int
    subject_id: int
    room_id: int
    professor_id: int
    start_time: datetime
    end_time: datetime

# Schema for creating a timetable (POST body)
class TimetableCreate(TimetableBase):
    pass

# Schema for reading/returning a timetable (includes ID)
class TimetableInDB(TimetableBase):
    id: int

    class Config:
        orm_mode = True  # Allows returning SQLAlchemy models directly
