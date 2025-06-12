# app/routes/classgroups.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import ClassGroup
from app.schemas.classgroup import (
    ClassGroupCreate,
    ClassGroupUpdate,
    ClassGroupResponse,
)
from app.database import get_session

router = APIRouter(prefix="/classgroups", tags=["classgroups"])

@router.get("/", response_model=list[ClassGroupResponse])
def get_all_classgroups(session: Session = Depends(get_session)):
    return session.query(ClassGroup).all()

@router.get("/{group_id}", response_model=ClassGroupResponse)
def get_classgroup(group_id: int, session: Session = Depends(get_session)):
    group = session.get(ClassGroup, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="ClassGroup not found")
    return group

@router.post("/", response_model=ClassGroupResponse)
def create_classgroup(data: ClassGroupCreate, session: Session = Depends(get_session)):
    group = ClassGroup(**data.dict())
    session.add(group)
    session.commit()
    session.refresh(group)
    return group

@router.put("/{group_id}", response_model=ClassGroupResponse)
def update_classgroup(group_id: int, data: ClassGroupUpdate, session: Session = Depends(get_session)):
    group = session.get(ClassGroup, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="ClassGroup not found")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(group, key, value)
    session.commit()
    session.refresh(group)
    return group

@router.delete("/{group_id}")
def delete_classgroup(group_id: int, session: Session = Depends(get_session)):
    group = session.get(ClassGroup, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="ClassGroup not found")
    session.delete(group)
    session.commit()
    return {"ok": True}

