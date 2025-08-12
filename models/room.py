from pydantic import BaseModel, Field


class RoomModel(BaseModel):
    room_id: str = Field(..., examples=["1112"])
    name: str = Field(..., examples=["Room1", "Room2"])
    capacity: int = Field(..., examples=[20])
    is_full: bool = Field(default=False, examples=[True, False])


class RoomPostModel(BaseModel):
    room_name: str = Field(..., examples=["1112"])
    capacity: int = Field(..., examples=[20])


class RoomJoinResponse(BaseModel):
    room: RoomModel = Field(...)
    websocket_url: str = Field(...)
