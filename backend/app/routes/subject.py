# backend/app/routes/subject.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_session
from app.models.models import Subject
from app.schemas.subject import SubjectCreate, SubjectRead
from app.models.models import Subject
from app.utils import calculate_total_hours_for_subject

router = APIRouter(prefix="/subjects", tags=["subjects"])

@router.post("/", response_model=SubjectRead)
def create_subject(subject: SubjectCreate, session: Session = Depends(get_session)):
    db_subject = Subject(**subject.dict())
    session.add(db_subject)
    session.commit()
    session.refresh(db_subject)
    return db_subject

@router.get("/", response_model=list[SubjectRead])
def get_all_subjects(session: Session = Depends(get_session)):
    return session.query(Subject).all()

@router.get("/{subject_id}", response_model=SubjectRead)
def get_subject(subject_id: int, session: Session = Depends(get_session)):
    subject = session.query(Subject).get(subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@router.get("/with-hours", response_model=list[SubjectRead])
def get_subjects_with_hours(session: Session = Depends(get_session)):
    return session.query(Subject).all()

@router.get("/missing-hours")
def get_missing_hours(session: Session = Depends(get_session)):
    subjects = session.query(Subject).all()
    result = []
    for subject in subjects:
        total_hours = calculate_total_hours_for_subject(subject.subject_id, session)
        missing = subject.weekly_required_hours - total_hours
        status = (
            "complete" if missing == 0 else
            "exceeded" if missing < 0 else
            "missing"
        )
        result.append({
            "subject_id": subject.subject_id,
            "subject_name": subject.name,
            "required_hours": subject.weekly_required_hours,
            "assigned_hours": total_hours,
            "missing_hours": max(missing, 0),
            "status": status
        })
    return result