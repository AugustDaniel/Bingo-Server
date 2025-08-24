import random
from typing import List


class Caller:
    def __init__(self):
        self.draws: List[int] = []
        self.available_draws: List[int] = list(range(1, 75 + 1))
        self.is_done: bool = False

    def draw(self) -> int | None:
        if not self.available_draws:
            return None

        draw = random.choice(self.available_draws)
        self.draws.append(draw)
        self.available_draws.remove(draw)

        if not self.available_draws:
            self.is_done = True

        return draw
