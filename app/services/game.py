from app.core.game import Game
from app.models import *
from app.mapper import *


class GameService:
    def __init__(self, game: Game):
        self.game = game

    def get_game(self) -> GameModel:
        return map_game_to_response(self.game)

    def create_room(self, room: RoomPostModel) -> RoomModel | None:
        return map_room_to_response(self.game.create_new_room(room.name, room.capacity))

    def join_room(self, room_id: str, player: PlayerPostModel) -> tuple[RoomModel, PlayerModel]:
        player = self.game.create_new_player(player.name)
        self.game.add_player_to_room(player, self.game.rooms.get(room_id))
        return map_room_to_response(self.game.rooms.get(room_id)), map_player_to_response(player)
