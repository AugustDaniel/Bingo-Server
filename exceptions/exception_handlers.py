from fastapi import HTTPException, FastAPI, Request
from starlette.responses import JSONResponse

from exceptions import *


def capacity_to_high_handler(request: Request, exception: Exception):
    return JSONResponse(status_code=400, content={"error": "Capacity too high"})


def max_rooms_reached_handler(request: Request, exception: Exception):
    return JSONResponse(status_code=400, content={"error": "Max room reached"})


exception_handlers = {
    CapacityTooHigh: capacity_to_high_handler,
    MaxRoomsReached: max_rooms_reached_handler
}
