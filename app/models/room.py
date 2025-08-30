from pydantic import BaseModel, Field


class RoomModel(BaseModel):
    room_id: str = Field(..., examples=["1112"])
    name: str = Field(..., examples=["Room1", "Room2"])
    capacity: int = Field(..., examples=[20])
    player_count: int = Field(default=0)
    is_full: bool = Field(default=False, examples=[True, False])


class RoomPostModel(BaseModel):
    name: str = Field(..., examples=["room1", "myroom"])
    capacity: int = Field(..., examples=[20])


class RoomJoinResponse(BaseModel):
    room: RoomModel = Field(...)
    websocket_url: str = Field(...)
