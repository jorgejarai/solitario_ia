from copy import deepcopy
from random import shuffle
from card import Card
import numpy as np

# TODO: Make class immutable (create a new instance every time a move is made)
# TODO: Check if there are no more moves available
# TODO: Hints


class SolitaireBoard:
    @staticmethod
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

    @staticmethod
    def generate_from_json(data: dict):
        """Generate a solitaire board from a JSON file."""

        stock = [Card.from_debug_str(i) for i in data["stock"]]
        waste = [Card.from_debug_str(i) for i in data["waste"]]
        foundations = {
            "S": [Card.from_debug_str(i) for i in data["foundations"]["S"]],
            "C": [Card.from_debug_str(i) for i in data["foundations"]["C"]],
            "H": [Card.from_debug_str(i) for i in data["foundations"]["H"]],
            "D": [Card.from_debug_str(i) for i in data["foundations"]["D"]],
        }
        tableau = [
            [Card.from_debug_str(i) if i is not None else None for i in j]
            for j in data["tableau"]
        ]

        return SolitaireBoard(tableau, foundations, stock, waste)  # type: ignore

    def __init__(
        self,
        tableau: list[list[Card]],
        foundations: dict[str, list[Card]],
        stock: list[Card],
        waste: list[Card],
    ):
        """Initialize a solitaire board with the given parameters."""
        self.tableau = tableau
        self.foundations = foundations
        self.stock = stock
        self.waste = waste
        self.consecutive_d_count = 0
        self.last_m_moves = []

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
            if not last_dest_card.is_right_next(first_moving_card):
                raise ValueError("Cards must be descending")
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
            if not self.tableau[from_col][i].is_right_next(
                self.tableau[from_col][i + 1]
            ):
                raise ValueError(f"Cards must be descending")

    def __show_last_card(self, col):
        """Shows the last card in the given column, if it is hidden."""
        done = False
        if len(self.tableau[col]) > 0:
            self.tableau[col][-1].hidden = False
            done = True

        return done

    def __check_card_to_foundation(self, card):
        """Checks if the given card can be added to the foundation."""
        # If foundation is empty, only A can be added
        if len(self.foundations[card.suit]) == 0:
            if card.number != "A":
                raise ValueError(f"Invalid card {card}")

        # If foundation is not empty, the new card must be next in order
        # to the last card in the foundation (e. g. if the last card is 5,
        # the new card must be 6)
        if len(self.foundations[card.suit]) > 0:
            last_card = self.foundations[card.suit][-1]
            if not last_card.is_right_before(card):
                raise ValueError(f"Invalid card {card}")

        return True

    def move_within_tableau(self, from_col, to_col, size=1):
        """Moves the given number of cards from one column to another in the
        tableau."""
        self.__check_tableau_range(from_col, to_col, size)

        # Move the cards
        cards = self.tableau[from_col][-size:]
        self.tableau[from_col] = self.tableau[from_col][:-size]
        self.tableau[to_col] += cards

        # Show last card in the origin column
        return self.__show_last_card(from_col)

    def draw_from_stock(self):
        """Draws a card from the stock."""
        # If the stock is empty, move the waste to the stock and reverse it
        if len(self.stock) == 0:
            self.stock = self.waste
            self.stock.reverse()
            self.waste = []

        self.waste.append(self.stock.pop())

    def move_to_foundation(self, col):
        """Moves the last card in the given column to the foundation."""
        if len(self.tableau[col]) == 0:
            raise ValueError(f"Column {col} is empty")

        # Take the last card in the column
        card = self.tableau[col][-1]

        self.__check_card_to_foundation(card)

        self.foundations[card.suit].append(self.tableau[col].pop())

        # Show last card in the origin column
        self.__show_last_card(col)

    def move_from_waste(self, col):
        """Moves the last card in the waste to the given column in the tableau."""
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

            if not last_card.is_right_next(card):
                raise ValueError(f"Invalid card {card} (not in descending order)")

        self.tableau[col].append(self.waste.pop())

    def move_from_waste_to_foundation(self):
        """Moves the last card in the waste to the foundation."""
        if len(self.waste) == 0:
            raise ValueError("Waste is empty")

        card = self.waste[-1]

        self.__check_card_to_foundation(card)

        self.foundations[card.suit].append(self.waste.pop())

    def move_from_foundation_to_tableau(self, suit, col):
        """Moves the last card in the given foundation to the given column in
        the tableau."""
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

            if not last_card.is_right_next(card):
                raise ValueError(f"Invalid card {card} (not in descending order)")

        self.tableau[col].append(self.foundations[suit].pop())

    def check_if_won(self):
        """Checks if the game has been won."""
        for suit in self.foundations:
            if len(self.foundations[suit]) != 13:
                return False

        return True

    def check_if_ready_to_win(self):
        """Checks if the tableau is ready to win, that is, if all the cards are
        in the tableau, are visible, and are in descending order."""
        if len(self.stock) > 0 or len(self.waste) > 0:
            return False

        for col in self.tableau:
            if len(col) == 0:
                continue

            if col[-1].hidden:
                return False

            for i in range(len(col) - 1):
                if not col[i].is_right_next(col[i + 1]):
                    return False

        return True

    def play_move(self, move: tuple | list):
        """Plays a move on the board. The move is a tuple or list, where the
        first element is the command, and the rest are its arguments. The
        syntax is the same as the one used in the game."""
        prev_sol = deepcopy(self)

        command = move[0]
        if command == "m":
            from_pile = int(move[1])
            to_pile = int(move[2])
            slice_length = int(move[3]) if len(move) > 3 else 1

            self.move_within_tableau(from_pile, to_pile, slice_length)
        elif command == "d":
            self.draw_from_stock()
        elif command == "f":
            pile = int(move[1])
            self.move_to_foundation(pile)
        elif command == "w":
            pile = int(move[1])
            self.move_from_waste(pile)
        elif command == "s":
            self.move_from_waste_to_foundation()
        elif command == "b":
            suit = move[1]
            col = int(move[2])

            self.move_from_foundation_to_tableau(suit, col)

        return prev_sol

    def get_empty_columns(self):
        """Returns a list of the empty columns in the tableau."""
        return [i for i in range(7) if len(self.tableau[i]) == 0]

    def play_move_reward(self, move: tuple | list):
        """Plays a move on the board and returns its associated reward. The
        move is a tuple or list, where the first element is the command, and the
        rest are its arguments. The syntax is the same as the one used in the
        game."""

        ret = 0

        empty_columns_before = self.get_empty_columns()

        command = move[0]
        if command == "m":
            self.consecutive_d_count = 0
            from_pile = int(move[1])
            to_pile = int(move[2])
            slice_length = int(move[3]) if len(move) > 3 else 1

            did_reveal_cards = self.move_within_tableau(
                from_pile, to_pile, slice_length
            )

            self.last_m_moves.append(
                (from_pile, to_pile, slice_length, did_reveal_cards)
            )

            # If the move revealed cards, the reward is 5
            # if did_reveal_cards:
            #     ret += 5

            # If the last_m_moves list has more than 5 elements, remove the first elements
            # until it has 5 elements
            while len(self.last_m_moves) > 5:
                self.last_m_moves.pop(0)

            ret = -5
        elif command == "d":
            if len(self.waste) == 0:
                # Increment counter for consecutive 'd' actions without any movement from the waste pile
                self.consecutive_d_count += 1
            else:
                # Reset the counter if the waste pile is not empty
                self.consecutive_d_count = 0
            self.draw_from_stock()
            ret = -40
        elif command == "f":
            self.consecutive_d_count = 0
            pile = int(move[1])
            suit = self.tableau[pile][-1].suit
            self.move_to_foundation(pile)
            ret = 10 * 2 ** len(self.foundations[suit])
        elif command == "w":
            self.consecutive_d_count = 0
            pile = int(move[1])
            self.move_from_waste(pile)
            ret = -5
        elif command == "s":
            self.consecutive_d_count = 0
            suit = self.waste[-1].suit
            self.move_from_waste_to_foundation()
            ret = 10 * 2 ** len(self.foundations[suit])
        elif command == "b":
            self.consecutive_d_count = 0
            suit = move[1]
            col = int(move[2])
            self.move_from_foundation_to_tableau(suit, col)
            ret = -10 * 4 ** len(self.foundations[suit])

        empty_columns_after = self.get_empty_columns()

        # Si se ha vaciado una columna, se premia con 10 por cada columna
        # vaciada
        if len(empty_columns_after) > len(empty_columns_before):
            ret += 10 * (len(empty_columns_after) - len(empty_columns_before))

        # Penalize for consecutive 'd' actions without any movement from the waste pile
        penalty_factor = 5  # Adjust the penalty factor as needed
        ret -= self.consecutive_d_count * penalty_factor

        # Penalize if an 'm' move is made that is the opposite of the previous 'm' moves
        # only if the previous 'm' moves were not made to reveal cards
        if len(self.last_m_moves) > 0:
            for m_move in self.last_m_moves[:-1]:
                if (
                    m_move[0] == self.last_m_moves[-1][1]
                    and m_move[1] == self.last_m_moves[-1][0]
                    and m_move[2] == self.last_m_moves[-1][2]
                    and not m_move[3]
                ):
                    ret -= 10

        if self.check_if_won():
            ret = 100000

        return ret

    def export(self):
        """Exports the state of the game to a dictionary."""

        ret = {}

        ret["stock"] = [i.debug_str().strip() for i in self.stock]
        ret["waste"] = [i.debug_str().strip() for i in self.waste]
        ret["foundations"] = {
            "S": [i.debug_str().strip() for i in self.foundations["S"]],
            "C": [i.debug_str().strip() for i in self.foundations["C"]],
            "H": [i.debug_str().strip() for i in self.foundations["H"]],
            "D": [i.debug_str().strip() for i in self.foundations["D"]],
        }
        ret["tableau"] = [
            [i.debug_str().strip() for i in j] for j in self.tableau  # type: ignore
        ]

        return ret

    def encode_board(self):
        """Encodes the state of the board as a one-hot vector, to be used as
        input to the neural network."""

        neurons = []

        # Encode stock
        for i in range(24):
            if i < len(self.stock):
                card = self.stock[i]
                neurons.append(card.encode())
            else:
                neurons.append([0] * 17)

        # Encode waste
        for i in range(24):
            if i < len(self.waste):
                card = self.waste[i]
                neurons.append(card.encode())
            else:
                neurons.append([0] * 17)

        # Encode foundations
        for suit in ["S", "C", "H", "D"]:
            for i in range(13):
                if i < len(self.foundations[suit]):
                    card = self.foundations[suit][i]
                    neurons.append(card.encode())
                else:
                    neurons.append([0] * 17)

        # Encode tableau
        for col in self.tableau:
            for i in range(20):
                if i < len(col):
                    card = col[i]
                    neurons.append(card.encode())
                else:
                    neurons.append([0] * 17)

        return np.array(neurons).flatten()
