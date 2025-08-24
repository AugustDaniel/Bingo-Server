from fastapi import APIRouter, WebSocket, Depends
from app.dependencies import get_play_service
from app.services import PlayService

router = APIRouter(
    prefix="/play",
    tags=["play"]
)


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, player_id: str,
                             service: PlayService = Depends(get_play_service)):
    await service.connect(websocket, room_id, player_id)
