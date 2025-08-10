from fastapi import HTTPException, FastAPI
from starlette.requests import Request

from exceptions import *


def capacity_to_high_handler(request: Request, exception: Exception):
    raise HTTPException(
        status_code=400,
        detail="Capacity too high"
    )


def max_rooms_reached_handler(request: Request, exception: Exception):
    raise HTTPException(
        status_code=400,
        detail="max rooms reached"
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(CapacityTooHigh, capacity_to_high_handler)
    app.add_exception_handler(MaxRoomsReached, max_rooms_reached_handler)
