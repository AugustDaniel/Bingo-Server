from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_game_service
from models import GameModel, RoomModel
from services.game_service import GameService

router = APIRouter(
    prefix="/game",
    tags=["game"],
)


@router.get("/", response_model=GameModel)
def get_game(game_service: GameService = Depends(get_game_service)):
    return game_service.get_game()


@router.post("/", response_model=RoomModel)
def create_room(name: str, capacity: int, service: GameService = Depends(get_game_service)):
    return service.create_room(name, capacity)
