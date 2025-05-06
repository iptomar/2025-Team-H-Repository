from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select  # Use sqlmodel instead of sqlalchemy.orm
from app.database import get_session
from app.models import Class as ClassModel
from app.schemas import ClassCreate, ClassUpdate, ClassResponse

router = APIRouter(prefix="/classes", tags=["classes"])

@router.get("/", response_model=list[ClassResponse])
def read_classes(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return session.exec(select(ClassModel).offset(skip).limit(limit)).all()

@router.get("/{class_id}", response_model=ClassResponse)
def read_class(class_id: int, session: Session = Depends(get_session)):
    class_obj = session.get(ClassModel, class_id)
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_obj

@router.post("/", response_model=ClassResponse)
def create_class(class_in: ClassCreate, session: Session = Depends(get_session)):
    class_obj = ClassModel(**class_in.dict())
    session.add(class_obj)
    session.commit()
    session.refresh(class_obj)
    return class_obj

@router.put("/{class_id}", response_model=ClassResponse)
def update_class(class_id: int, class_in: ClassUpdate, session: Session = Depends(get_session)):
    class_obj = session.get(ClassModel, class_id)
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    for field, value in class_in.dict(exclude_unset=True).items():
        setattr(class_obj, field, value)
    session.commit()
    session.refresh(class_obj)
    return class_obj

@router.delete("/{class_id}")
def delete_class(class_id: int, session: Session = Depends(get_session)):
    class_obj = session.get(ClassModel, class_id)
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    session.delete(class_obj)
    session.commit()
    return {"ok": True}