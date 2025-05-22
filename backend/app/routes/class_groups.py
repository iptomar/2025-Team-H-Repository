from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.class_group import ClassGroupCreate, ClassGroupUpdate, ClassGroupResponse
from app.models.class_group import ClassGroup
from app.database import get_db

router = APIRouter(prefix="/class_groups", tags=["class_groups"])

@router.post("/", response_model=ClassGroupResponse, status_code=status.HTTP_201_CREATED)
def create_class_group(class_group: ClassGroupCreate, db: Session = Depends(get_db)):
    try:
        db_class_group = ClassGroup(**class_group.dict())
        db.add(db_class_group)
        db.commit()
        db.refresh(db_class_group)
        return db_class_group
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating class group: {str(e)}")

@router.get("/", response_model=List[ClassGroupResponse])
def read_class_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    class_groups = db.query(ClassGroup).offset(skip).limit(limit).all()
    return class_groups

@router.get("/{class_group_id}", response_model=ClassGroupResponse)
def read_class_group(class_group_id: int, db: Session = Depends(get_db)):
    class_group = db.query(ClassGroup).filter(ClassGroup.class_group_id == class_group_id).first()
    if not class_group:
        raise HTTPException(status_code=404, detail="Class group not found")
    return class_group

@router.put("/{class_group_id}", response_model=ClassGroupResponse)
def update_class_group(class_group_id: int, class_group_update: ClassGroupUpdate, db: Session = Depends(get_db)):
    db_class_group = db.query(ClassGroup).filter(ClassGroup.class_group_id == class_group_id).first()
    if not db_class_group:
        raise HTTPException(status_code=404, detail="Class group not found")
    try:
        for key, value in class_group_update.dict(exclude_unset=True).items():
            setattr(db_class_group, key, value)
        db.commit()
        db.refresh(db_class_group)
        return db_class_group
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating class group: {str(e)}")

@router.delete("/{class_group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class_group(class_group_id: int, db: Session = Depends(get_db)):
    db_class_group = db.query(ClassGroup).filter(ClassGroup.class_group_id == class_group_id).first()
    if not db_class_group:
        raise HTTPException(status_code=404, detail="Class group not found")
    try:
        db.delete(db_class_group)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting class group: {str(e)}")
    return None