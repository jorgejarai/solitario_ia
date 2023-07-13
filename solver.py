#!/usr/bin/env python3

from multiprocessing import Pool
import sys
import time
from solitaire_board import SolitaireBoard
import json
from dfs import dfs_traversal

max_nodes = 10_000
n_threads = 12
n_bench_tests = 1000


def run_dfs(board=None):
    initial_board = SolitaireBoard.generate_random() if board is None else board
    moves = dfs_traversal(initial_board, max_nodes, 150, False)

    out = f"{moves}"
    print(out)

    return out


def main():
    initial_board = None
    if len(sys.argv) > 1 and sys.argv[1] != "--bench":
        with open(sys.argv[1], "r") as f:
            board_json = f.read()
            board_json = json.loads(board_json)

        initial_board = SolitaireBoard.generate_from_json(board_json)
    elif len(sys.argv) > 1 and sys.argv[1] == "--bench":
        timestr = time.strftime("%Y%m%d-%H%M%S")
        log_file = open(f"dfs-bench-{timestr}.csv", "w")

        if len(sys.argv) > 2:
            json_files = sys.argv[2:]
            boards = []

            for json_file in json_files:
                with open(json_file, "r") as f:
                    board_json = f.read()
                    board_json = json.loads(board_json)

                boards.append(SolitaireBoard.generate_from_json(board_json))

            with Pool(n_threads) as p:
                results = p.map(run_dfs, boards)

        else:
            with Pool(n_threads) as p:
                results = p.map(run_dfs, [None] * n_bench_tests)

        log_file.write("\n".join(results))

    else:
        initial_board = SolitaireBoard.generate_random()

    dfs_traversal(initial_board, max_nodes)


if __name__ == "__main__":
    main()
