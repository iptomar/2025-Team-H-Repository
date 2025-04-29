from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Database setup function
def setup_database(create_tables: bool = False):
    """
    Set up the database connection.
    
    Args:
        create_tables: If True, create all tables in the database
    
    Returns:
        SQLAlchemy engine
    """
    if create_tables:
        SQLModel.metadata.create_all(engine)
    return engine

# Dependency to get a database session
def get_session():
    """
    Provide a database session for dependency injection.
    
    Yields:
        Session: A SQLModel session
    """
    with Session(engine) as session:
        yield session