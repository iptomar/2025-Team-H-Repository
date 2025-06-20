from pydantic import BaseModel, PositiveInt
from typing import Optional
from datetime import datetime
from app.models.enums import ApprovalStatus

class ApprovalBase(BaseModel):
    class_id: PositiveInt
    requested_by: PositiveInt
    approved_by: Optional[PositiveInt] = None
    status: ApprovalStatus = ApprovalStatus.pending

class ApprovalCreate(ApprovalBase):
    pass

class ApprovalUpdate(ApprovalBase):
    class_id: Optional[PositiveInt] = None
    requested_by: Optional[PositiveInt] = None
    status: Optional[ApprovalStatus] = None

class ApprovalResponse(ApprovalBase):
    approval_id: PositiveInt
    request_date: datetime

    class Config:
        orm_mode = True  # Alinhado com ClassResponse (Pydantic v1)