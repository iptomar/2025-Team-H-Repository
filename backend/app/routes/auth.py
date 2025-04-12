from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.models.models import User

router = APIRouter(prefix="/auth", tags=["auth"])
