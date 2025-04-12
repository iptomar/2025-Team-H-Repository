from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.timetable import Timetable
from app.schemas.timetable import TimetableCreate, TimetableInDB

router = APIRouter(prefix="/timetables", tags=["timetables"])

# CREATE
@router.post("/", response_model=TimetableInDB)
def create_timetable(timetable: TimetableCreate, db: Session = Depends(get_db)):
    db_tt = Timetable(**timetable.dict())
    db.add(db_tt)
    db.commit()
    db.refresh(db_tt)
    return db_tt

# READ ALL
@router.get("/", response_model=list[TimetableInDB])
def get_all_timetables(db: Session = Depends(get_db)):
    return db.query(Timetable).all()

# READ ONE
@router.get("/{timetable_id}", response_model=TimetableInDB)
def get_timetable(timetable_id: int, db: Session = Depends(get_db)):
    db_tt = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if not db_tt:
        raise HTTPException(status_code=404, detail="Timetable not found")
    return db_tt

# UPDATE
@router.put("/{timetable_id}", response_model=TimetableInDB)
def update_timetable(timetable_id: int, updated_tt: TimetableCreate, db: Session = Depends(get_db)):
    db_tt = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if not db_tt:
        raise HTTPException(status_code=404, detail="Timetable not found")
    for key, value in updated_tt.dict().items():
        setattr(db_tt, key, value)
    db.commit()
    db.refresh(db_tt)
    return db_tt

# DELETE
@router.delete("/{timetable_id}", status_code=204)
def delete_timetable(timetable_id: int, db: Session = Depends(get_db)):
    db_tt = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if not db_tt:
        raise HTTPException(status_code=404, detail="Timetable not found")
    db.delete(db_tt)
    db.commit()
