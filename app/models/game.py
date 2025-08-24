from typing import Dict

from pydantic import BaseModel, Field

from app.models import RoomModel


class GameModel(BaseModel):
    rooms: Dict[str, RoomModel] = Field(...) # room_id -> RoomModel
    max_capacity: int = Field(..., examples=[20])
    max_rooms: int = Field(..., examples=[20])
