#!/usr/bin/env python3

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
