class BingoCardCell:
    def __init__(self, content: str | int, scratched: bool = False):
        self.content: str | int = content
        self.scratched: bool = scratched

    def scratch(self):
        self.scratched = True