from typing import List

from fastapi import APIRouter

from models import Room

router = APIRouter(prefix="/game", tags=["game"])

