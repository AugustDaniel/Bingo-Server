from fastapi import APIRouter, WebSocket

router = APIRouter(
    prefix="/play",
    tags=["play"]
)


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(room_id: str, player_name: str, websocket: WebSocket):
    await websocket.accept()
    pass
