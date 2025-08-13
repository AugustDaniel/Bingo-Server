from core import Game
from services import GameService, PlayService

__game: Game = Game()
__game_service: GameService = GameService(__game)
__play_service: PlayService = PlayService(__game)


def get_game_service() -> GameService:
    return __game_service


def get_play_service() -> PlayService:
    return __play_service
