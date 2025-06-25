from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.routes import auth
from app.routes import classes
from app.database import get_session, init_db
from typing import Dict

app = FastAPI(
    title="Horários IPT",
    description="Sistema de criação de horários",
    version="0.1.0",
)

# Run once to init database
# init_db()

app.include_router(auth.router)
app.include_router(classes.router)

@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "Welcome to the FastAPI MariaDB Auth API"}

@app.get("/example")
def example_route(db: Session = Depends(get_session)) -> Dict[str, str]:
    # Example: db.query(SomeModel).all()
    return {"message": "This is an example route using the database session"}
