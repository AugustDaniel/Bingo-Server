import asyncio

from fastapi import WebSocket, WebSocketDisconnect

from core import Game
from exceptions import InvalidWebSocketJoin
from models import WebSocketMessage


class PlayService:
    def __init__(self, game: Game):
        self.game = game
        self.connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, room_id: str, player_id: str) -> None:
        if room_id not in self.game.rooms or player_id not in self.game.rooms[room_id].players:
            raise InvalidWebSocketJoin("This websocket url is not valid")

        await websocket.accept()
        self.connections[player_id] = websocket

        if not self.game.rooms[room_id].is_started:
            asyncio.create_task(self.__start_game(room_id))

    async def broadcast(self , player_ids: list[str], message: WebSocketMessage):
        for player_id in player_ids:
            try:
                await self.connections[player_id].send_json(message)
            except WebSocketDisconnect as e:
                pass #TODO maybe


    async def __start_game(self, room_id):
        self.game.rooms[room_id].is_started = True
        self.__draw_numbers(room_id)

    def __draw_numbers(self, room_id):
        room = self.game.rooms[room_id]

        while not room.is_over():
             message = WebSocketMessage(
                 type="draw",
                 message=str(room.draw_number())
             )

             self.broadcast(room_id, message)
             asyncio.sleep(5)

        self.__remove_room(room_id)


    def __remove_room(self, room_id):
        pass


