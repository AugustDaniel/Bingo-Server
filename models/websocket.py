from pydantic import BaseModel, Field
from .card import BingoCardModel


class WebSocketMessage(BaseModel):
    type: str = Field(...)
    message: str | BingoCardModel = Field(...)