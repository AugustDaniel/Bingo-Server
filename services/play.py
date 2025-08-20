import asyncio

from fastapi import WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from core import Game, Room, Player
from exceptions import InvalidWebSocketJoin
from mapper import map_bingo_card_to_response
from models.websocket import *


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


class PlayService:
    def __init__(self, game: Game):
        self.game = game
        self.connection_manager: dict[Room, ConnectionManager] = {}

    async def connect(self, websocket: WebSocket, room_id: str, player_id: str) -> None:
        if room_id not in self.game.rooms or player_id not in self.game.rooms[room_id].players:
            raise InvalidWebSocketJoin("This websocket url is not valid")

        await websocket.accept()
        joined_room: Room = self.game.rooms[room_id]
        connection = Connection(
            websocket=websocket,
            player=joined_room.players[player_id],
            room=joined_room
        )

        await (self.connection_manager
               .setdefault(joined_room, ConnectionManager())
               .add_connection(connection))

        asyncio.create_task(self.__listen_for_messages(connection))

        await connection.send(
            BingoCardMessage(
                message=map_bingo_card_to_response(connection.player.cards[0]),
            )
        )

        if not self.game.rooms[room_id].is_started:
            asyncio.create_task(self.__start_room(joined_room))

    async def disconnect(self, connection: Connection):
        try:
            await connection.close()
            await self.connection_manager[connection.room].remove_connection(connection)
        except KeyError:
            pass

    async def handle_message(self, message: WebSocketMessage, connection: Connection):
        msg_type = message.type

        match msg_type:
            case "bingo":
                await self.handle_bingo(connection)
            case "leave":
                await self.disconnect(connection)
            case _:
                pass

    async def handle_bingo(self, connection: Connection):
        bingo = connection.room.check_bingo(connection.player)

        if bingo:
            await self.connection_manager[connection.room].broadcast(ValidBingoMessage(
                message=connection.player.name
            ))
        else:
            await connection.send(InvalidBingoMessage(
                message="Invalid bingo"
            ))

    async def __start_room(self, room: Room):
        room.is_started = True
        await self.__draw_numbers(room)

    async def __close_room(self, room: Room):
        await self.connection_manager[room].broadcast(RoomOverMessage(
            message=room.room_id
        ))
        room.is_started = False
        await self.__close_connections(room)
        del self.game.rooms[room.room_id]

    async def __draw_numbers(self, room: Room):
        while not room.is_over() and room.players:
            message = NewDrawMessage(
                message=str(room.draw_number())
            )

            await self.connection_manager[room].broadcast(message)
            await asyncio.sleep(5)

        await self.__close_room(room)

    async def __close_connections(self, room: Room):
        for connection in await self.connection_manager[room].get_connections():
            await self.disconnect(connection)

    async def __listen_for_messages(self, connection: Connection):
        try:
            while True:
                try:
                    message = await connection.receive()
                    await self.handle_message(message, connection)
                except ValidationError as e:
                    await connection.send(ErrorMessage(
                        message="Invalid message received",
                    ))
        except WebSocketDisconnect:
            await self.disconnect(connection)
