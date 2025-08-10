from typing import List

from core.bingo_card.cell import CardCell


class Card:
    card = List[List[CardCell]]

    def __init__(self, card: List[List[CardCell]]):
        self.card: List[List[CardCell]] = card