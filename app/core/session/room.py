from enum import Enum
from typing import Dict

from app.core.player import Player
from app.core.session.caller import Caller
from app.exceptions import RoomFull, InvalidPlayer
from ..bingo_card import BingoCardFactory, BingoCard


class BingoProgress(Enum):
    LINE = "line"
    DOUBLE_LINE = "double_line"
    FULL_CARD = "full_card"


class Room:
    def __init__(self, room_id: str, name: str, capacity: int):
        self.room_id: str = room_id
        self.name: str = name
        self.capacity: int = capacity
        self.players: Dict[str, Player] = {}  # player_id -> Player
        self.caller: Caller = Caller()
        self.is_started: bool = False
        self.progress: BingoProgress = BingoProgress.LINE

    def join(self, player: Player) -> None:
        if self.is_full():
            raise RoomFull("Room is full")

        if player.id in self.players:
            raise InvalidPlayer("Player is already in the room")

        self.players[player.id] = player
        player.cards.append(BingoCardFactory.create())

    def leave(self, player: Player) -> None:
        if player.id not in self.players:
            raise InvalidPlayer("Player not in room")

        self.players.pop(player.id)

    def is_full(self) -> bool:
        return len(self.players) >= self.capacity

    def draw_number(self) -> int | None:
        return self.caller.draw()

    def is_over(self) -> bool:
        return self.caller.is_done

    def check_bingo(self, player: Player) -> bool:
        draws = self.caller.draws
        bingo_card: BingoCard = player.cards[0]

        full_columns = sum(
            all(
                cell.scratched and cell.content in draws
                for cell in row
            )
            for row in bingo_card.card
        )

        full_rows = sum(
            all(
                column[index].scratched and column[index].content in draws
                for column in bingo_card.card
            )
            for index in range(len(bingo_card.card))
        )

        total = full_columns + full_rows

        match self.progress:
            case BingoProgress.FULL_CARD:
                if total >= 5:
                    self.caller.is_done = True
                    return  True
            case BingoProgress.DOUBLE_LINE:
                if total >= 2:
                    self.progress = BingoProgress.FULL_CARD
                    return True
            case BingoProgress.LINE:
                if total >= 1:
                    self.progress = BingoProgress.DOUBLE_LINE
                    return True
        return False
