from board import valid_moves, make_move, opponent, EMPTY, BOARD_SIZE

import copy

class GreedyAgent:
    def __init__(self, color):
        self.color = color

    def get_move(self, board):
        moves = valid_moves(board, self.color)
        if not moves:
            return None

        best_score = -1
        best_move = None

        for move in moves:
            # Simuler le coup
            test_board = copy.deepcopy(board)
            make_move(test_board, self.color, *move)
            score = self.evaluate(test_board)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def evaluate(self, board):
        # Score simple : nombre de pions du joueur
        return sum(row.count(self.color) for row in board)
