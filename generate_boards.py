#!/usr/bin/env python3

import json
from solitaire_board import SolitaireBoard
import sys
import uuid
import os


def export_board(board: SolitaireBoard):
    """Exports a given SolitaireBoard instance to a JSON file, including the
    moves used to arrive to a solution from this board."""

    if not os.path.exists("boards/random"):
        os.makedirs("boards/random", exist_ok=True)

    board_id = str(uuid.uuid4())

    exported_board = board.export()

    with open(f"boards/random/{board_id}.json", "w") as f:
        json.dump(exported_board, f)


def main():
    if len(sys.argv) == 1:
        print(f"usage: {sys.argv[0]} <count>", file=sys.stderr)
        sys.exit(1)

    count = int(sys.argv[1])
    for _ in range(count):
        board = SolitaireBoard.generate_random()
        export_board(board)


if __name__ == "__main__":
    main()
