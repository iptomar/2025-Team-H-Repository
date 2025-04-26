from fastapi import FastAPI
from app.database import setup_database
from app.routes import auth
from app.routes import classes
from app.routes import rooms
from sqlmodel import Session
from typing import Dict

app = FastAPI(
    title="Horários IPT",
    description="Sistema de criação de horários",
    version="0.1.0",
)

engine = setup_database(True)

Base.metadata.create_all(bind=engine) #Cria as tabelas definidas pelos modelos (incluindo Room)

with Session(engine) as session:
    app.include_router(auth.router)
    app.include_router(classes.router)
    app.include_router(rooms.router)

    @app.get("/")
    def read_root() -> Dict[str, str]:
        return {"message": "Welcome to the FastAPI MariaDB Auth API"}