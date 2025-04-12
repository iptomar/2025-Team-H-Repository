from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Database setup function
def setup_database(create_tables: bool = False):
    """
    Set up the database connection.
    
    Args:
        create_tables: If True, create all tables in the database
    
    Returns:
        SQLAlchemy engine
    """
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    if create_tables:
        SQLModel.metadata.create_all(engine)
    
    return engine
