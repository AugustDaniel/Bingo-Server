from fastapi import FastAPI

from api import game_routes, play_routes

app = FastAPI()

app.include_router(game_routes.router)
app.include_router(play_routes.router)
