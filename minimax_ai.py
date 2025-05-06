import copy
from board import valid_moves, make_move, opponent, EMPTY, BOARD_SIZE

class MinimaxAgent:
    def __init__(self, color, depth=3):
        self.color = color
        self.depth = depth

    def get_move(self, board):
        moves = valid_moves(board, self.color)
        if not moves:
            return None

        best_score = float("-inf")
        best_move = None

        for move in moves:
            new_board = copy.deepcopy(board)
            make_move(new_board, self.color, *move)
            score = self.minimax(new_board, self.depth - 1, False, opponent(self.color))
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def minimax(self, board, depth, maximizing, current_color):
        moves = valid_moves(board, current_color)

        if depth == 0 or not moves:
            return self.evaluate(board)

        if maximizing:
            max_eval = float("-inf")
            for move in moves:
                new_board = copy.deepcopy(board)
                make_move(new_board, current_color, *move)
                eval = self.minimax(new_board, depth - 1, False, opponent(current_color))
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float("inf")
            for move in moves:
                new_board = copy.deepcopy(board)
                make_move(new_board, current_color, *move)
                eval = self.minimax(new_board, depth - 1, True, opponent(current_color))
                min_eval = min(min_eval, eval)
            return min_eval

    def evaluate(self, board):
        # Évaluation simple : score pondéré coins + nombre de pions
        score = 0
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if board[x][y] == self.color:
                    score += 1
                elif board[x][y] == opponent(self.color):
                    score -= 1

        # Bonus pour les coins
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        for x, y in corners:
            if board[x][y] == self.color:
                score += 10
            elif board[x][y] == opponent(self.color):
                score -= 10
        return score
