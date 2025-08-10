import random
from typing import List


class Caller:
    def __init__(self):
        self.draws: List[int] = []
        self.available_draws: List[int] = list(range(1, 75 + 1))

    def draw(self) -> int | None:
        if not self.available_draws:
            return None

        draw = random.choice(self.available_draws)
        self.draws.append(draw)
        self.available_draws.remove(draw)
        return draw

    def is_done(self) -> bool:
        return not self.available_draws
