#!/usr/bin/env python3

from solitaire_board import SolitaireBoard
from legal_moves import LegalMoveChecker


def main():
    sol = SolitaireBoard.generate_random()

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
            elif cmd[0] == "m":
                from_pile = int(cmd[1])
                to_pile = int(cmd[2])
                slice_length = int(cmd[3]) if len(cmd) > 3 else 1
                sol.move_within_tableau(from_pile, to_pile, slice_length)
            elif cmd[0] == "d":
                sol.draw_from_stock()
            elif cmd[0] == "f":
                pile = int(cmd[1])
                sol.move_to_foundation(pile)
            elif cmd[0] == "w":
                pile = int(cmd[1])
                sol.move_from_waste(pile)
            elif cmd[0] == "s":
                sol.move_from_waste_to_foundation()
            elif cmd[0] == "b":
                suit = cmd[1]
                col = int(cmd[2])
                sol.move_from_foundation_to_tableau(suit, col)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
