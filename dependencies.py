from services.game_service import GameService

__game_service: GameService = GameService()


def get_game_service() -> GameService:
    return __game_service
