import random
from board import valid_moves

class RandomAgent:
    def __init__(self, color):
        self.color = color  # "B" ou "W"

    def get_move(self, board):
        moves = valid_moves(board, self.color)
        if moves:
            return random.choice(moves)
        return None  # Aucun coup possible
