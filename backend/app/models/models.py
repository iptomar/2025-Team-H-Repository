from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from . import Base

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Date,
    Time,
    ForeignKey,
    CheckConstraint,
    Index,
    UniqueConstraint,
    Text,
    Table,
)
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Enum as SQLEnum

if TYPE_CHECKING:
    from sqlalchemy.orm import Mapped

# Enums
class UserRole(str, Enum):
    Administrator = "Administrator"
    School_Timetable_Committee = "School_Timetable_Committee"
    Course_Timetable_Committee = "Course_Timetable_Committee"
    Teacher = "Teacher"


class ClassType(str, Enum):
    P = "P"  # Practical
    T = "T"  # Theoretical
    TP = "TP"  # Theoretical-Practical


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


# Models
class Location(Base):
    __tablename__ = "locations"

    location_id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False, index=True)
    is_campus = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    schools = relationship("School", back_populates="location")
    rooms = relationship("Room", back_populates="location")
    class_groups = relationship("ClassGroup", back_populates="location")


class School(Base):
    __tablename__ = "schools"

    school_id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), nullable=False, index=True)
    location_id = mapped_column(
        Integer, ForeignKey("locations.location_id"), nullable=False
    )

    # Relationships
    location = relationship("Location", back_populates="schools")
    courses = relationship("Course", back_populates="school")
    users = relationship("User", back_populates="school")


class User(Base):
    __tablename__ = "users"

    user_id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(50), nullable=False, unique=True, index=True)
    password_hash = mapped_column(String(255), nullable=False)
    role = mapped_column(SQLEnum(UserRole), nullable=False)
    school_id = mapped_column(Integer, ForeignKey("schools.school_id"), nullable=True)
    course_id = mapped_column(Integer, ForeignKey("courses.course_id"), nullable=True)

    # Relationships
    school = relationship("School", back_populates="users")
    course = relationship("Course", back_populates="users")
    taught_classes = relationship("Class", back_populates="teacher")
    unavailabilities = relationship("Unavailability", back_populates="teacher")
    created_versions = relationship("TimetableVersion", back_populates="creator")
    requested_approvals = relationship(
        "Approval", foreign_keys="[Approval.requested_by]", back_populates="requester"
    )
    given_approvals = relationship(
        "Approval", foreign_keys="[Approval.approved_by]", back_populates="approver"
    )

    __table_args__ = (
        CheckConstraint(
            "(role != 'School_Timetable_Committee') OR (school_id IS NOT NULL)",
            name="chk_role_school",
        ),
        CheckConstraint(
            "(role != 'Course_Timetable_Committee') OR (course_id IS NOT NULL)",
            name="chk_role_course",
        ),
    )


class Course(Base):
    __tablename__ = "courses"

    course_id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False, index=True)
    school_id = mapped_column(Integer, ForeignKey("schools.school_id"), nullable=False)
    is_short_course = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    school = relationship("School", back_populates="courses")
    subjects = relationship("Subject", back_populates="course")
    owned_rooms = relationship("Room", back_populates="owner_course")
    users = relationship("User", back_populates="course")


class Subject(Base):
    __tablename__ = "subjects"

    subject_id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False, index=True)
    course_id = mapped_column(Integer, ForeignKey("courses.course_id"), nullable=False)

    # Relationships
    course = relationship("Course", back_populates="subjects")
    class_groups = relationship("ClassGroup", back_populates="subject")
    classes = relationship("Class", back_populates="subject")


class ClassGroup(Base):
    __tablename__ = "class_groups"

    class_group_id = mapped_column(Integer, primary_key=True)
    subject_id = mapped_column(
        Integer, ForeignKey("subjects.subject_id"), nullable=False
    )
    group_number = mapped_column(Integer, nullable=False)
    enrollment_count = mapped_column(Integer, default=0, nullable=False)
    location_id = mapped_column(
        Integer, ForeignKey("locations.location_id"), nullable=False
    )

    # Relationships
    subject = relationship("Subject", back_populates="class_groups")
    location = relationship("Location", back_populates="class_groups")
    classes = relationship(
        "Class", secondary="class_group_assignments", back_populates="class_groups"
    )

    __table_args__ = (
        UniqueConstraint("subject_id", "group_number", name="unique_subject_group"),
        Index("idx_classgroup_subject", "subject_id"),
        CheckConstraint("group_number >= 1", name="chk_group_number_positive"),
        CheckConstraint("enrollment_count >= 0", name="chk_enrollment_non_negative"),
    )


class Room(Base):
    __tablename__ = "rooms"

    room_id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), nullable=False, index=True)
    capacity = mapped_column(Integer, nullable=False)
    location_id = mapped_column(
        Integer, ForeignKey("locations.location_id"), nullable=False
    )
    owner_course_id = mapped_column(
        Integer, ForeignKey("courses.course_id"), nullable=True
    )

    # Relationships
    location = relationship("Location", back_populates="rooms")
    owner_course = relationship("Course", back_populates="owned_rooms")
    scheduled_classes = relationship("Class", back_populates="room")

    __table_args__ = (CheckConstraint("capacity > 0", name="chk_capacity_positive"),)


class TimetableVersion(Base):
    __tablename__ = "timetable_versions"

    version_id = mapped_column(Integer, primary_key=True)
    created_by = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)
    creation_date = mapped_column(DateTime, default=datetime.now, nullable=False)
    phase = mapped_column(SQLEnum(TimetablePhase), nullable=False)
    description = mapped_column(Text, nullable=True)

    # Relationships
    creator = relationship("User", back_populates="created_versions")
    classes = relationship("Class", back_populates="version")

    __table_args__ = (Index("idx_version_date", "creation_date"),)


class Class(Base):
    __tablename__ = "classes"

    class_id = mapped_column(Integer, primary_key=True)
    subject_id = mapped_column(
        Integer, ForeignKey("subjects.subject_id"), nullable=False
    )
    class_type = mapped_column(SQLEnum(ClassType), nullable=False)
    teacher_id = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)
    room_id = mapped_column(Integer, ForeignKey("rooms.room_id"), nullable=False)
    day_of_week = mapped_column(Integer, nullable=True)
    date = mapped_column(Date, nullable=True)
    start_time = mapped_column(Time, nullable=False)
    end_time = mapped_column(Time, nullable=False)
    is_recurring = mapped_column(Boolean, default=True, nullable=False)
    approval_status = mapped_column(
        SQLEnum(ApprovalStatus), default=ApprovalStatus.approved, nullable=False
    )
    version_id = mapped_column(
        Integer, ForeignKey("timetable_versions.version_id"), nullable=True
    )

    # Relationships
    subject = relationship("Subject", back_populates="classes")
    teacher = relationship("User", back_populates="taught_classes")
    room = relationship("Room", back_populates="scheduled_classes")
    version = relationship("TimetableVersion", back_populates="classes")
    class_groups = relationship(
        "ClassGroup", secondary="class_group_assignments", back_populates="classes"
    )
    approvals = relationship("Approval", back_populates="class_")

    __table_args__ = (
        CheckConstraint("start_time < end_time", name="chk_time_order"),
        CheckConstraint(
            "(is_recurring = TRUE AND day_of_week IS NOT NULL AND day_of_week BETWEEN 1 AND 7 AND date IS NULL) OR "
            "(is_recurring = FALSE AND date IS NOT NULL AND day_of_week IS NULL)",
            name="chk_recurring",
        ),
        Index(
            "idx_classes_teacher_time",
            "teacher_id",
            "day_of_week",
            "start_time",
            "end_time",
        ),
        Index(
            "idx_classes_room_time", "room_id", "day_of_week", "start_time", "end_time"
        ),
        Index("idx_classes_date", "date"),
        Index("idx_classes_approval", "approval_status"),
    )


class Unavailability(Base):
    __tablename__ = "unavailability"

    unavailability_id = mapped_column(Integer, primary_key=True)
    teacher_id = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)
    day_of_week = mapped_column(Integer, nullable=True)
    date = mapped_column(Date, nullable=True)
    start_time = mapped_column(Time, nullable=True)
    end_time = mapped_column(Time, nullable=True)
    is_full_day = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    teacher = relationship("User", back_populates="unavailabilities")

    __table_args__ = (
        CheckConstraint(
            "(is_full_day = TRUE AND start_time IS NULL AND end_time IS NULL) OR "
            "(is_full_day = FALSE AND start_time IS NOT NULL AND end_time IS NOT NULL AND start_time < end_time)",
            name="chk_unavail_time",
        ),
        CheckConstraint(
            "(day_of_week IS NOT NULL AND day_of_week BETWEEN 1 AND 7 AND date IS NULL) OR "
            "(date IS NOT NULL AND day_of_week IS NULL)",
            name="chk_unavail_recurring",
        ),
        Index("idx_unavailability_teacher", "teacher_id"),
        Index("idx_unavailability_date", "date"),
        Index("idx_unavailability_day", "day_of_week"),
    )


class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    event_id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)
    start_date = mapped_column(Date, nullable=False)
    end_date = mapped_column(Date, nullable=False)
    type = mapped_column(SQLEnum(EventType), nullable=False)

    __table_args__ = (
        CheckConstraint("start_date <= end_date", name="chk_event_date_order"),
        Index("idx_calendar_dates", "start_date", "end_date"),
    )


class Approval(Base):
    __tablename__ = "approvals"

    approval_id = mapped_column(Integer, primary_key=True)
    class_id = mapped_column(Integer, ForeignKey("classes.class_id"), nullable=False)
    requested_by = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)
    approved_by = mapped_column(Integer, ForeignKey("users.user_id"), nullable=True)
    status = mapped_column(
        SQLEnum(ApprovalStatus), default=ApprovalStatus.pending, nullable=False
    )
    request_date = mapped_column(DateTime, default=datetime.now, nullable=False)
    response_date = mapped_column(DateTime, nullable=True)
    notes = mapped_column(Text, nullable=True)

    # Relationships
    class_ = relationship("Class", back_populates="approvals")
    requester = relationship(
        "User", foreign_keys=[requested_by], back_populates="requested_approvals"
    )
    approver = relationship(
        "User", foreign_keys=[approved_by], back_populates="given_approvals"
    )

    __table_args__ = (
        Index("idx_approval_status", "status"),
        Index("idx_approval_class", "class_id"),
        CheckConstraint(
            "(status = 'pending' AND approved_by IS NULL AND response_date IS NULL) OR "
            "(status != 'pending' AND approved_by IS NOT NULL AND response_date IS NOT NULL)",
            name="chk_approval_consistency",
        ),
    )


# Define association table after all models
# This is defined using the Table construct, not as a model class
class_group_assignments = Table(
    "class_group_assignments",
    Base.metadata,
    Column("class_id", Integer, ForeignKey("classes.class_id"), primary_key=True),
    Column(
        "class_group_id",
        Integer,
        ForeignKey("class_groups.class_group_id"),
        primary_key=True,
    ),
)
