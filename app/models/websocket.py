from typing import Literal

from pydantic import BaseModel, Field
from .card import BingoCardModel


class WebSocketMessage(BaseModel):
    type: str = Field(...)
    message: str | BingoCardModel = Field(...)


class InvalidBingoMessage(WebSocketMessage):
    type: Literal["invalid_bingo"] = "invalid_bingo"
    message: str  # invalid bingo message


class ValidBingoMessage(WebSocketMessage):
    type: Literal["valid_bingo"] = "valid_bingo"
    message: str  # valid bingo message


class BingoBroadcast(WebSocketMessage):
    type: Literal["bingo"] = "bingo"
    message: str # contains name of the player who has gotten a bingo


class NewDrawMessage(WebSocketMessage):
    type: Literal["draw"] = "draw"
    message: str  # new draw in the room


class ErrorMessage(WebSocketMessage):
    type: Literal["error"] = "error"
    message: str  # error message


class BingoCardMessage(WebSocketMessage):
    type: Literal["card"] = "card"
    message: BingoCardModel  # bingo card


class RoomOverMessage(WebSocketMessage):
    type: Literal["room_over"] = "room_over"
    message: str # room id
