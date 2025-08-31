from fastapi import APIRouter, Depends
from app.dependencies import get_game_service
from app.models import GameModel, RoomModel, RoomPostModel
from app.models.player import PlayerPostModel
from app.models import RoomJoinResponse
from app.services import GameService

router = APIRouter(
    prefix="/game",
    tags=["game"],
)


@router.get("/", response_model=GameModel)
def get_game(service: GameService = Depends(get_game_service)):
    return service.get_game()


@router.post("/rooms", response_model=RoomModel)
def create_room(room: RoomPostModel, service: GameService = Depends(get_game_service)):
    return service.create_room(room)


@router.delete("/rooms/{room_id}")
def delete_room(room_id: str, service: GameService = Depends(get_game_service)):
    return service.delete_room(room_id)


@router.post("/rooms/{room_id}/players", response_model=RoomJoinResponse)
def join_room(room_id: str, player_post: PlayerPostModel, service: GameService = Depends(get_game_service)):
    room, player = service.join_room(room_id, player_post)
    websocket_url = f'/play/ws/{room_id}?player_id={player.id}'
    return RoomJoinResponse(room=room, websocket_url=websocket_url)
