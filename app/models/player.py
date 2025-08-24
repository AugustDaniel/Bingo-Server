from pydantic import BaseModel, Field


class PlayerPostModel(BaseModel):
    name: str = Field(..., title="Player's name")


class PlayerModel(BaseModel):
    name: str = Field(...)
    id: str = Field(...)
