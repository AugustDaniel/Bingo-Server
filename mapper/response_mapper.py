from core import Room, Game, Player
from models import RoomModel, GameModel, PlayerModel


def map_room_to_response(room: Room) -> RoomModel:
    return RoomModel(
        room_id=room.room_id,
        name=room.name,
        capacity=room.capacity,
        is_full=room.is_full()
    )


def map_game_to_response(game: Game) -> GameModel:
    return GameModel(
        rooms={room: map_room_to_response(game.rooms[room]) for room in game.rooms},
        max_capacity=game.max_capacity,
        max_rooms=game.max_rooms,
    )


def map_response_to_player(player: PlayerModel) -> Player:
    return Player(player.name)
