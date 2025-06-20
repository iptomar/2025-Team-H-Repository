from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.approval import ApprovalCreate, ApprovalUpdate, ApprovalResponse
from app.models.approval import Approval
from app.database import get_db

router = APIRouter(prefix="/approvals", tags=["approvals"])

@router.post("/", response_model=ApprovalResponse, status_code=status.HTTP_201_CREATED)
def create_approval(approval: ApprovalCreate, db: Session = Depends(get_db)):
    try:
        db_approval = Approval(**approval.dict())
        db.add(db_approval)
        db.commit()
        db.refresh(db_approval)
        return db_approval
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating approval: {str(e)}")

@router.get("/", response_model=List[ApprovalResponse])
def read_approvals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    approvals = db.query(Approval).offset(skip).limit(limit).all()
    return approvals

@router.get("/{approval_id}", response_model=ApprovalResponse)
def read_approval(approval_id: int, db: Session = Depends(get_db)):
    approval = db.query(Approval).filter(Approval.approval_id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")
    return approval

@router.put("/{approval_id}", response_model=ApprovalResponse)
def update_approval(approval_id: int, approval_update: ApprovalUpdate, db: Session = Depends(get_db)):
    db_approval = db.query(Approval).filter(Approval.approval_id == approval_id).first()
    if not db_approval:
        raise HTTPException(status_code=404, detail="Approval not found")
    try:
        for key, value in approval_update.dict(exclude_unset=True).items():
            setattr(db_approval, key, value)
        db.commit()
        db.refresh(db_approval)
        return db_approval
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating approval: {str(e)}")

@router.delete("/{approval_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_approval(approval_id: int, db: Session = Depends(get_db)):
    db_approval = db.query(Approval).filter(Approval.approval_id == approval_id).first()
    if not db_approval:
        raise HTTPException(status_code=404, detail="Approval not found")
    try:
        db.delete(db_approval)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting approval: {str(e)}")
    return None