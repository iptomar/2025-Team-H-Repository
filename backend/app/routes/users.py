from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Mock database
users_db = []

# User model
class User(BaseModel):
    id: int
    name: str
    email: str

# Get all users
@router.get("/users", response_model=List[User])
async def get_users():
    return users_db

# Get a user by ID
@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = next((user for user in users_db if user["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Create a new user
@router.post("/users", response_model=User)
async def create_user(user: User):
    if any(u["id"] == user.id for u in users_db):
        raise HTTPException(status_code=400, detail="User with this ID already exists")
    users_db.append(user.dict())
    return user

# Update a user
@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, updated_user: User):
    for index, user in enumerate(users_db):
        if user["id"] == user_id:
            users_db[index] = updated_user.dict()
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

# Delete a user
@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    global users_db
    users_db = [user for user in users_db if user["id"] != user_id]
    return {"message": "User deleted successfully"}