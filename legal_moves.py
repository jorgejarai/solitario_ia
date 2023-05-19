from solitaire_board import SolitaireBoard
from copy import deepcopy


class LegalMoveChecker:
    def __init__(self, board: SolitaireBoard):
        self.board = board

    def get_legal_moves(self):
        f_moves = self.check_f_moves()
        w_moves = self.check_w_moves()
        d_moves = self.check_d_moves()
        s_moves = self.check_s_moves()
        m_moves = self.check_m_moves()
        b_moves = self.check_b_moves()

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

        if len(b_moves) > 0:
            for i in b_moves:
                ret.append(("b", *i))

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
