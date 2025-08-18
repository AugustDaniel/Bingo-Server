from typing import List

from core.bingo_card.cell import BingoCardCell


class BingoCard:
    def __init__(self, card: List[List[BingoCardCell]]):
        self.card: List[List[BingoCardCell]] = card