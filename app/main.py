from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import game_routes
from app.api import play_routes
from app.exceptions import exception_handlers

app = FastAPI(exception_handlers=exception_handlers)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game_routes.router)
app.include_router(play_routes.router)
