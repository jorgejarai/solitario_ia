from random import shuffle
from card import Card

# TODO: Make class immutable (create a new instance every time a move is made)
# TODO: Check if there are no more moves available
# TODO: Check if the game is won
# TODO: Hints


class SolitaireBoard:
    def generate_random():
        """Generate a random solitaire board."""
        cards = [Card(n, s) for s in Card.suits for n in Card.numbers]
        shuffle(cards)

        tableau: list[list[Card]] = [[], [], [], [], [], [], []]
        foundations: dict[str, list[Card]] = {"C": [], "S": [], "H": [], "D": []}
        stock: list[Card] = []
        waste: list[Card] = []

        # Populate the tableau
        for i in range(7):
            for j in range(i + 1):
                card = cards.pop()

                # The last card in each pile is visible
                if j != i:
                    card.hidden = True

                tableau[i].append(card)

        # The remaining cards go to the stock
        stock = cards

        return SolitaireBoard(tableau, foundations, stock, waste)

    def __init__(
        self,
        tableau: list[list[Card]],
        foundations: dict[str, list[Card]],
        stock: list[Card],
        waste: list[Card],
    ):
        self.tableau = tableau
        self.foundations = foundations
        self.stock = stock
        self.waste = waste

    def print_game(self):
        """Prints the current state of the game."""

        # Print the stock
        if len(self.stock) > 0:
            print(f"XXX", end="")
        else:
            print(f"___", end="")

        # Print the last card in the waste (if there is one)
        last_waste = self.waste[-1] if len(self.waste) > 0 else "___"
        print(f" {last_waste}", end="")

        print("     ", end="")

        # Print the foundations
        last_hearts = (
            self.foundations["H"][-1] if len(self.foundations["H"]) > 0 else "___"
        )
        last_diamonds = (
            self.foundations["D"][-1] if len(self.foundations["D"]) > 0 else "___"
        )
        last_clubs = (
            self.foundations["C"][-1] if len(self.foundations["C"]) > 0 else "___"
        )
        last_spades = (
            self.foundations["S"][-1] if len(self.foundations["S"]) > 0 else "___"
        )

        print(f"{last_clubs} {last_spades} {last_hearts} {last_diamonds}")
        print()

        # Print the tableau
        print(" 0   1   2   3   4   5   6")

        padded_tableau = [row + ["   "] * (20 - len(row)) for row in self.tableau]

        for card in zip(*padded_tableau):
            if all(c == "   " for c in card):
                continue
            print(*card)
        print()

    def __check_tableau_range(self, from_col, to_col, size=1):
        """Checks if the range of cards to move is valid (follows the game
        rules about card order, alternating colors, among others)."""

        # Check if the origin and destination columns are valid
        if from_col < 0 or from_col > 6:
            raise ValueError(f"Invalid column {from_col}")
        if to_col < 0 or to_col > 6:
            raise ValueError(f"Invalid column {to_col}")

        # Check if the size of the slice is valid
        if size < 1 or size > 20:
            raise ValueError(f"Invalid size {size}")

        if len(self.tableau[from_col]) < size:
            raise ValueError(f"Invalid size {size}")

        # Check if the origin column has any hidden cards
        if any(card.hidden for card in self.tableau[from_col][-size:]):
            raise ValueError(f"Cannot move hidden cards")

        # Check if the last card in the destination column is next in order to
        # the first card in the moving range and has a different color
        if len(self.tableau[to_col]) > 0:
            last_dest_card = self.tableau[to_col][-1]
            first_moving_card = self.tableau[from_col][-size]

            if last_dest_card.color() == first_moving_card.color():
                raise ValueError("Colors must alternate")

            # Check if the last card in the destination column and the
            # first card in the moving range are next to each other
            # in number
            if not last_dest_card.is_right_before(first_moving_card):
                raise ValueError("Cards must be descending b")
        else:
            # Check if the first card in the moving range is a king
            if self.tableau[from_col][-size].number != "K":
                raise ValueError(f"Column must start with a K")

        if size == 1:
            return

        # Check if the cards in the moving range are alternating colors
        for i in range(-size, -1, 1):
            if (
                self.tableau[from_col][i].color()
                == self.tableau[from_col][i + 1].color()
            ):
                raise ValueError(f"Cards must alternate colors")

        # Check if the cards in the moving range are ordered in descending order
        for i in range(-size, -1, 1):
            if not self.tableau[from_col][i].is_right_before(
                self.tableau[from_col][i + 1]
            ):
                raise ValueError(f"Cards must be descending order")

    def __show_last_card(self, col):
        if len(self.tableau[col]) > 0:
            self.tableau[col][-1].hidden = False

    def __check_card_to_foundation(self, card):
        # If foundation is empty, only A can be added
        if len(self.foundations[card.suit]) == 0:
            if card.number != "A":
                raise ValueError(f"Invalid card {card}")

        # If foundation is not empty, the card must be next in order
        if len(self.foundations[card.suit]) > 0:
            last_card = self.foundations[card.suit][-1]
            if not last_card.is_right_next(card):
                raise ValueError(f"Invalid card {card}")

        return True

    def move_within_tableau(self, from_col, to_col, size=1):
        self.__check_tableau_range(from_col, to_col, size)

        # Move the cards
        cards = self.tableau[from_col][-size:]
        self.tableau[from_col] = self.tableau[from_col][:-size]
        self.tableau[to_col] += cards

        # Show last card in the origin column
        self.__show_last_card(from_col)

    def draw_from_stock(self):
        # If the stock is empty, move the waste to the stock and reverse it
        if len(self.stock) == 0:
            self.stock = self.waste
            self.stock.reverse()
            self.waste = []

        self.waste.append(self.stock.pop())

    def move_to_foundation(self, col):
        if len(self.tableau[col]) == 0:
            raise ValueError(f"Column {col} is empty")

        # Take the last card in the column
        card = self.tableau[col][-1]

        self.__check_card_to_foundation(card)

        self.foundations[card.suit].append(self.tableau[col].pop())

        # Show last card in the origin column
        self.__show_last_card(col)

    def move_from_waste(self, col):
        if len(self.waste) == 0:
            raise ValueError("Waste is empty")

        card = self.waste[-1]

        # If column is empty, only K can be added
        if len(self.tableau[col]) == 0:
            if card.number != "K":
                raise ValueError(f"Invalid card {card}")

        # If column is not empty, the card must be next in order
        if len(self.tableau[col]) > 0:
            last_card = self.tableau[col][-1]

            if last_card.color() == card.color():
                raise ValueError(f"Invalid card {card} (colors must alternate)")

            if not last_card.is_right_before(card):
                raise ValueError(f"Invalid card {card} (not in descending order)")

        self.tableau[col].append(self.waste.pop())

    def move_from_waste_to_foundation(self):
        if len(self.waste) == 0:
            raise ValueError("Waste is empty")

        card = self.waste[-1]

        self.__check_card_to_foundation(card)

        self.foundations[card.suit].append(self.waste.pop())

    def move_from_foundation_to_tableau(self, suit, col):
        if len(self.foundations[suit]) == 0:
            raise ValueError(f"Foundation {suit} is empty")

        card = self.foundations[suit][-1]

        # If column is empty, only K can be added
        if len(self.tableau[col]) == 0:
            if card.number != "K":
                raise ValueError(f"Invalid card {card}")
        else:
            # If column is not empty, the card must be next in order
            last_card = self.tableau[col][-1]
            if last_card.color() == card.color():
                raise ValueError(f"Invalid card {card} (colors must alternate)")

            if not last_card.is_right_before(card):
                raise ValueError(f"Invalid card {card} (not in descending order)")

        self.tableau[col].append(self.foundations[suit].pop())

    def check_if_won(self):
        for suit in self.foundations:
            if len(self.foundations[suit]) != 13:
                return False

        return True
