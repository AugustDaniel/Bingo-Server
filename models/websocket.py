from pydantic import BaseModel, Field


class WebSocketMessage(BaseModel):
    type: str = Field(...)
    message: str = Field(...)