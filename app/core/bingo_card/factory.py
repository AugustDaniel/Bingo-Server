import random

from app.core.bingo_card.card import BingoCard
from app.core.bingo_card.cell import BingoCardCell


class BingoCardFactory:

    @classmethod
    def create(cls) -> BingoCard:
        return cls.__create_random_card()

    @classmethod
    def __create_random_card(cls) -> BingoCard:
        card_content = []

        for i in range(5):
            min_val = i * 15 + 1
            max_val = min_val + 14

            column_content = random.sample(range(min_val, max_val + 1), 5)
            column = [BingoCardCell(content) for content in column_content]
            card_content.append(column)

        card_content[2][2] = BingoCardCell('free')

        return BingoCard(card_content)
