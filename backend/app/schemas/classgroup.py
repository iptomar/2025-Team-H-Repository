from pydantic import BaseModel
from typing import Optional

class ClassGroupBase(BaseModel):
    subject_id: int
    group_number: int
    enrollment_count: int
    location_id: int

class ClassGroupCreate(ClassGroupBase):
    pass

class ClassGroupUpdate(BaseModel):
    group_number: Optional[int] = None
    enrollment_count: Optional[int] = None
    location_id: Optional[int] = None

class ClassGroupResponse(ClassGroupBase):
    class_group_id: int

    class Config:
        orm_mode = True
