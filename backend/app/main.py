from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth
from typing import Dict

app = FastAPI(
    title="FastAPI MariaDB Auth",
    description="Simple authentication API with FastAPI and MariaDB",
    version="0.1.0",
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)


@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "Welcome to the FastAPI MariaDB Auth API"}
