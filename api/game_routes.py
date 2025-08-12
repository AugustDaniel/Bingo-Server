from fastapi import APIRouter, Depends
from dependencies import get_game_service
from models import GameModel, RoomModel, PlayerModel
from models.player import PlayerPostModel
from models.room_join_response import RoomJoinResponse
from services.game_service import GameService

router = APIRouter(
    prefix="/game",
    tags=["game"],
)


@router.get("/", response_model=GameModel)
def get_game(service: GameService = Depends(get_game_service)):
    return service.get_game()


@router.post("/rooms", response_model=RoomModel)
def create_room(room: RoomModel, service: GameService = Depends(get_game_service)):
    return service.create_room(room)


@router.post("/rooms/{room_id}/players", response_model=RoomJoinResponse)
def join_room(room_id: str, player_post: PlayerPostModel, service: GameService = Depends(get_game_service)):
    room, player = service.join_room(room_id, player_post)
    websocket_url = f'/play/ws/{room_id}?player_name={player.id}'
    return RoomJoinResponse(room=room, websocket_url=websocket_url)
