from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from dependencies import get_play_service

router = APIRouter(
    prefix="/play",
    tags=["play"]
)


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, player_id: str, service=Depends(get_play_service)):
    service

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{player_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{player_id} left the chat")
