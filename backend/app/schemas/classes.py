from __future__ import annotations

from pydantic import BaseModel, Field
from datetime import date, time , datetime
from typing import Optional, List
from enum import Enum

# Mirror the Enum types from models
class ClassTypeEnum(str, Enum):
    P = "P"
    T = "T"
    TP = "TP"

class ApprovalStatusEnum(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

# Base schema shared properties
class ClassBase(BaseModel):
    subject_id: int
    class_type: ClassTypeEnum
    teacher_id: int
    room_id: int
    start_time: time
    end_time: time
    is_recurring: bool = True
    approval_status: ApprovalStatusEnum = ApprovalStatusEnum.approved
    version_id: Optional[int] = None
    # For recurring
    day_of_week: Optional[int] = Field(None, ge=1, le=7)
    # For non-recurring
    date: Optional[date] = None
    # Many-to-many class_groups by their IDs
    class_group_ids: Optional[List[int]] = None

# Schema for creation (all required except IDs)
class ClassCreate(ClassBase):
    pass

# Schema for update (all fields optional)
class ClassUpdate(BaseModel):
    subject_id: Optional[int]
    class_type: Optional[ClassTypeEnum]
    teacher_id: Optional[int]
    room_id: Optional[int]
    start_time: Optional[time]
    end_time: Optional[time]
    is_recurring: Optional[bool]
    approval_status: Optional[ApprovalStatusEnum]
    version_id: Optional[int]
    day_of_week: Optional[int] = Field(None, ge=1, le=7)
    date: Optional[date]
    class_group_ids: Optional[List[int]]

# Schema for response
class ClassResponse(ClassBase):
    class_id: int

    class Config:
        orm_mode = True


# schema ActionLog (for logging user actions)
class ActionLogBase(BaseModel):
    action: str
    details: Optional[str] = None

class ActionLogCreate(ActionLogBase):
    user_id: int

class ActionLogResponse(ActionLogBase):
    id: int
    user_id: int
    timestamp: datetime

    class Config:
        orm_mode = True
