from fastapi import APIRouter, Depends
from dependencies import get_game_service
from models import GameModel, RoomModel, PlayerModel
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
def join_room(room_id: str, player: PlayerModel, service: GameService = Depends(get_game_service)):
    room = service.join_room(room_id, player)
    websocket_url = f'/play/ws/{room_id}?player_name={player.name}'
    return RoomJoinResponse(room=room, websocket_url=websocket_url)
