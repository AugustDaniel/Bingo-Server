import asyncio
import logging

from fastapi import WebSocket

from app.core import Player, Room
from app.models import WebSocketMessage

logger = logging.getLogger(__name__)


class Connection:
    def __init__(self, player: Player, room: Room, websocket: WebSocket):
        self.player: Player = player
        self.room: Room = room
        self.__websocket: WebSocket = websocket
        self.__lock = asyncio.Lock()

    async def send(self, message: WebSocketMessage):
        async with self.__lock:
            try:
                logger.debug(f"Sending message: {message}")
                await asyncio.wait_for(
                    self.__websocket.send_json(message.model_dump()),
                    timeout=2
                )
                logger.debug("sent")
            except asyncio.TimeoutError:
                logger.warning(f"send_json to {self.player.name} timed out")
            except Exception as e:
                logger.exception(f"send failed: {e}")
                raise

    async def receive(self) -> WebSocketMessage:
        data = await self.__websocket.receive_json()
        return WebSocketMessage(**data)

    async def close(self):
        try:
            await self.__websocket.close()
        except RuntimeError:
            pass


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

    async def broadcast(self, message: WebSocketMessage) -> dict[str, list]:
        connections = await self.get_connections()
        report = {
            "success": [],
            "failed": [],
        }
        for connection in connections:
            try:
                await connection.send(message)
                report["success"].append(connection)
            except Exception as e:
                logger.error("failed broadcast ")
                report["failed"].append(connection)

        return report

