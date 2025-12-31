import asyncio
import logging

from fastapi import WebSocket
from pydantic import ValidationError

from app.core import Game, Room
from app.exceptions import InvalidWebSocketJoin
from app.mapper import map_bingo_card_to_response
from app.models.websocket import *
from .connection import ConnectionManager, Connection

logger = logging.getLogger(__name__)


class PlayService:
    def __init__(self, game: Game):
        self.game = game
        self.connection_manager: dict[str, ConnectionManager] = {}  # room_id -> connection manager

    async def connect(self, websocket: WebSocket, room_id: str) -> Connection:
        logger.info(f"connect {room_id}")
        await websocket.accept()
        player_id = websocket.query_params.get('player_id')

        if room_id not in self.game.rooms or player_id not in self.game.rooms[room_id].players:
            raise InvalidWebSocketJoin("This websocket url is not valid")

        joined_room: Room = self.game.rooms[room_id]
        connection = Connection(
            websocket=websocket,
            player=joined_room.players[player_id],
            room=joined_room
        )

        await (self.connection_manager
               .setdefault(joined_room.room_id, ConnectionManager())
               .add_connection(connection))

        try:
            await connection.send(
                BingoCardMessage(
                    message=map_bingo_card_to_response(connection.player.cards[0]),
                )
            )
        except:
            await self.disconnect(connection)
            raise InvalidWebSocketJoin("Card could not be sent")

        if not self.game.rooms[room_id].is_started:
            logger.info("creating room: " + room_id)
            asyncio.create_task(self.__start_room(joined_room))

        return connection

    async def disconnect(self, connection: Connection):
        try:
            await connection.close()
            await self.connection_manager[connection.room.room_id].remove_connection(connection)
            del self.game.rooms[connection.room.room_id].players[connection.player.id]
        except Exception as e:
            logger.exception("unable to remove connection" + e)
            pass

    async def room_broadcast(self, room: Room, message: WebSocketMessage):
        report = await self.connection_manager[room.room_id].broadcast(message)

        failed = report["failed"]
        for connection in failed:
            logger.error(f"failed {connection.player.name}")
            await self.disconnect(connection)

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
            await self.room_broadcast(connection.room, ValidBingoMessage(
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
        await self.room_broadcast(room, RoomOverMessage(
            message=room.room_id
        ))
        room.is_started = False
        await self.__close_connections(room)
        del self.game.rooms[room.room_id]

    async def __draw_numbers(self, room: Room):
        logger.info("drawing numbers")
        while not room.is_over() and room.players:
            logger.info(f"number drawn {room.players.__len__()}")
            message = NewDrawMessage(
                message=str(room.draw_number())
            )

            await self.room_broadcast(room, message)
            await asyncio.sleep(5)
        logger.info("finished drawing numbers")
        await self.__close_room(room)

    async def __close_connections(self, room: Room):
        for connection in await self.connection_manager[room.room_id].get_connections():
            await self.disconnect(connection)

    async def listen_for_messages(self, connection: Connection):
        logger.info("start listening for messages")
        try:
            while True:
                try:
                    message = await connection.receive()
                    await self.handle_message(message, connection)
                except ValidationError as e:
                    await connection.send(ErrorMessage(
                        message="Invalid message received",
                    ))
        except:
            logger.info("disconnect")
            await self.disconnect(connection)
