from fastapi import FastAPI

from app.api import game_routes
from app.api import play_routes
from app.exceptions import exception_handlers

app = FastAPI(exception_handlers=exception_handlers)

app.include_router(game_routes.router)
app.include_router(play_routes.router)