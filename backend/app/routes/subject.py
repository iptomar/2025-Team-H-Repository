# backend/app/routes/subject.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_session
from app.models.models import Subject
from app.schemas.subject import SubjectCreate, SubjectRead

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
