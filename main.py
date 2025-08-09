from fastapi import FastAPI

from api import game_routes

app = FastAPI()

app.include_router(game_routes.router)
