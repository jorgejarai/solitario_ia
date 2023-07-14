from solitaire_board import SolitaireBoard
from copy import deepcopy

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


class LegalMoveChecker:
    __move_dict = []

    def __populate_move_dict(self):
        self.__move_dict = []

        # Move within tableau
        for from_pile in range(7):
            for to_pile in range(7):
                if from_pile == to_pile:
                    continue

                for slice_length in range(1, 21):
                    self.__move_dict.append(("m", from_pile, to_pile, slice_length))

        # Draw from stock
        self.__move_dict.append(("d",))

        # Move to foundation
        for pile in range(7):
            self.__move_dict.append(("f", pile))

        # Move from waste
        for pile in range(7):
            self.__move_dict.append(("w", pile))

        # Move from waste to foundation
        self.__move_dict.append(("s",))

        # # Move from foundation to tableau
        # for suit in ["S", "C", "H", "D"]:
        #     for col in range(7):
        #         self.__move_dict.append(("b", suit, col))

        # Undo move
        # self.__move_dict.append(("u",))

    def __init__(self, board: SolitaireBoard):
        self.board = board

        self.__populate_move_dict()

    def get_legal_moves(self):
        f_moves = self.check_f_moves()
        w_moves = self.check_w_moves()
        d_moves = self.check_d_moves()
        s_moves = self.check_s_moves()
        m_moves = self.check_m_moves()
        # b_moves = self.check_b_moves()

        ret = []

        if len(f_moves) > 0:
            for i in f_moves:
                ret.append(("f", i))

        if len(w_moves) > 0:
            for i in w_moves:
                ret.append(("w", i))

        if d_moves:
            ret.append(("d",))

        if s_moves:
            ret.append(("s",))

        if len(m_moves) > 0:
            for i in m_moves:
                ret.append(("m", *i))

        # if len(b_moves) > 0:
        #     for i in b_moves:
        #         ret.append(("b", *i))

        return ret

    def check_f_moves(self):
        ret = []

        for i in range(7):
            test_board = deepcopy(self.board)
            try:
                test_board.move_to_foundation(i)
                ret.append(i)
            except ValueError:
                continue

        return ret

    def check_w_moves(self):
        ret = []

        for i in range(7):
            test_board = deepcopy(self.board)
            try:
                test_board.move_from_waste(i)
                ret.append(i)
            except ValueError:
                continue

        return ret

    def check_d_moves(self):
        return len(self.board.stock) > 0 or len(self.board.waste) > 0

    def check_s_moves(self):
        test_board = deepcopy(self.board)
        try:
            test_board.move_from_waste_to_foundation()
            return True
        except ValueError:
            return False

    def check_m_moves(self):
        ret = []

        for i in range(7):
            # If the column is empty, skip it
            if len(self.board.tableau[i]) == 0:
                continue

            # If the columns starts with a not hidden K, skip it
            # (moving a K if it's already visible is redundant)
            if (
                not self.board.tableau[i][0].hidden
                and self.board.tableau[i][0].number == "K"
            ):
                continue

            for j in range(7):
                col_len = len(self.board.tableau[i])

                for k in range(1, col_len + 1):
                    test_board = deepcopy(self.board)
                    try:
                        test_board.move_within_tableau(i, j, k)
                        ret.append((i, j, k))
                    except ValueError:
                        continue

        return ret

    def check_b_moves(self):
        ret = []

        for i in ["C", "D", "H", "S"]:
            for j in range(7):
                test_board = deepcopy(self.board)
                try:
                    test_board.move_from_foundation_to_tableau(i, j)
                    ret.append((i, j))
                except ValueError:
                    continue

        return ret

    def encode_legal_moves(self):
        legal_moves = self.get_legal_moves()

        ret = []
        for move in self.__move_dict:
            if move in legal_moves:
                ret.append(1)
            else:
                ret.append(0)

        return ret

    def decode_move(self, move):
        return self.__move_dict[move]
