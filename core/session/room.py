from typing import List

from core.player import Player
from core.session.caller import Caller
from exceptions import RoomFull, InvalidPlayer


class Room:
    def __init__(self, room_id, name, capacity):
        self.room_id: str = room_id
        self.name: str = name
        self.capacity: int = capacity
        self.players: List[Player] = []
        self.caller: Caller = Caller()

    def join(self, player: Player) -> None:
        if self.is_full():
            raise RoomFull("Room is full")

        self.players.append(player)

    def leave(self, player: Player) -> None:
        if player not in self.players:
            raise InvalidPlayer("Player not in room")

        self.players.remove(player)

    def is_full(self) -> bool:
        return len(self.players) >= self.capacity

    def draw_number(self) -> int | None:
        return self.caller.draw()

    def is_over(self) -> bool:
        return self.caller.is_done()
