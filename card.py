"""
solitario_ia
Copyright (C) 2023 Aníbal Ibaceta, Sebastián Hevia & Jorge Jara

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


class Card:
    suits = ["C", "S", "H", "D"]  # Tréboles, picas, corazones, diamantes
    numbers = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

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
        """Creates a new card. `number` is the number of the card, and `suit` is
        the suit of the card. `hidden` is a boolean that indicates whether the
        card should be hidden or not."""
        if number not in self.numbers:
            raise ValueError(f"Invalid number {number}")
        if suit not in self.suits:
            raise ValueError(f"Invalid suit {suit}")

        self.number = number
        self.suit = suit
        self.hidden = hidden

    def __str__(self) -> str:
        """Returns a string representation of the card that can be printed to
        a terminal."""
        if self.hidden:
            return "XXX"

        return f"\033[{self.suit_colors[self.suit]};1m{self.number:>2}{self.suit_glyphs[self.suit]}\033[0m"

    def __repr__(self) -> str:
        return str(self)

    def is_right_before(self, other):
        """Returns `True` if the card is right before the other card in
        the traditional order (e. g. 2 of hearts is right before 3 of hearts).
        The suit is ignored."""
        return self.numbers.index(self.number) - self.numbers.index(other.number) == -1

    def is_right_next(self, other):
        """Returns `True` if the card is right next to the other card in the
        traditional order (e. g. king of hearts is right next to queen of
        hearts). The suit is ignored."""
        return self.numbers.index(self.number) - self.numbers.index(other.number) == 1

    def color(self):
        """Returns the color of the card, either "red" or "black"."""
        if self.suit in ["H", "D"]:
            return "red"
        else:
            return "black"

    def debug_str(self):
        """Returns a string representation of the card that can be used to
        reconstruct it."""
        if self.hidden:
            return f"{self.number}{self.suit}X"
        else:
            return f"{self.number}{self.suit}"

    @staticmethod
    def from_debug_str(debug_str: str):
        """Reconstructs a card from a debug string."""
        if len(debug_str) < 2 or len(debug_str) > 4:
            raise ValueError(f"Invalid debug string {debug_str}")

        if len(debug_str) == 2:
            return Card(debug_str[0], debug_str[1], False)
        elif len(debug_str) == 3:
            if debug_str[-1] == "X":
                return Card(debug_str[0], debug_str[1], True)

            return Card(debug_str[0:2], debug_str[2], False)
        elif len(debug_str) == 4:
            return Card(debug_str[0:2], debug_str[2], True)

    def encode(self):
        """Returns a one-hot encoding of the card. The encoding is a list of
        17 elements, where the first 13 elements represent the number of the
        card, and the next 4 elements represent the suit of the card."""

        ret = [0] * 17
        ret[self.numbers.index(self.number)] = 1
        ret[13 + self.suits.index(self.suit)] = 1

        return ret
