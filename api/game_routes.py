from typing import List, Dict

from fastapi import APIRouter

from models.room_model import RoomModel

router = APIRouter(prefix="/game", tags=["game"])


# @router.get("/rooms", response_model=Dict[Room])
# def get_rooms() -> Dict[Room]:
