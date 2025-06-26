from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models.models import Class as ClassModel
from app.schemas import classes as schemas
from datetime import datetime
from app import models
from typing import List

router = APIRouter(prefix="/classes", tags=["classes"])

