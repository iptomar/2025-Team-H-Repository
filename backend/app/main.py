from fastapi import FastAPI
from app.database import setup_database
from app.routes import auth
from sqlmodel import Session
from typing import Dict

app = FastAPI(
    title="Horários IPT",
    description="Sistema de criação de horários",
    version="0.1.0",
)

engine = setup_database(True)

with Session(engine) as session:
    app.include_router(auth.router)


    @app.get("/")
    def read_root() -> Dict[str, str]:
        return {"message": "Welcome to the FastAPI MariaDB Auth API"}
