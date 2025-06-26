from datetime import datetime, date, time
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from enum import Enum


# Enums
class UserRole(str, Enum):
    Administrator = "Administrator"
    School_Timetable_Committee = "School_Timetable_Committee"
    Course_Timetable_Committee = "Course_Timetable_Committee"
    Teacher = "Teacher"


class ClassType(str, Enum):
    P = "P"
    T = "T"
    TP = "TP"


class ApprovalStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class EventType(str, Enum):
    holiday = "holiday"
    break_ = "break"
    other = "other"


class TimetablePhase(str, Enum):
    proposal = "proposal"
    adjustment = "adjustment"


# Base schemas
class LocationBase(BaseModel):
    name: str
    is_campus: bool = False


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    is_campus: Optional[bool] = None


class Location(LocationBase):
    model_config = ConfigDict(from_attributes=True)
    location_id: int


class SchoolBase(BaseModel):
    name: str
    location_id: int


class SchoolCreate(SchoolBase):
    pass


class SchoolUpdate(BaseModel):
    name: Optional[str] = None
    location_id: Optional[int] = None


class School(SchoolBase):
    model_config = ConfigDict(from_attributes=True)
    school_id: int
    location: Optional[Location] = None


class UserBase(BaseModel):
    username: str
    role: UserRole
    school_id: Optional[int] = None
    course_id: Optional[int] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    role: Optional[UserRole] = None
    school_id: Optional[int] = None
    course_id: Optional[int] = None
    password: Optional[str] = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    school: Optional[School] = None


class CourseBase(BaseModel):
    name: str
    school_id: int
    is_short_course: bool = False


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    school_id: Optional[int] = None
    is_short_course: Optional[bool] = None


class Course(CourseBase):
    model_config = ConfigDict(from_attributes=True)
    course_id: int
    school: Optional[School] = None


class SubjectBase(BaseModel):
    name: str
    course_id: int


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    course_id: Optional[int] = None


class Subject(SubjectBase):
    model_config = ConfigDict(from_attributes=True)
    subject_id: int
    course: Optional[Course] = None


class ClassGroupBase(BaseModel):
    subject_id: int
    group_number: int
    enrollment_count: int = 0
    location_id: int


class ClassGroupCreate(ClassGroupBase):
    pass


class ClassGroupUpdate(BaseModel):
    subject_id: Optional[int] = None
    group_number: Optional[int] = None
    enrollment_count: Optional[int] = None
    location_id: Optional[int] = None


class ClassGroup(ClassGroupBase):
    model_config = ConfigDict(from_attributes=True)
    class_group_id: int
    subject: Optional[Subject] = None
    location: Optional[Location] = None


class RoomBase(BaseModel):
    name: str
    capacity: int
    location_id: int
    owner_course_id: Optional[int] = None


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    name: Optional[str] = None
    capacity: Optional[int] = None
    location_id: Optional[int] = None
    owner_course_id: Optional[int] = None


class Room(RoomBase):
    model_config = ConfigDict(from_attributes=True)
    room_id: int
    location: Optional[Location] = None
    owner_course: Optional[Course] = None


class TimetableVersionBase(BaseModel):
    created_by: int
    phase: TimetablePhase
    description: Optional[str] = None


class TimetableVersionCreate(TimetableVersionBase):
    pass


class TimetableVersionUpdate(BaseModel):
    phase: Optional[TimetablePhase] = None
    description: Optional[str] = None


class TimetableVersion(TimetableVersionBase):
    model_config = ConfigDict(from_attributes=True)
    version_id: int
    creation_date: datetime
    creator: Optional[User] = None


class ClassBase(BaseModel):
    subject_id: int
    class_type: ClassType
    teacher_id: int
    room_id: int
    day_of_week: Optional[int] = None
    date: Optional[date] = None
    start_time: time
    end_time: time
    is_recurring: bool = True
    approval_status: ApprovalStatus = ApprovalStatus.approved
    version_id: Optional[int] = None


class ClassCreate(ClassBase):
    class_group_ids: List[int] = []


class ClassUpdate(BaseModel):
    subject_id: Optional[int] = None
    class_type: Optional[ClassType] = None
    teacher_id: Optional[int] = None
    room_id: Optional[int] = None
    day_of_week: Optional[int] = None
    date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_recurring: Optional[bool] = None
    approval_status: Optional[ApprovalStatus] = None
    version_id: Optional[int] = None
    class_group_ids: Optional[List[int]] = None


class Class(ClassBase):
    model_config = ConfigDict(from_attributes=True)
    class_id: int
    subject: Optional[Subject] = None
    teacher: Optional[User] = None
    room: Optional[Room] = None
    version: Optional[TimetableVersion] = None
    class_groups: List[ClassGroup] = []


class UnavailabilityBase(BaseModel):
    teacher_id: int
    day_of_week: Optional[int] = None
    date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_full_day: bool = False


class UnavailabilityCreate(UnavailabilityBase):
    pass


class UnavailabilityUpdate(BaseModel):
    teacher_id: Optional[int] = None
    day_of_week: Optional[int] = None
    date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_full_day: Optional[bool] = None


class Unavailability(UnavailabilityBase):
    model_config = ConfigDict(from_attributes=True)
    unavailability_id: int
    teacher: Optional[User] = None


class CalendarEventBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    type: EventType


class CalendarEventCreate(CalendarEventBase):
    pass


class CalendarEventUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    type: Optional[EventType] = None


class CalendarEvent(CalendarEventBase):
    model_config = ConfigDict(from_attributes=True)
    event_id: int


class ApprovalBase(BaseModel):
    class_id: int
    requested_by: int
    notes: Optional[str] = None


class ApprovalCreate(ApprovalBase):
    pass


class ApprovalUpdate(BaseModel):
    status: Optional[ApprovalStatus] = None
    notes: Optional[str] = None


class ApprovalResponse(BaseModel):
    approved_by: int
    status: ApprovalStatus
    notes: Optional[str] = None


class Approval(ApprovalBase):
    model_config = ConfigDict(from_attributes=True)
    approval_id: int
    approved_by: Optional[int] = None
    status: ApprovalStatus
    request_date: datetime
    response_date: Optional[datetime] = None
    requester: Optional[User] = None
    approver: Optional[User] = None
    class_: Optional[Class] = None
