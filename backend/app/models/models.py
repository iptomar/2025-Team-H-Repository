from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Date,
    Time,
    DateTime,
    Enum as SQLEnum,
    CheckConstraint,
    Index,
    UniqueConstraint,
    Table,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


# Define Enums for database ENUM types
class UserRole(str, Enum):
    Administrator = "Administrator"
    School_Timetable_Committee = "School_Timetable_Committee"
    Course_Timetable_Committee = "Course_Timetable_Committee"
    Teacher = "Teacher"


class ClassType(str, Enum):
    P  = "P"  # Practical
    T  = "T"  # Theoretical
    TP = "TP"  # Theoretical-Practical


class ApprovalStatus(str, Enum):
    pending  = "pending"
    approved = "approved"
    rejected = "rejected"


class EventType(str, Enum):
    holiday = "holiday"
    break_  = "break"
    other   = "other"


class TimetablePhase(str, Enum):
    proposal   = "proposal"
    adjustment = "adjustment"


# Link tables for many-to-many relationships
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


class User(Base):
    """Users table to manage all system users with role-based access."""

    __tablename__ = "users"

    user_id       = Column(Integer, primary_key=True, autoincrement=True)
    username      = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role          = Column(SQLEnum(UserRole), nullable=False)
    school_id     = Column(Integer, ForeignKey("schools.school_id"), nullable=True)
    course_id     = Column(Integer, ForeignKey("courses.course_id"), nullable=True)

    # Relationships will be defined from other tables
    taught_classes = relationship(
        "Class", foreign_keys="Class.teacher_id", back_populates="teacher"
    )
    unavailabilities = relationship("Unavailability", back_populates="teacher")
    requested_approvals = relationship(
        "Approval", foreign_keys="Approval.requested_by", back_populates="requester"
    )
    approved_approvals = relationship(
        "Approval", foreign_keys="Approval.approved_by", back_populates="approver"
    )
    created_versions = relationship("TimetableVersion", back_populates="creator")

    # Check constraints
    __table_args__ = (
        CheckConstraint(
            "role != 'School_Timetable_Committee' OR school_id IS NOT NULL",
            name="chk_role_school",
        ),
        CheckConstraint(
            "role != 'Course_Timetable_Committee' OR course_id IS NOT NULL",
            name="chk_role_course",
        ),
    )

    @validates("role", "school_id", "course_id")
    def validate_role_constraints(self, key, value):
        if key == "role" and self.role != value:
            # Role is being changed, reset related fields
            if value == UserRole.School_Timetable_Committee:
                if not hasattr(self, "school_id") or self.school_id is None:
                    raise ValueError(
                        "School Timetable Committee members must have a school_id"
                    )
            elif value == UserRole.Course_Timetable_Committee:
                if not hasattr(self, "course_id") or self.course_id is None:
                    raise ValueError(
                        "Course Timetable Committee members must have a course_id"
                    )
        return value


class Location(Base):
    """Locations table for campuses and additional locations."""

    __tablename__ = "locations"

    location_id = Column(Integer, primary_key=True, autoincrement=True)
    name        = Column(String(100), nullable=False)
    is_campus   = Column(Boolean, nullable=False, default=False)

    # Relationships
    schools      = relationship("School", back_populates="location")
    rooms        = relationship("Room", back_populates="location")
    class_groups = relationship("ClassGroup", back_populates="location")


class School(Base):
    """Schools table, linked to campus locations."""

    __tablename__ = "schools"

    school_id   = Column(Integer, primary_key=True, autoincrement=True)
    name        = Column(String(50), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.location_id"), nullable=False)

    # Relationships
    location          = relationship("Location", back_populates="schools")
    courses           = relationship("Course", back_populates="school")
    committee_members = relationship("User", foreign_keys="User.school_id")

    # Constraint to ensure schools are at campus locations
    __table_args__ = (
        CheckConstraint(
            "EXISTS (SELECT 1 FROM locations WHERE location_id = schools.location_id AND is_campus = TRUE)",
            name="chk_campus_school",
        ),
    )

    def validate_campus_location(self, session):
        """Ensure school's location is a campus"""
        location = session.query(Location).get(self.location_id)
        if not location.is_campus:
            raise ValueError("Schools must be located at a campus")


class Course(Base):
    """Courses table, including a flag for short courses."""

    __tablename__ = "courses"

    course_id       = Column(Integer, primary_key=True, autoincrement=True)
    name            = Column(String(100), nullable=False)
    school_id       = Column(Integer, ForeignKey("schools.school_id"), nullable=False)
    is_short_course = Column(Boolean, nullable=False, default=False)

    # Relationships
    school            = relationship("School", back_populates="courses")
    subjects          = relationship("Subject", back_populates="course")
    owned_rooms       = relationship("Room", back_populates="owner_course")
    committee_members = relationship("User", foreign_keys="User.course_id")


class Subject(Base):
    """Subjects table, each tied to a specific course."""

    __tablename__ = "subjects"

    subject_id = Column(Integer, primary_key=True, autoincrement=True)
    name       = Column(String(100), nullable=False)
    course_id  = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    weekly_required_hours = Column(Integer, nullable=False, default=2)


    # Relationships
    course       = relationship("Course", back_populates="subjects")
    class_groups = relationship("ClassGroup", back_populates="subject")
    classes      = relationship("Class", back_populates="subject")


class ClassGroup(Base):
    """Class Groups table, with a location that defaults to the school's campus."""

    __tablename__ = "class_groups"

    class_group_id   = Column(Integer, primary_key=True, autoincrement=True)
    subject_id       = Column(Integer, ForeignKey("subjects.subject_id"), nullable=False)
    group_number     = Column(Integer, nullable=False)
    enrollment_count = Column(Integer, nullable=False)
    location_id      = Column(Integer, ForeignKey("locations.location_id"), nullable=False)

    # Relationships
    subject  = relationship("Subject", back_populates="class_groups")
    location = relationship("Location", back_populates="class_groups")
    classes  = relationship(
        "Class", secondary=class_group_assignments, back_populates="class_groups"
    )

    # Check constraint for enrollment_count
    __table_args__ = (
        CheckConstraint("enrollment_count >= 0", name="chk_enrollment_count"),
        UniqueConstraint("subject_id", "group_number", name="unique_subject_group"),
    )


class Room(Base):
    """Rooms table, with capacity and optional course ownership for special rooms."""

    __tablename__ = "rooms"

    room_id         = Column(Integer, primary_key=True, autoincrement=True)
    name            = Column(String(50), nullable=False)
    capacity        = Column(Integer, nullable=False)
    location_id     = Column(Integer, ForeignKey("locations.location_id"), nullable=False)
    owner_course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=True)

    # Relationships
    location          = relationship("Location", back_populates="rooms")
    owner_course      = relationship("Course", back_populates="owned_rooms")
    scheduled_classes = relationship("Class", back_populates="room")

    # Check constraint for capacity
    __table_args__ = (CheckConstraint("capacity > 0", name="chk_capacity"),)


class TimetableVersion(Base):
    """Timetable Versions for tracking changes."""

    __tablename__ = "timetable_versions"

    version_id    = Column(Integer, primary_key=True, autoincrement=True)
    created_by    = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    creation_date = Column(DateTime, nullable=False, default=datetime.now)
    phase         = Column(SQLEnum(TimetablePhase), nullable=False)
    description   = Column(Text)

    # Relationships
    creator = relationship("User", back_populates="created_versions")
    classes = relationship("Class", back_populates="version")


class Class(Base):
    """Classes table, supporting both recurring and non-recurring schedules."""

    __tablename__ = "classes"

    class_id        = Column(Integer, primary_key=True, autoincrement=True)
    subject_id      = Column(Integer, ForeignKey("subjects.subject_id"), nullable=False)
    class_type      = Column(SQLEnum(ClassType), nullable=False)
    teacher_id      = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    room_id         = Column(Integer, ForeignKey("rooms.room_id"), nullable=False)
    day_of_week     = Column(Integer)  # 1-7 (Monday-Sunday)
    date            = Column(Date)
    start_time      = Column(Time, nullable=False)
    end_time        = Column(Time, nullable=False)
    is_recurring    = Column(Boolean, nullable=False, default=True)
    approval_status = Column(
        SQLEnum(ApprovalStatus), nullable=False, default=ApprovalStatus.approved
    )
    version_id      = Column(Integer, ForeignKey("timetable_versions.version_id"))

    # Relationships
    subject = relationship("Subject", back_populates="classes")
    teacher = relationship(
        "User", foreign_keys=[teacher_id], back_populates="taught_classes"
    )
    room         = relationship("Room", back_populates="scheduled_classes")
    version      = relationship("TimetableVersion", back_populates="classes")
    approvals    = relationship("Approval", back_populates="class_")
    class_groups = relationship(
        "ClassGroup", secondary=class_group_assignments, back_populates="classes"
    )

    # Constraints and indexes
    __table_args__ = (
        # Check constraints
        CheckConstraint(
            "EXTRACT(MINUTE FROM start_time) IN (0, 30) AND EXTRACT(MINUTE FROM end_time) IN (0, 30)",
            name="chk_time_resolution",
        ),
        CheckConstraint("start_time < end_time", name="chk_time_order"),
        CheckConstraint(
            "(is_recurring = TRUE AND day_of_week BETWEEN 1 AND 7 AND date IS NULL) OR "
            "(is_recurring = FALSE AND date IS NOT NULL AND day_of_week IS NULL)",
            name="chk_recurring",
        ),
        CheckConstraint(
            "EXISTS (SELECT 1 FROM users WHERE user_id = teacher_id AND role = 'Teacher')",
            name="chk_teacher_role",
        ),
        # Indexes
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
    )

    @validates("start_time", "end_time")
    def validate_time_resolution(self, key, value):
        if key == "start_time" or key == "end_time":
            if value.minute not in (0, 30):
                raise ValueError(f"{key} minutes must be either 0 or 30")
        if key == "end_time" and hasattr(self, "start_time") and self.start_time:
            if value <= self.start_time:
                raise ValueError("End time must be after start time")
        return value

    @validates("is_recurring", "day_of_week", "date")
    def validate_recurring_constraints(self, key, value):
        if key == "is_recurring":
            if value:
                # Recurring classes need day_of_week and no date
                if hasattr(self, "day_of_week") and (
                    self.day_of_week is None or not 1 <= self.day_of_week <= 7
                ):
                    raise ValueError(
                        "Recurring classes must have a day of week between 1 and 7"
                    )
                if hasattr(self, "date") and self.date is not None:
                    raise ValueError("Recurring classes cannot have a specific date")
            else:
                # Non-recurring classes need date and no day_of_week
                if hasattr(self, "date") and self.date is None:
                    raise ValueError("Non-recurring classes must have a specific date")
                if hasattr(self, "day_of_week") and self.day_of_week is not None:
                    raise ValueError("Non-recurring classes cannot have a day of week")

        if key == "day_of_week" and value is not None:
            if not 1 <= value <= 7:
                raise ValueError("Day of week must be between 1 and 7")
            if hasattr(self, "is_recurring") and not self.is_recurring:
                raise ValueError("Non-recurring classes cannot have a day of week")

        if key == "date" and value is not None:
            if hasattr(self, "is_recurring") and self.is_recurring:
                raise ValueError("Recurring classes cannot have a specific date")

        return value

    def validate_teacher_role(self, session):
        """Ensure the assigned teacher has the Teacher role"""
        teacher = session.query(User).get(self.teacher_id)
        if teacher.role != UserRole.Teacher:
            raise ValueError("Class teacher must have the Teacher role")


class Unavailability(Base):
    """Unavailability table for teachers."""

    __tablename__ = "unavailability"

    unavailability_id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id        = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    day_of_week       = Column(Integer)  # 1-7 for recurring
    date              = Column(Date)
    start_time        = Column(Time)
    end_time          = Column(Time)
    is_full_day       = Column(Boolean, nullable=False, default=False)

    # Relationships
    teacher = relationship("User", back_populates="unavailabilities")

    # Constraints and indexes
    __table_args__ = (
        # Check constraints
        CheckConstraint(
            "(is_full_day = TRUE AND start_time IS NULL AND end_time IS NULL) OR "
            "(is_full_day = FALSE AND start_time IS NOT NULL AND end_time IS NOT NULL AND start_time < end_time)",
            name="chk_unavail_time",
        ),
        CheckConstraint(
            "(day_of_week BETWEEN 1 AND 7 AND date IS NULL) OR (date IS NOT NULL AND day_of_week IS NULL)",
            name="chk_unavail_recurring",
        ),
        CheckConstraint(
            "EXISTS (SELECT 1 FROM users WHERE user_id = teacher_id AND role = 'Teacher')",
            name="chk_teacher_unavail_role",
        ),
        # Indexes
        Index(
            "idx_unavailability_teacher",
            "teacher_id",
            "day_of_week",
            "start_time",
            "end_time",
        ),
    )

    @validates("is_full_day", "start_time", "end_time")
    def validate_time_constraints(self, key, value):
        if key == "is_full_day":
            if value:
                # For full day, start_time and end_time should be None
                if hasattr(self, "start_time") and self.start_time is not None:
                    raise ValueError(
                        "Full day unavailability should not have start time"
                    )
                if hasattr(self, "end_time") and self.end_time is not None:
                    raise ValueError("Full day unavailability should not have end time")
            else:
                # For partial day, start_time and end_time are required
                if not hasattr(self, "start_time") or self.start_time is None:
                    raise ValueError("Partial day unavailability must have start time")
                if not hasattr(self, "end_time") or self.end_time is None:
                    raise ValueError("Partial day unavailability must have end time")

        if (
            key == "end_time"
            and value is not None
            and hasattr(self, "start_time")
            and self.start_time is not None
        ):
            if value <= self.start_time:
                raise ValueError("End time must be after start time")

        return value

    @validates("day_of_week", "date")
    def validate_recurring_constraints(self, key, value):
        if key == "day_of_week" and value is not None:
            if not 1 <= value <= 7:
                raise ValueError("Day of week must be between 1 and 7")
            if hasattr(self, "date") and self.date is not None:
                raise ValueError("Cannot have both day of week and specific date")

        if key == "date" and value is not None:
            if hasattr(self, "day_of_week") and self.day_of_week is not None:
                raise ValueError("Cannot have both day of week and specific date")

        return value

    def validate_teacher_role(self, session):
        """Ensure the teacher has the Teacher role"""
        teacher = session.query(User).get(self.teacher_id)
        if teacher.role != UserRole.Teacher:
            raise ValueError(
                "Unavailability can only be set for users with Teacher role"
            )


class CalendarEvent(Base):
    """Calendar Events table for holidays and breaks."""

    __tablename__ = "calendar_events"

    event_id   = Column(Integer, primary_key=True, autoincrement=True)
    name       = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date   = Column(Date, nullable=False)
    type       = Column(SQLEnum(EventType), nullable=False)

    # Constraints
    __table_args__ = (CheckConstraint("start_date <= end_date", name="chk_date_order"),)

    @validates("start_date", "end_date")
    def validate_dates(self, key, value):
        if (
            key == "end_date"
            and hasattr(self, "start_date")
            and self.start_date is not None
        ):
            if value < self.start_date:
                raise ValueError("End date must be after or equal to start date")
        return value


class Approval(Base):
    """Approvals table for special room bookings."""

    __tablename__ = "approvals"

    approval_id  = Column(Integer, primary_key=True, autoincrement=True)
    class_id     = Column(Integer, ForeignKey("classes.class_id"), nullable=False)
    requested_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    approved_by  = Column(Integer, ForeignKey("users.user_id"))
    status       = Column(
        SQLEnum(ApprovalStatus), nullable=False, default=ApprovalStatus.pending
    )
    request_date = Column(DateTime, nullable=False, default=datetime.now)

    # Relationships
    class_ = relationship("Class", back_populates="approvals")
    requester = relationship(
        "User", foreign_keys=[requested_by], back_populates="requested_approvals"
    )
    approver = relationship(
        "User", foreign_keys=[approved_by], back_populates="approved_approvals"
    )


# Database setup function
def setup_database(db_url: str, create_tables: bool = False):
    """
    Set up the database connection.

    Args:
        db_url: Database URL
        create_tables: If True, create all tables in the database

    Returns:
        SQLAlchemy engine and session maker
    """
    engine = create_engine(db_url)

    if create_tables:
        Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal
