from core import Room, Game
from models import RoomModel, GameModel


def map_room_to_response(room: Room) -> RoomModel:
    return RoomModel(
        room_id=room.room_id,
        name=room.name,
        capacity=room.capacity,
        is_full=room.is_full()
    )


def map_game_to_response(game: Game) -> GameModel:
    return GameModel(
        rooms={game.rooms[room].room_id: map_room_to_response(game.rooms[room]) for room in game.rooms},
        max_capacity=game.max_capacity,
        max_rooms=game.max_rooms,
    )
