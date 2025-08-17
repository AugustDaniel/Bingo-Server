from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from dependencies import get_play_service
from services import PlayService

router = APIRouter(
    prefix="/play",
    tags=["play"]
)


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, player_id: str,
                             service: PlayService = Depends(get_play_service)):
    await service.connect(websocket, room_id, player_id)

    try:
        while True:
            data = await websocket.receive_json()
            # service.handle_message(data)
    except WebSocketDisconnect:
        pass
        # service.disconnect(websocket)
