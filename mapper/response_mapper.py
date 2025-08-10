from core.room import Room
from models.room_model import RoomModel


def map_room_to_response(room: Room) -> RoomModel:
    return RoomModel(
        room_id=room.room_id,
        name=room.name,
        capacity=room.capacity,
        is_full=room.is_full()
    )