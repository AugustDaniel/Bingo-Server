from pydantic import BaseModel, Field
from .card import BingoCardModel


class WebSocketMessage(BaseModel):
    type: str = Field(...)
    message: str | BingoCardModel = Field(...)


class InvalidBingoMessage(WebSocketMessage):
    def __init__(self, message: str):
        super().__init__(
            type="invalid_bingo",
            message=message
        )


class ValidBingoMessage(WebSocketMessage):
    def __init__(self, message: str):
        super().__init__(
            type="valid_bingo",
            message=message
        )


class NewDrawMessage(WebSocketMessage):
    def __init__(self, message: str):
        super().__init__(
            type="draw",
            message=message
        )


class ErrorMessage(WebSocketMessage):
    def __init__(self, message: str):
        super().__init__(
            type="error",
            message=message
        )


class BingoCardMessage(WebSocketMessage):
    def __init__(self, message: BingoCardModel):
        super().__init__(
            type="card",
            message=message
        )
