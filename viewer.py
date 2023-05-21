#!/usr/bin/env python3

import json
import sys
from solitaire_board import SolitaireBoard

"""
This script is used to view the moves generated by the solver. It takes a single
argument, which is the path to a JSON file containing the board state and the
moves to make. The JSON file should be in the same format as the output of
solver.py.

The moves are printed to the screen one at a time, and the user must press enter
to see the next move. This allows the user to see the moves being made and
understand how the solver works.
"""


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <board_file>", file=sys.stderr)
        sys.exit(1)

    board_json = None

    with open(sys.argv[1], "r") as f:
        board_json = f.read()
        board_json = json.loads(board_json)

    board = SolitaireBoard.generate_from_json(board_json)

    for i, move in enumerate(board_json["moves"]):
        sys.stdout.write("\033[2J\033[H")

        print(f"Move {i + 1} of {len(board_json['moves'])}")
        print(f"Next move: {move}")

        board.print_game()
        sys.stdout.flush()

        input()

        board.play_move(move)


if __name__ == "__main__":
    main()
