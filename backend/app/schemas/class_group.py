from pydantic import BaseModel, PositiveInt, conint
from typing import Optional

class ClassGroupBase(BaseModel):
    subject_id: PositiveInt
    group_number: PositiveInt
    enrollment_count: conint(ge=0)  # Garante enrollment_count >= 0
    location_id: PositiveInt

class ClassGroupCreate(ClassGroupBase):
    pass

class ClassGroupUpdate(ClassGroupBase):
    subject_id: Optional[PositiveInt] = None
    group_number: Optional[PositiveInt] = None
    enrollment_count: Optional[conint(ge=0)] = None
    location_id: Optional[PositiveInt] = None

class ClassGroupResponse(ClassGroupBase):
    class_group_id: PositiveInt

    class Config:
        orm_mode = True  # Alinhado com ClassResponse (Pydantic v1)