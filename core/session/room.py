from enum import Enum
from typing import Dict

from core.player import Player
from core.session.caller import Caller
from exceptions import RoomFull, InvalidPlayer
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
        return self.caller.is_done()

    def check_bingo(self, player: Player) -> bool:
        # draws = self.caller.draws
        # card: BingoCard = player.cards[0].card
        #
        # full_rows = sum(all(cell.scratched for cell in row) for row in card.card)

        return False
