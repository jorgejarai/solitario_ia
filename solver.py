#!/usr/bin/env python3

import networkx as nx
import os
# from networkx.drawing.nx_pydot import to_pydot
from legal_moves import LegalMoveChecker
from solitaire_board import SolitaireBoard
from copy import deepcopy
from random import shuffle
import json
import time


def export_board(board: SolitaireBoard):
    """Exports a given SolitaireBoard instance to a JSON file."""

    if not os.path.exists("boards"):
        os.makedirs("boards")

    timestamp = round(time.time())

    with open(f"boards/board-{timestamp}.json", "w") as f:
        json.dump(
            {
                "stock": [i.debug_str().strip() for i in board.stock],
                "waste": [i.debug_str().strip() for i in board.waste],
                "foundations": {
                    "S": [i.debug_str().strip() for i in board.foundations["S"]],
                    "C": [i.debug_str().strip() for i in board.foundations["C"]],
                    "H": [i.debug_str().strip() for i in board.foundations["H"]],
                    "D": [i.debug_str().strip() for i in board.foundations["D"]],
                },
                "tableau": [[i.debug_str().strip() for i in j] for j in board.tableau],
            },
            f,
        )


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

                export_board(start_node)
                return graph

            legal_checker = LegalMoveChecker(current_node)
            legal_moves = legal_checker.get_legal_moves()
            shuffle(legal_moves)

            # Add all legal moves to the stack
            for move in legal_moves:
                new_node = deepcopy(current_node)

                if move[0] == "m":
                    new_node.move_within_tableau(move[1], move[2], move[3])
                elif move[0] == "d":
                    new_node.draw_from_stock()
                elif move[0] == "f":
                    new_node.move_to_foundation(move[1])
                elif move[0] == "w":
                    new_node.move_from_waste(move[1])
                elif move[0] == "s":
                    new_node.move_from_waste_to_foundation()
                elif move[0] == "b":
                    new_node.move_from_foundation_to_tableau(move[1], move[2])

                graph.add_node(new_node)
                graph.add_edge(current_node, new_node, move=move)

                if graph.number_of_nodes() > max_nodes:
                    print("Max nodes exceeded")
                    return

                stack.append(new_node)


def main():
    max_nodes = 1_000_000
    initial_board = SolitaireBoard.generate_random()

    dfs_traversal(initial_board, max_nodes)

    # # Print the result graph in DOT format
    # dot_graph = to_pydot(graph)
    # print(dot_graph.to_string())

if __name__ == "__main__":
    main()
