class CardCell:
    def __init__(self, content: str | int):
        self.content: str | int = content
        self.scratched: bool = False

    def scratch(self):
        self.scratched = True