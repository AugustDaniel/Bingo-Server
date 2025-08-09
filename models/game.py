from typing import Dict

from .room import Room

import uuid


class Game:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self.max_capacity: int = 20
        self.max_rooms: int = 20

    def create_new_room(self, name:str) -> Room | None:
        if len(self.rooms) < self.max_rooms:
            return None
        room = Room(uuid.uuid4(), name, self.max_capacity)
        self.rooms[room.room_id] = room
        return room



