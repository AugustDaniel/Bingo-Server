import random

from core.bingo_card.card import Card
from core.bingo_card.cell import CardCell


class CardFactory:

    @classmethod
    def create(cls) -> Card:
        return cls.__create_random_card()

    @classmethod
    def __create_random_card(cls) -> Card:
        card_content = []

        for i in range(5):
            min_val = i * 15 + 1
            max_val = min_val + 14

            column_content = random.sample(range(min_val, max_val + 1), 5)
            column = [CardCell(content) for content in column_content]
            card_content.append(column)

        card_content[2][2] = CardCell('free')

        return Card(card_content)
