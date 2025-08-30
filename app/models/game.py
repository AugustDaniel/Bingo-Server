from pydantic import BaseModel, Field

from app.models import RoomModel


class GameModel(BaseModel):
    rooms: list[RoomModel] = Field(...)
    max_capacity: int = Field(..., examples=[20])
    max_rooms: int = Field(..., examples=[20])
