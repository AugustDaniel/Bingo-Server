import asyncio

from fastapi import WebSocket

from app.core import Player, Room
from app.models import WebSocketMessage


class Connection:
    def __init__(self, player: Player, room: Room, websocket: WebSocket):
        self.player: Player = player
        self.room: Room = room
        self.__websocket: WebSocket = websocket

    async def send(self, message: WebSocketMessage):
        await self.__websocket.send_json(message)

    async def receive(self) -> WebSocketMessage:
        data = await self.__websocket.receive_json()
        return WebSocketMessage(**data)

    async def close(self):
        await self.__websocket.close()


class ConnectionManager:
    def __init__(self):
        self.__connections: list[Connection] = []
        self.__lock = asyncio.Lock()

    async def add_connection(self, connection: Connection):
        async with self.__lock:
            self.__connections.append(connection)

    async def remove_connection(self, connection: Connection):
        async with self.__lock:
            try:
                self.__connections.remove(connection)
            except ValueError:
                pass

    async def get_connections(self) -> list[Connection]:
        async with self.__lock:
            return list(self.__connections)

    async def broadcast(self, message: WebSocketMessage):
        connections = await self.get_connections()

        await asyncio.gather(
            *(c.send(message) for c in connections),
            return_exceptions=True
        )
