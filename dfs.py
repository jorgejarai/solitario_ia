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


def dfs_traversal(
    start_node: SolitaireBoard,
    max_nodes: int,
    max_depth: int = 150,
    print_output: bool = True,
):
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
            if print_output and graph.number_of_nodes() % 100 == 0:
                print("\x1b[2J\x1b[H")
                print("Number of nodes:", graph.number_of_nodes())
                current_node.print_game()

            visited.add(current_node)
            graph.add_node(current_node)

            if current_node.check_if_won():
                if print_output:
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
                    winning_moves.append(edge["move"])

                if print_output:
                    print("Moves:", len(winning_moves))
                export_board(start_node, winning_moves)

                return len(winning_moves)

            legal_checker = LegalMoveChecker(current_node)
            legal_moves = legal_checker.get_legal_moves()
            shuffle(legal_moves)

            # If the board is ready to be won (all cards are in the tableau,
            # they are all face up and in order), ignore moves that don't move
            # cards to the foundation
            if current_node.check_if_ready_to_win():
                legal_moves = [move for move in legal_moves if move[0] == "f"]

            # Add all legal moves to the stack
            for move in legal_moves:
                new_node = deepcopy(current_node)
                new_node.play_move(move)

                graph.add_node(new_node)
                graph.add_edge(current_node, new_node, move=move)

                if graph.number_of_nodes() > max_nodes:
                    if print_output:
                        print("Max nodes exceeded")
                    return -1

                stack.append(new_node)
