from typing import Literal

from pydantic import BaseModel, Field
from .card import BingoCardModel


class WebSocketMessage(BaseModel):
    type: str = Field(...)
    message: str | BingoCardModel = Field(...)


class InvalidBingoMessage(WebSocketMessage):
    type: Literal["invalid_bingo"] = "invalid_bingo"
    message: str


class ValidBingoMessage(WebSocketMessage):
    type: Literal["valid_bingo"] = "valid_bingo"
    message: str


class NewDrawMessage(WebSocketMessage):
    type: Literal["draw"] = "draw"
    message: str


class ErrorMessage(WebSocketMessage):
    type: Literal["error"] = "error"
    message: str


class BingoCardMessage(WebSocketMessage):
    type: Literal["card"] = "card"
    message: BingoCardModel
