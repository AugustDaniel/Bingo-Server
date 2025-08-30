from app.core import Room, Game, Player, BingoCard
from app.models import RoomModel, GameModel, PlayerModel, BingoCardModel, BingoCardCellModel


def map_room_to_response(room: Room) -> RoomModel:
    return RoomModel(
        room_id=room.room_id,
        name=room.name,
        player_count=len(room.players),
        capacity=room.capacity,
        is_full=room.is_full()
    )


def map_game_to_response(game: Game) -> GameModel:
    return GameModel(
        rooms=[map_room_to_response(game.rooms[room]) for room in game.rooms],
        max_capacity=game.max_capacity,
        max_rooms=game.max_rooms,
    )


def map_player_to_response(player: Player) -> PlayerModel:
    return PlayerModel(
        name=player.name,
        id=player.id,
    )


def map_bingo_card_to_response(bingo_card: BingoCard) -> BingoCardModel:
    return BingoCardModel(
        card=[
            [
                BingoCardCellModel(
                    content=cell.content,
                    scratched=cell.scratched,
                )
                for cell in column
            ]
            for column in bingo_card.card
        ]
    )
