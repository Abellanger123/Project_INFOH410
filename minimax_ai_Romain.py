from board import valid_moves, make_move, count_pieces
import copy

class MinimaxAgentRomain:
    def __init__(self, color, depth=3):
        """
        Initialize the Minimax agent.
        
        Args:
            color: The color that the agent is playing ('B' or 'W')
            depth: The maximum depth to search in the game tree
        """
        self.color = color
        self.opponent_color = 'W' if color == 'B' else 'B'
        self.depth = depth
    
    def get_move(self, board):
        """
        Get the best move according to the minimax algorithm.
        
        Args:
            board: The current game board
            
        Returns:
            The best move as a tuple (row, col) or None if no moves are available
        """
        moves = valid_moves(board, self.color)
        if not moves:
            return None
        
        best_score = float('-inf')
        best_move = None
        
        for move in moves:
            # Create a copy of the board to simulate the move
            new_board = copy.deepcopy(board)
            make_move(new_board, self.color, *move)
            
            # Get the score for this move using minimax
            score = self._minimax(new_board, self.depth - 1, False)
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def _minimax(self, board, depth, is_maximizing):
        """
        Minimax algorithm with alpha-beta pruning.
        
        Args:
            board: The current game board
            depth: Current depth in the game tree
            is_maximizing: Whether it's the maximizing player's turn
            
        Returns:
            The best score for the current board position
        """
        # If we've reached the maximum depth or the game is over, evaluate the board
        if depth == 0:
            return self._evaluate(board)
        
        current_color = self.color if is_maximizing else self.opponent_color
        moves = valid_moves(board, current_color)
        
        # If there are no valid moves, pass the turn
        if not moves:
            # If both players pass, the game is over
            opponent_moves = valid_moves(board, 'W' if current_color == 'B' else 'B')
            if not opponent_moves:
                # Game over, evaluate the final board
                return self._evaluate(board)
            # Otherwise, pass the turn
            return self._minimax(board, depth - 1, not is_maximizing)
        
        # Initialize the best score
        best_score = float('-inf') if is_maximizing else float('inf')
        
        # Try each move and get the best score
        for move in moves:
            new_board = copy.deepcopy(board)
            make_move(new_board, current_color, *move)
            
            score = self._minimax(new_board, depth - 1, not is_maximizing)
            
            if is_maximizing:
                best_score = max(best_score, score)
            else:
                best_score = min(best_score, score)
        
        return best_score
    
    def _evaluate(self, board):
        """
        Evaluate the board position for the agent.
        
        Args:
            board: The current game board
            
        Returns:
            A score representing how good the position is for the agent
        """
        # Basic evaluation: difference in piece count
        black_count, white_count = count_pieces(board)
        
        if self.color == 'B':
            return black_count - white_count
        else:
            return white_count - black_count
