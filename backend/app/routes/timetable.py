from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_session
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/timetable", tags=["timetable"])

# Simple event model for demonstration
class TimetableEvent(BaseModel):
    id: Optional[int] = None
    title: str
    start: str
    end: str
    backgroundColor: Optional[str] = None
    extendedProps: Optional[dict] = None

# In-memory store for demo (replace with DB in production)
events_db: List[TimetableEvent] = []

@router.get("/events", response_model=List[TimetableEvent])
def get_events():
    return events_db

@router.post("/events", response_model=TimetableEvent)
def create_event(event: TimetableEvent):
    event.id = len(events_db) + 1
    events_db.append(event)
    return event

@router.put("/events/{event_id}", response_model=TimetableEvent)
def update_event(event_id: int, event: TimetableEvent):
    for idx, e in enumerate(events_db):
        if e.id == event_id:
            events_db[idx] = event
            events_db[idx].id = event_id
            return events_db[idx]
    raise HTTPException(status_code=404, detail="Event not found")

@router.delete("/events/{event_id}")
def delete_event(event_id: int):
    global events_db
    events_db = [e for e in events_db if e.id != event_id]
    return {"message": "Event deleted"} 