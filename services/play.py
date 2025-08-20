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


class PlayService:
    def __init__(self, game: Game):
        self.game = game
        self.connections: list[Connection] = []

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

        self.connections.append(connection)

        asyncio.create_task(self.__listen_for_messages(connection))

        await connection.send(
            BingoCardMessage(
                message=map_bingo_card_to_response(connection.player.cards[0]),
            )
        )

        if not self.game.rooms[room_id].is_started:
            asyncio.create_task(self.__start_room(joined_room))

    async def disconnect(self, connection: Connection):
        await connection.close()
        self.connections.remove(connection)

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
            await self.broadcast(connection.room, ValidBingoMessage(
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
        await self.broadcast(room, RoomOverMessage(
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

            await self.broadcast(room, message)
            await asyncio.sleep(5)

        await self.__close_room(room)

    async def __close_connections(self, room: Room):
        connections = self.get_room_connections(room)
        for connection in connections:
            await self.disconnect(connection)

    def get_room_connections(self, room: Room) -> list[Connection]:
        return [con for con in self.connections if con.room.room_id == room.room_id]

    async def broadcast(self, room: Room, message: WebSocketMessage):
        room_connections = self.get_room_connections(room)
        for connection in room_connections:
            try:
                await connection.send(message)
            except WebSocketDisconnect as e:
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
