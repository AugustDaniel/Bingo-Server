from typing import Dict

from core.player import Player
from core.session.caller import Caller
from exceptions import RoomFull, InvalidPlayer


class Room:
    def __init__(self, room_id: str, name: str, capacity: int):
        self.room_id: str = room_id
        self.name: str = name
        self.capacity: int = capacity
        self.players: Dict[str, Player] = {} # player_id -> Player
        self.caller: Caller = Caller()
        self.is_started: bool = False

    def join(self, player: Player) -> None:
        if self.is_full():
            raise RoomFull("Room is full")

        if player.id in self.players:
            raise InvalidPlayer("Player is already in the room")

        self.players[player.id] = player

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
