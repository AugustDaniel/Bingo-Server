from bingo_card import BingoCard


class Player:
    def __init__(self, name: str, player_id: str):
        self.id: str = player_id
        self.name: str = name
        self.cards: list[BingoCard] = []
