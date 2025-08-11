from fastapi import FastAPI

from api import game_routes, play_routes
from exceptions import exception_handlers

app = FastAPI(exception_handlers=exception_handlers)

app.include_router(game_routes.router)
app.include_router(play_routes.router)