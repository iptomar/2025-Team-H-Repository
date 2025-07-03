from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

# Import the Base from your models
# from app.models import Base

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections before using
    echo=False,  # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency for FastAPI
def get_session():
    """
    Database session dependency for FastAPI.
    Usage: db: Session = Depends(get_session)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize database tables
def init_db():
    """Create all tables in the database"""
    from app.models import models  # Ensure all models are imported
    from app.models import Base
    print('Tables SQLAlchemy will create:', list(Base.metadata.tables.keys()))
    Base.metadata.create_all(bind=engine)


# Drop all tables (use with caution!)
def drop_db():
    """Drop all tables from the database"""
    from app import models

    models.Base.metadata.drop_all(bind=engine)


def get_or_create(session: Session, model, defaults=None, **kwargs):
    """
    Get an object or create it if it doesn't exist.

    Args:
        session: Database session
        model: SQLAlchemy model class
        defaults: Dict of default values for creation
        **kwargs: Lookup parameters

    Returns:
        tuple: (instance, created) where created is a boolean
    """
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items())
        if defaults:
            params.update(defaults)
        instance = model(**params)
        session.add(instance)
        session.flush()
        return instance, True


# Create initial admin user
def create_admin_user(username: str, password: str):
    """Create an admin user if it doesn't exist"""
    from . import models
    from .api import hash_password

    with get_session() as db:
        admin, created = get_or_create(
            db,
            models.User,
            defaults={
                "password_hash": hash_password(password),
                "role": models.UserRole.Administrator,
            },
            username=username,
        )
        if created:
            print(f"Admin user '{username}' created successfully")
        else:
            print(f"Admin user '{username}' already exists")
        return admin


def seed_schools():
    from app.models.models import School, Location
    from app.database import get_session
    session = next(get_session())
    # Add campuses
    tomar = Location(name="Tomar", is_campus=True)
    abrantes = Location(name="Abrantes", is_campus=True)
    session.add_all([tomar, abrantes])
    session.commit()
    # Add schools
    estt = School(name="ESTT", location_id=tomar.location_id)
    esgt = School(name="ESGT", location_id=tomar.location_id)
    esta = School(name="ESTA", location_id=abrantes.location_id)
    session.add_all([estt, esgt, esta])
    session.commit()
    print("Seeded campuses and schools.")
