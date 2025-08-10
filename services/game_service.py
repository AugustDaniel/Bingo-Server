from core.game import Game, MaxRoomsReached, CapacityTooHigh
from models import *
from mapper import *


class GameService:
    def __init__(self):
        self.game = Game()

    def get_game(self) -> GameModel:
        return map_game_to_response(self.game)

    def create_room(self, name: str, capacity: int) -> RoomModel | None:
        return map_room_to_response(self.game.create_new_room(name, capacity))
