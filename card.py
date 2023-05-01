class Card:
    suits = ["C", "S", "H", "D"]  # Tréboles, picas, corazones, diamantes
    numbers = ["A", "2", "3", "4", "5", "6",
               "7", "8", "9", "10", "J", "Q", "K"]

    suit_glyphs = {
        "C": "♣",
        "S": "♠",
        "H": "♥",
        "D": "♦",
    }

    suit_colors = {
        "C": "30",
        "S": "30",
        "H": "31",
        "D": "31",
    }

    def __init__(self, number, suit, hidden=False):
        if number not in self.numbers:
            raise ValueError(f"Invalid number {number}")
        if suit not in self.suits:
            raise ValueError(f"Invalid suit {suit}")

        self.number = number
        self.suit = suit
        self.hidden = hidden

    def __str__(self) -> str:
        if self.hidden:
            return "XXX"

        return f"\033[{self.suit_colors[self.suit]};1m{self.number:>2}{self.suit_glyphs[self.suit]}\033[0m"

    def __repr__(self) -> str:
        return str(self)

    def is_descending(self, other):
        """"""
        return self.numbers.index(self.number) - self.numbers.index(other.number) > 0

    def is_right_next(self, other):
        """"""
        return self.numbers.index(self.number) - self.numbers.index(other.number) == 1

    def is_right_before(self, other):
        """"""
        return self.numbers.index(self.number) - self.numbers.index(other.number) == -1

    def color(self):
        if self.suit in ["H", "D"]:
            return "red"
        else:
            return "black"
