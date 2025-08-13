from fastapi import Request
from starlette.responses import JSONResponse

from exceptions import *


def capacity_to_high_handler(request: Request, exception: Exception):
    return JSONResponse(status_code=400, content={"error": str(exception)})


def max_rooms_reached_handler(request: Request, exception: Exception):
    return JSONResponse(status_code=400, content={"error": str(exception)})


def invalid_player_handler(request: Request, exception: Exception):
    return JSONResponse(status_code=400, content={"error": str(exception)})


def room_full_handler(request: Request, exception: Exception):
    return JSONResponse(status_code=400, content={"error": str(exception)})


def room_not_found_handler(request: Request, exception: Exception):
    return JSONResponse(status_code=404, content={"error": str(exception)})


exception_handlers = {
    CapacityTooHigh: capacity_to_high_handler,
    MaxRoomsReached: max_rooms_reached_handler,
    InvalidPlayer: invalid_player_handler,
    RoomFull: room_full_handler,
    RoomNotFound: room_not_found_handler,
}
