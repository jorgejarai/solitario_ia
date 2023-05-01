#!/usr/bin/env python3

from solitaire_board import SolitaireBoard


def main():
    sol = SolitaireBoard.generate_random()

    while True:
        sol.print_game()
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
