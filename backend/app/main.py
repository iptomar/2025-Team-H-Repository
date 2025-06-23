"""
Main application entry point for the IPT Timetables API.

This module initializes the FastAPI application and configures all routes.
The application provides endpoints for managing class schedules and user authentication.
"""

from fastapi import FastAPI
from app.database import setup_database
from app.routes import auth
from app.routes import classes
from sqlmodel import Session
from typing import Dict

# Initialize FastAPI application with metadata
app = FastAPI(
    title="Horários IPT",
    description="Sistema de criação de horários",
    version="0.1.0",
)

# Setup database connection
engine = setup_database(True)

# Configure application routes within database session context
with Session(engine) as session:
    # Include authentication routes
    app.include_router(auth.router)
    # Include class management routes
    app.include_router(classes.router)

    @app.get("/")
    def read_root() -> Dict[str, str]:
        """
        Root endpoint that returns a welcome message.
        
        Returns:
            Dict[str, str]: Welcome message for the API
        """
        return {"message": "Welcome to the FastAPI MariaDB Auth API"}
