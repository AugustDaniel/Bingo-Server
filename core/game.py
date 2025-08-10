from typing import Dict

from core.session.room import Room
from exceptions import MaxRoomsReached, CapacityTooHigh

import uuid


class Game:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self.max_capacity: int = 20
        self.max_rooms: int = 20

    def create_new_room(self, name: str = "room", capacity: int | None = None) -> Room | None:
        if len(self.rooms) >= self.max_rooms:
            raise MaxRoomsReached("Max rooms reached")

        if capacity is None:
            capacity = self.max_capacity
        elif capacity > self.max_capacity:
            raise CapacityTooHigh("Capacity too high")

        room = Room(str(uuid.uuid4()), name, capacity)
        self.rooms[room.room_id] = room
        return room

    def remove_room(self, room: Room) -> None:
        if room.room_id in self.rooms:
            del self.rooms[room.room_id]
