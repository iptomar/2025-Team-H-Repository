from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.routes import auth
from app.routes import classes
from app.routes import timetable
from app.database import get_session, init_db
from app.models import models
from app.schemas import classes as schemas
from app.utils import get_password_hash
from fastapi.middleware.cors import CORSMiddleware


"""
Main application entry point for the IPT Timetables API.

This module initializes the FastAPI application and configures all routes.
The application provides endpoints for managing class schedules and user authentication.
"""

# Initialize FastAPI application with metadata
app = FastAPI(
    title="Horários IPT",
    description="Sistema de criação de horários",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Explicitly include OPTIONS
    allow_headers=["*"],
)


# Run once to init database
# init_db()

app.include_router(auth.router)
app.include_router(classes.router)
app.include_router(timetable.router)

@app.post("/locations/", response_model=schemas.Location)
def create_location(location: schemas.LocationCreate, db: Session = Depends(get_session)):
    db_location = models.Location(**location.model_dump())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

@app.get("/locations/", response_model=List[schemas.Location])
def read_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    locations = db.query(models.Location).offset(skip).limit(limit).all()
    return locations

@app.get("/locations/{location_id}", response_model=schemas.Location)
def read_location(location_id: int, db: Session = Depends(get_session)):
    location = db.query(models.Location).filter(models.Location.location_id == location_id).first()
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@app.put("/locations/{location_id}", response_model=schemas.Location)
def update_location(location_id: int, location: schemas.LocationUpdate, db: Session = Depends(get_session)):
    db_location = db.query(models.Location).filter(models.Location.location_id == location_id).first()
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    
    update_data = location.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_location, field, value)
    
    db.commit()
    db.refresh(db_location)
    return db_location

@app.delete("/locations/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_session)):
    location = db.query(models.Location).filter(models.Location.location_id == location_id).first()
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(location)
    db.commit()
    return {"message": "Location deleted successfully"}

# School endpoints
@app.post("/schools/", response_model=schemas.School)
def create_school(school: schemas.SchoolCreate, db: Session = Depends(get_session)):
    db_school = models.School(**school.model_dump())
    db.add(db_school)
    db.commit()
    db.refresh(db_school)
    return db_school

@app.get("/schools/", response_model=List[schemas.School])
def read_schools(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    schools = db.query(models.School).offset(skip).limit(limit).all()
    return schools

@app.get("/schools/{school_id}", response_model=schemas.School)
def read_school(school_id: int, db: Session = Depends(get_session)):
    school = db.query(models.School).filter(models.School.school_id == school_id).first()
    if school is None:
        raise HTTPException(status_code=404, detail="School not found")
    return school

@app.put("/schools/{school_id}", response_model=schemas.School)
def update_school(school_id: int, school: schemas.SchoolUpdate, db: Session = Depends(get_session)):
    db_school = db.query(models.School).filter(models.School.school_id == school_id).first()
    if db_school is None:
        raise HTTPException(status_code=404, detail="School not found")
    
    update_data = school.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_school, field, value)
    
    db.commit()
    db.refresh(db_school)
    return db_school

@app.delete("/schools/{school_id}")
def delete_school(school_id: int, db: Session = Depends(get_session)):
    school = db.query(models.School).filter(models.School.school_id == school_id).first()
    if school is None:
        raise HTTPException(status_code=404, detail="School not found")
    db.delete(school)
    db.commit()
    return {"message": "School deleted successfully"}

# User endpoints
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_session)):
    # Check if username already exists
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    user_data = user.model_dump()
    password = user_data.pop('password')
    user_data['password_hash'] = get_password_hash(password)
    
    db_user = models.User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_session)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_session)):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user.model_dump(exclude_unset=True)
    if 'password' in update_data:
        update_data['password_hash'] = get_password_hash(update_data.pop('password'))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_session)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# Course endpoints
@app.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_session)):
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.get("/courses/", response_model=List[schemas.Course])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    courses = db.query(models.Course).offset(skip).limit(limit).all()
    return courses

@app.get("/courses/{course_id}", response_model=schemas.Course)
def read_course(course_id: int, db: Session = Depends(get_session)):
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.put("/courses/{course_id}", response_model=schemas.Course)
def update_course(course_id: int, course: schemas.CourseUpdate, db: Session = Depends(get_session)):
    db_course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    update_data = course.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_course, field, value)
    
    db.commit()
    db.refresh(db_course)
    return db_course

@app.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_session)):
    course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}

# Subject endpoints
@app.post("/subjects/", response_model=schemas.Subject)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_session)):
    db_subject = models.Subject(**subject.model_dump())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

@app.get("/subjects/", response_model=List[schemas.Subject])
def read_subjects(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    subjects = db.query(models.Subject).offset(skip).limit(limit).all()
    return subjects

@app.get("/subjects/{subject_id}", response_model=schemas.Subject)
def read_subject(subject_id: int, db: Session = Depends(get_session)):
    subject = db.query(models.Subject).filter(models.Subject.subject_id == subject_id).first()
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@app.put("/subjects/{subject_id}", response_model=schemas.Subject)
def update_subject(subject_id: int, subject: schemas.SubjectUpdate, db: Session = Depends(get_session)):
    db_subject = db.query(models.Subject).filter(models.Subject.subject_id == subject_id).first()
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    update_data = subject.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_subject, field, value)
    
    db.commit()
    db.refresh(db_subject)
    return db_subject

@app.delete("/subjects/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_session)):
    subject = db.query(models.Subject).filter(models.Subject.subject_id == subject_id).first()
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    db.delete(subject)
    db.commit()
    return {"message": "Subject deleted successfully"}

# ClassGroup endpoints
@app.post("/class-groups/", response_model=schemas.ClassGroup)
def create_class_group(class_group: schemas.ClassGroupCreate, db: Session = Depends(get_session)):
    db_class_group = models.ClassGroup(**class_group.model_dump())
    db.add(db_class_group)
    db.commit()
    db.refresh(db_class_group)
    return db_class_group

@app.get("/class-groups/", response_model=List[schemas.ClassGroup])
def read_class_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    class_groups = db.query(models.ClassGroup).offset(skip).limit(limit).all()
    return class_groups

@app.get("/class-groups/{class_group_id}", response_model=schemas.ClassGroup)
def read_class_group(class_group_id: int, db: Session = Depends(get_session)):
    class_group = db.query(models.ClassGroup).filter(models.ClassGroup.class_group_id == class_group_id).first()
    if class_group is None:
        raise HTTPException(status_code=404, detail="Class group not found")
    return class_group

@app.put("/class-groups/{class_group_id}", response_model=schemas.ClassGroup)
def update_class_group(class_group_id: int, class_group: schemas.ClassGroupUpdate, db: Session = Depends(get_session)):
    db_class_group = db.query(models.ClassGroup).filter(models.ClassGroup.class_group_id == class_group_id).first()
    if db_class_group is None:
        raise HTTPException(status_code=404, detail="Class group not found")
    
    update_data = class_group.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_class_group, field, value)
    
    db.commit()
    db.refresh(db_class_group)
    return db_class_group

@app.delete("/class-groups/{class_group_id}")
def delete_class_group(class_group_id: int, db: Session = Depends(get_session)):
    class_group = db.query(models.ClassGroup).filter(models.ClassGroup.class_group_id == class_group_id).first()
    if class_group is None:
        raise HTTPException(status_code=404, detail="Class group not found")
    db.delete(class_group)
    db.commit()
    return {"message": "Class group deleted successfully"}

# Room endpoints
@app.post("/rooms/", response_model=schemas.Room)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_session)):
    db_room = models.Room(**room.model_dump())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@app.get("/rooms/", response_model=List[schemas.Room])
def read_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    rooms = db.query(models.Room).offset(skip).limit(limit).all()
    return rooms

@app.get("/rooms/{room_id}", response_model=schemas.Room)
def read_room(room_id: int, db: Session = Depends(get_session)):
    room = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@app.put("/rooms/{room_id}", response_model=schemas.Room)
def update_room(room_id: int, room: schemas.RoomUpdate, db: Session = Depends(get_session)):
    db_room = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    
    update_data = room.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_room, field, value)
    
    db.commit()
    db.refresh(db_room)
    return db_room

@app.delete("/rooms/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_session)):
    room = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(room)
    db.commit()
    return {"message": "Room deleted successfully"}

# TimetableVersion endpoints
@app.post("/timetable-versions/", response_model=schemas.TimetableVersion)
def create_timetable_version(version: schemas.TimetableVersionCreate, db: Session = Depends(get_session)):
    db_version = models.TimetableVersion(**version.model_dump())
    db.add(db_version)
    db.commit()
    db.refresh(db_version)
    return db_version

@app.get("/timetable-versions/", response_model=List[schemas.TimetableVersion])
def read_timetable_versions(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    versions = db.query(models.TimetableVersion).offset(skip).limit(limit).all()
    return versions

@app.get("/timetable-versions/{version_id}", response_model=schemas.TimetableVersion)
def read_timetable_version(version_id: int, db: Session = Depends(get_session)):
    version = db.query(models.TimetableVersion).filter(models.TimetableVersion.version_id == version_id).first()
    if version is None:
        raise HTTPException(status_code=404, detail="Timetable version not found")
    return version

@app.put("/timetable-versions/{version_id}", response_model=schemas.TimetableVersion)
def update_timetable_version(version_id: int, version: schemas.TimetableVersionUpdate, db: Session = Depends(get_session)):
    db_version = db.query(models.TimetableVersion).filter(models.TimetableVersion.version_id == version_id).first()
    if db_version is None:
        raise HTTPException(status_code=404, detail="Timetable version not found")
    
    update_data = version.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_version, field, value)
    
    db.commit()
    db.refresh(db_version)
    return db_version

@app.delete("/timetable-versions/{version_id}")
def delete_timetable_version(version_id: int, db: Session = Depends(get_session)):
    version = db.query(models.TimetableVersion).filter(models.TimetableVersion.version_id == version_id).first()
    if version is None:
        raise HTTPException(status_code=404, detail="Timetable version not found")
    db.delete(version)
    db.commit()
    return {"message": "Timetable version deleted successfully"}

# Class endpoints
@app.post("/classes/", response_model=schemas.Class)
def create_class(class_data: schemas.ClassCreate, db: Session = Depends(get_session)):
    class_dict = class_data.model_dump()
    class_group_ids = class_dict.pop('class_group_ids', [])
    
    db_class = models.Class(**class_dict)
    db.add(db_class)
    db.commit()
    
    # Add class groups
    if class_group_ids:
        class_groups = db.query(models.ClassGroup).filter(models.ClassGroup.class_group_id.in_(class_group_ids)).all()
        db_class.class_groups.extend(class_groups)
        db.commit()
    
    db.refresh(db_class)
    return db_class

@app.get("/classes/", response_model=List[schemas.Class])
def read_classes(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    classes = db.query(models.Class).offset(skip).limit(limit).all()
    return classes

@app.get("/classes/{class_id}", response_model=schemas.Class)
def read_class(class_id: int, db: Session = Depends(get_session)):
    class_obj = db.query(models.Class).filter(models.Class.class_id == class_id).first()
    if class_obj is None:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_obj

@app.put("/classes/{class_id}", response_model=schemas.Class)
def update_class(class_id: int, class_data: schemas.ClassUpdate, db: Session = Depends(get_session)):
    db_class = db.query(models.Class).filter(models.Class.class_id == class_id).first()
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    
    update_data = class_data.model_dump(exclude_unset=True)
    class_group_ids = update_data.pop('class_group_ids', None)
    
    for field, value in update_data.items():
        setattr(db_class, field, value)
    
    # Update class groups if provided
    if class_group_ids is not None:
        db_class.class_groups.clear()
        if class_group_ids:
            class_groups = db.query(models.ClassGroup).filter(models.ClassGroup.class_group_id.in_(class_group_ids)).all()
            db_class.class_groups.extend(class_groups)
    
    db.commit()
    db.refresh(db_class)
    return db_class

@app.delete("/classes/{class_id}")
def delete_class(class_id: int, db: Session = Depends(get_session)):
    class_obj = db.query(models.Class).filter(models.Class.class_id == class_id).first()
    if class_obj is None:
        raise HTTPException(status_code=404, detail="Class not found")
    db.delete(class_obj)
    db.commit()
    return {"message": "Class deleted successfully"}

# Unavailability endpoints
@app.post("/unavailabilities/", response_model=schemas.Unavailability)
def create_unavailability(unavailability: schemas.UnavailabilityCreate, db: Session = Depends(get_session)):
    db_unavailability = models.Unavailability(**unavailability.model_dump())
    db.add(db_unavailability)
    db.commit()
    db.refresh(db_unavailability)
    return db_unavailability

@app.get("/unavailabilities/", response_model=List[schemas.Unavailability])
def read_unavailabilities(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    unavailabilities = db.query(models.Unavailability).offset(skip).limit(limit).all()
    return unavailabilities

@app.get("/unavailabilities/{unavailability_id}", response_model=schemas.Unavailability)
def read_unavailability(unavailability_id: int, db: Session = Depends(get_session)):
    unavailability = db.query(models.Unavailability).filter(models.Unavailability.unavailability_id == unavailability_id).first()
    if unavailability is None:
        raise HTTPException(status_code=404, detail="Unavailability not found")
    return unavailability

@app.put("/unavailabilities/{unavailability_id}", response_model=schemas.Unavailability)
def update_unavailability(unavailability_id: int, unavailability: schemas.UnavailabilityUpdate, db: Session = Depends(get_session)):
    db_unavailability = db.query(models.Unavailability).filter(models.Unavailability.unavailability_id == unavailability_id).first()
    if db_unavailability is None:
        raise HTTPException(status_code=404, detail="Unavailability not found")
    
    update_data = unavailability.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_unavailability, field, value)
    
    db.commit()
    db.refresh(db_unavailability)
    return db_unavailability

@app.delete("/unavailabilities/{unavailability_id}")
def delete_unavailability(unavailability_id: int, db: Session = Depends(get_session)):
    unavailability = db.query(models.Unavailability).filter(models.Unavailability.unavailability_id == unavailability_id).first()
    if unavailability is None:
        raise HTTPException(status_code=404, detail="Unavailability not found")
    db.delete(unavailability)
    db.commit()
    return {"message": "Unavailability deleted successfully"}

# CalendarEvent endpoints
@app.post("/calendar-events/", response_model=schemas.CalendarEvent)
def create_calendar_event(event: schemas.CalendarEventCreate, db: Session = Depends(get_session)):
    db_event = models.CalendarEvent(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.get("/calendar-events/", response_model=List[schemas.CalendarEvent])
def read_calendar_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    events = db.query(models.CalendarEvent).offset(skip).limit(limit).all()
    return events

@app.get("/calendar-events/{event_id}", response_model=schemas.CalendarEvent)
def read_calendar_event(event_id: int, db: Session = Depends(get_session)):
    event = db.query(models.CalendarEvent).filter(models.CalendarEvent.event_id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Calendar event not found")
    return event

@app.put("/calendar-events/{event_id}", response_model=schemas.CalendarEvent)
def update_calendar_event(event_id: int, event: schemas.CalendarEventUpdate, db: Session = Depends(get_session)):
    db_event = db.query(models.CalendarEvent).filter(models.CalendarEvent.event_id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Calendar event not found")
    
    update_data = event.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event, field, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event

@app.delete("/calendar-events/{event_id}")
def delete_calendar_event(event_id: int, db: Session = Depends(get_session)):
    event = db.query(models.CalendarEvent).filter(models.CalendarEvent.event_id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Calendar event not found")
    db.delete(event)
    db.commit()
    return {"message": "Calendar event deleted successfully"}

# Approval endpoints
@app.post("/approvals/", response_model=schemas.Approval)
def create_approval(approval: schemas.ApprovalCreate, db: Session = Depends(get_session)):
    db_approval = models.Approval(**approval.model_dump())
    db.add(db_approval)
    db.commit()
    db.refresh(db_approval)
    return db_approval

@app.get("/approvals/", response_model=List[schemas.Approval])
def read_approvals(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    approvals = db.query(models.Approval).offset(skip).limit(limit).all()
    return approvals

@app.get("/approvals/{approval_id}", response_model=schemas.Approval)
def read_approval(approval_id: int, db: Session = Depends(get_session)):
    approval = db.query(models.Approval).filter(models.Approval.approval_id == approval_id).first()
    if approval is None:
        raise HTTPException(status_code=404, detail="Approval not found")
    return approval

@app.put("/approvals/{approval_id}/respond", response_model=schemas.Approval)
def respond_to_approval(approval_id: int, response: schemas.ApprovalResponse, db: Session = Depends(get_session)):
    db_approval = db.query(models.Approval).filter(models.Approval.approval_id == approval_id).first()
    if db_approval is None:
        raise HTTPException(status_code=404, detail="Approval not found")
    
    if db_approval.status != schemas.ApprovalStatus.pending:
        raise HTTPException(status_code=400, detail="Approval has already been responded to")
    
    db_approval.approved_by = response.approved_by
    db_approval.status = response.status
    db_approval.response_date = datetime.now()
    if response.notes:
        db_approval.notes = response.notes
    
    db.commit()
    db.refresh(db_approval)
    return db_approval

@app.delete("/approvals/{approval_id}")
def delete_approval(approval_id: int, db: Session = Depends(get_session)):
    approval = db.query(models.Approval).filter(models.Approval.approval_id == approval_id).first()
    if approval is None:
        raise HTTPException(status_code=404, detail="Approval not found")
    db.delete(approval)
    db.commit()
    return {"message": "Approval deleted successfully"}

# Additional utility endpoints
@app.get("/users/{user_id}/classes", response_model=List[schemas.Class])
def get_user_classes(user_id: int, db: Session = Depends(get_session)):
    """Get all classes taught by a specific user"""
    classes = db.query(models.Class).filter(models.Class.teacher_id == user_id).all()
    return classes

@app.get("/rooms/{room_id}/classes", response_model=List[schemas.Class])
def get_room_classes(room_id: int, db: Session = Depends(get_session)):
    """Get all classes scheduled in a specific room"""
    classes = db.query(models.Class).filter(models.Class.room_id == room_id).all()
    return classes

@app.get("/subjects/{subject_id}/classes", response_model=List[schemas.Class])
def get_subject_classes(subject_id: int, db: Session = Depends(get_session)):
    """Get all classes for a specific subject"""
    classes = db.query(models.Class).filter(models.Class.subject_id == subject_id).all()
    return classes

@app.get("/users/{user_id}/unavailabilities", response_model=List[schemas.Unavailability])
def get_user_unavailabilities(user_id: int, db: Session = Depends(get_session)):
    """Get all unavailabilities for a specific user"""
    unavailabilities = db.query(models.Unavailability).filter(models.Unavailability.teacher_id == user_id).all()
    return unavailabilities

@app.get("/approvals/pending", response_model=List[schemas.Approval])
def get_pending_approvals(db: Session = Depends(get_session)):
    """Get all pending approvals"""
    approvals = db.query(models.Approval).filter(models.Approval.status == schemas.ApprovalStatus.pending).all()
    return approvals
