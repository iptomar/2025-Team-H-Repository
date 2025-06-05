from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.models import ActionLog
from app.schemas.classes import ActionLogCreate, ActionLogResponse

# Create a router for log-related endpoints
router = APIRouter(prefix="/logs", tags=["logs"])

# GET /logs - Retrieve all logs (admin-only in the future)
@router.get("/", response_model=list[ActionLogResponse])
def get_logs(session: Session = Depends(get_session)):
    """
    Retrieve all action logs from the database.
    In the future, this endpoint may be restricted to admin users only.
    """
    logs = session.exec(select(ActionLog)).all()
    return logs

# POST /logs - Create a new log entry
@router.post("/", response_model=ActionLogResponse)
def create_log(log_in: ActionLogCreate, session: Session = Depends(get_session)):
    """
    Create a new action log entry in the database.
    """
    new_log = ActionLog(**log_in.dict())
    session.add(new_log)
    session.commit()
    session.refresh(new_log)
    return new_log