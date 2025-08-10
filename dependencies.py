from services.game_service import GameService
from services.play_service import PlayService

game_service: GameService = GameService()
play_service: PlayService = PlayService()


def get_game_service() -> GameService:
    return game_service

def get_play_service() -> PlayService:
    return play_service