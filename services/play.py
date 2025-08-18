import asyncio

from fastapi import WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from core import Game, BingoCardFactory, Room, Player
from exceptions import InvalidWebSocketJoin
from mapper import map_bingo_card_to_response
from models import WebSocketMessage


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


async def broadcast(connections: list[Connection], message: WebSocketMessage):
    for connection in connections:
        try:
            await connection.send(message)
        except WebSocketDisconnect as e:
            pass  # TODO maybe make separate connection manager class


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
            WebSocketMessage(
                type="card",
                message=map_bingo_card_to_response(BingoCardFactory.create())
            )
        )

        if not self.game.rooms[room_id].is_started:
            asyncio.create_task(self.__start_game(room_id))

    async def disconnect(self, connection: Connection):
        await connection.close()
        self.connections.remove(connection)

    async def handle_message(self, message: WebSocketMessage, connection: Connection):
        msg_type = message.type

        match msg_type:
            case "bingo":
                await self.handle_bingo(message, connection)
            case "leave":
                await self.disconnect(connection)
            case _:
                pass

    async def handle_bingo(self, message: WebSocketMessage, connection: Connection):
        bingo = connection.room.check_bingo(message.message)

        if bingo:
            room_connections = [con for con in self.connections if con.room.room_id == connection.room.room_id]
            await broadcast(room_connections, WebSocketMessage(
                type="bingo",
                message=connection.player.name
            ))
        else:
            await connection.send(WebSocketMessage(
                type="invalid_bingo",
                message="Invalid bingo"
            ))

    async def __start_game(self, room_id: str):
        self.game.rooms[room_id].is_started = True
        self.__draw_numbers(room_id)

    def __draw_numbers(self, room_id):
        room: Room = self.game.rooms[room_id]

        while not room.is_over() or room.players:
            message = WebSocketMessage(
                type="draw",
                message=str(room.draw_number())
            )

            broadcast(room_id, message)
            asyncio.sleep(5)

        self.__remove_room(room_id)

    def __remove_room(self, room_id: str):
        pass

    async def __listen_for_messages(self, connection: Connection):
        try:
            while True:
                try:
                    message = await connection.receive()
                    await self.handle_message(message, connection)
                except ValidationError as e:
                    await connection.send(WebSocketMessage(
                        type="error",
                        message="Invalid message received",
                    ))
        except WebSocketDisconnect:
            await self.disconnect(connection)
