#!/usr/bin/env python3

import sys
import networkx as nx
import os
from legal_moves import LegalMoveChecker
from solitaire_board import SolitaireBoard
from copy import deepcopy
from random import shuffle
import json
import datetime


def export_board(board: SolitaireBoard, moves: list[tuple]):
    """Exports a given SolitaireBoard instance to a JSON file, including the
    moves used to arrive to a solution from this board."""

    if not os.path.exists("boards"):
        os.makedirs("boards")

    timestamp = datetime.datetime.now().isoformat(timespec="seconds")

    exported_board = board.export()
    exported_board["moves"] = moves

    with open(f"boards/board-{timestamp}.json", "w") as f:
        json.dump(exported_board, f)


def dfs_traversal(start_node: SolitaireBoard, max_nodes: int, max_depth: int = 150):
    """Traverses through the possible moves for a given SolitaireBoard using DFS.

    If any solution is found, the initial card configuration is saved to a JSON
    file."""

    graph = nx.DiGraph()
    visited = set()  # Set to keep track of visited nodes
    stack = [start_node]  # Stack to store nodes to be visited and their parent

    while stack:
        # Get the next node and its parent from the stack
        current_node = stack.pop()

        # If depth of current node is more than 150, skip
        if len(stack) > max_depth:
            continue

        if current_node not in visited:
            if graph.number_of_nodes() % 100 == 0:
                current_node.print_game()

            visited.add(current_node)
            graph.add_node(current_node)

            if current_node.check_if_won():
                print("You won!")
                print("Number of nodes:", graph.number_of_nodes())
                print("Number of edges:", graph.number_of_edges())
                print("Depth:", len(stack))

                # Get the moves that led to the winning board
                # shortest path from start_node to current_node
                winning_moves = []

                shortest_path = nx.shortest_path(graph, start_node, current_node)
                edges = [
                    (shortest_path[i], shortest_path[i + 1])
                    for i in range(len(shortest_path) - 1)
                ]

                for from_node, to_node in edges:
                    edge = graph.get_edge_data(from_node, to_node)
                    print(edge)

                    winning_moves.append(edge["move"])

                print("Moves:", len(winning_moves))
                export_board(start_node, winning_moves)
                return graph

            legal_checker = LegalMoveChecker(current_node)
            legal_moves = legal_checker.get_legal_moves()
            shuffle(legal_moves)

            # Add all legal moves to the stack
            for move in legal_moves:
                new_node = deepcopy(current_node)
                new_node.play_move(move)

                graph.add_node(new_node)
                graph.add_edge(current_node, new_node, move=move)

                if graph.number_of_nodes() > max_nodes:
                    print("Max nodes exceeded")
                    return

                stack.append(new_node)


def main():
    max_nodes = 1_000_000

    initial_board = None
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            board_json = f.read()
            board_json = json.loads(board_json)

        initial_board = SolitaireBoard.generate_from_json(board_json)
    else:
        initial_board = SolitaireBoard.generate_random()

    dfs_traversal(initial_board, max_nodes)


if __name__ == "__main__":
    main()
