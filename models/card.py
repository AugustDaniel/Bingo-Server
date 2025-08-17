from pydantic import BaseModel, Field


class BingoCardCellModel(BaseModel):
    content: str | int = Field(...)
    scratched: bool = Field(...)


class BingoCardModel(BaseModel):
    card: list[list[BingoCardCellModel]] = Field(..., title="Card")
