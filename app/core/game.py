from typing import Dict

from .player import Player
from app.core.session.room import Room
from app.exceptions import MaxRoomsReached, CapacityTooHigh, RoomNotFound, InvalidPlayer

import uuid


class Game:
    def __init__(self):
        self.rooms: Dict[str, Room] = {} # room_id -> Room
        self.max_capacity: int = 20
        self.max_rooms: int = 20
        self.players: Dict[str, Player] = {} # player_id -> Player

    def create_new_room(self, name: str = "room", capacity: int | None = None) -> Room:
        if len(self.rooms) >= self.max_rooms:
            raise MaxRoomsReached("Max rooms reached")

        if capacity is None:
            capacity = self.max_capacity
        elif capacity > self.max_capacity:
            raise CapacityTooHigh("Capacity too high")

        room = Room(str(uuid.uuid4()), name, capacity)
        self.rooms[room.room_id] = room
        return room

    def create_new_player(self, player_name: str) -> Player:
        player = Player(player_id=str(uuid.uuid4()), name=player_name)
        self.players[player.id] = player
        return player

    def remove_room(self, room: Room) -> None:
        if room and room.room_id in self.rooms:
            for player_id in self.rooms[room.room_id].players:
                self.players.pop(player_id)
            room.caller.is_done = True
            del self.rooms[room.room_id]
        else:
            raise RoomNotFound("Invalid room")

    def add_player_to_room(self, player: Player, room: Room) -> None:
        if not room or room.room_id not in self.rooms:
            raise RoomNotFound("Invalid room")

        if not player:
            raise InvalidPlayer("Invalid player")

        room.join(player)
