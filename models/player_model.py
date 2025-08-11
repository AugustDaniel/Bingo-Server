from pydantic import BaseModel, Field


class PlayerModel(BaseModel):
    name: str = Field(...)
