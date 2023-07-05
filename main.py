#!/usr/bin/env python3

import json
from solitaire_board import SolitaireBoard
from legal_moves import LegalMoveChecker
from copy import deepcopy
import sys

"""
This script is used to play the game interactively. It takes a single optional
argument, which is the path to a JSON file containing the initial board state.
If no argument is provided, a random board is generated. The user can then
interact with the game by typing in commands. The commands are provided in the
README.
"""


def main():
    # If a second argument is provided, use that as the initial board
    sol = None
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            board_json = f.read()
            board_json = json.loads(board_json)

        sol = SolitaireBoard.generate_from_json(board_json)
    else:
        sol = SolitaireBoard.generate_random()

    history = []

    legal_checker = LegalMoveChecker(sol)
    print(len(legal_checker.encode_legal_moves()))

    while True:
        sol.print_game()

        if sol.check_if_won():
            print("You won!")
            break

        legal_checker = LegalMoveChecker(sol)
        print(f"Can draw from stock? {legal_checker.check_d_moves()}")
        print(f"Can move from stock to foundation? {legal_checker.check_s_moves()}")
        print(f"Legal f moves: {legal_checker.check_f_moves()}")
        print(f"Legal w moves: {legal_checker.check_w_moves()}")
        print(f"Legal m moves: {legal_checker.check_m_moves()}")
        print(f"Legal b moves: {legal_checker.check_b_moves()}")

        print("Enter a command: ", end="")
        cmd = input().split(" ")

        try:
            if cmd[0] == "q":
                break
            elif cmd[0] == "u":
                if len(history) == 0:
                    raise Exception("Can't undo any further")

                sol = history.pop()
            else:
                prev_move = sol.play_move(cmd)
                history.append(prev_move)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
