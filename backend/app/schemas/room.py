from pydantic import BaseModel, constr, PositiveInt
from typing import Optional

class RoomBase(BaseModel):
    name: constr(max_length=50)
    capacity: PositiveInt
    location_id: int
    owner_course_id: Optional[int] = None

class RoomCreate(RoomBase):
    pass

class RoomUpdate(RoomBase):
    name: Optional[constr(max_length=50)] = None
    capacity: Optional[PositiveInt] = None
    location_id: Optional[int] = None

class RoomResponse(RoomBase):
    room_id: int

    class Config:
        from_attributes = True  # Permite serializar objetos SQLAlchemy