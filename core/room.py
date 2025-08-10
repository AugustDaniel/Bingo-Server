from typing import List

from .player import Player


class Room:
    def __init__(self, room_id, name, capacity):
        self.room_id: str = room_id
        self.name: str = name
        self.capacity: int = capacity
        self.players: List[Player] = []

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