from pydantic import BaseModel, Field

from models import RoomModel


class RoomJoinResponse(BaseModel):
    room: RoomModel = Field(...)
    websocket_url: str = Field(...)
