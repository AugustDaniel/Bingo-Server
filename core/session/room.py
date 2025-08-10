from typing import List

from core.player import Player
from core.session.caller import Caller


class Room:
    def __init__(self, room_id, name, capacity):
        self.room_id: str = room_id
        self.name: str = name
        self.capacity: int = capacity
        self.players: List[Player] = []
        self.caller: Caller = Caller()

    def join_room(self, player: Player) -> bool:
        if len(self.players) < self.capacity:
            self.players.append(player)
            return True
        return False

    def leave_room(self, player: Player) -> bool:
        if len(self.players) < self.capacity:
            self.players.remove(player)
            return True
        return False

    def is_full(self) -> bool:
        return len(self.players) >= self.capacity

    def draw_number(self) -> int | None:
        return self.caller.draw()

    def is_over(self) -> bool:
        return self.caller.is_done()
