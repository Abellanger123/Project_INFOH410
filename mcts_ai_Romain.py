from board import valid_moves, make_move, count_pieces
import copy
import random
import math

class MCTSNode:
    def __init__(self, board, color, parent=None, move=None):
        """
        Initialize a node in the Monte Carlo search tree.
        
        Args:
            board: The board state at this node
            color: The player's color at this node ('B' or 'W')
            parent: The parent node
            move: The move that led to this node
        """
        self.board = board
        self.color = color
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0
        self.unexplored_moves = valid_moves(board, color)
        
    def fully_expanded(self):
        """Check if all possible moves from this state have been explored."""
        return len(self.unexplored_moves) == 0
    
    def select_child(self):
        """Select a child node using the UCB1 formula."""
        # UCB1 formula: wins/visits + C * sqrt(ln(parent_visits) / visits)
        C = 1.41  # Exploration parameter
        
        best_score = float('-inf')
        best_child = None
        
        for child in self.children:
            # Avoid division by zero
            if child.visits == 0:
                return child
                
            exploitation = child.wins / child.visits
            exploration = math.sqrt(math.log(self.visits) / child.visits)
            score = exploitation + C * exploration
            
            if score > best_score:
                best_score = score
                best_child = child
                
        return best_child
    
    def expand(self):
        """Expand the tree by adding a new child node."""
        if not self.unexplored_moves:
            return None
            
        # Choose a random unexplored move
        move = random.choice(self.unexplored_moves)
        self.unexplored_moves.remove(move)
        
        # Create a new board with this move
        new_board = copy.deepcopy(self.board)
        opponent_color = 'W' if self.color == 'B' else 'B'
        make_move(new_board, self.color, *move)
        
        # Create and return the new child node
        child = MCTSNode(new_board, opponent_color, parent=self, move=move)
        self.children.append(child)
        return child
    
    def update(self, result):
        """Update the node statistics based on simulation result."""
        self.visits += 1
        self.wins += result


class MCTSAgentRomain:
    def __init__(self, color, iterations=1000):
        """
        Initialize the Monte Carlo Tree Search agent.
        
        Args:
            color: The color that the agent is playing ('B' or 'W')
            iterations: The number of iterations to run MCTS
        """
        self.color = color
        self.opponent_color = 'W' if color == 'B' else 'B'
        self.iterations = iterations
    
    def get_move(self, board):
        """
        Get the best move according to MCTS.
        
        Args:
            board: The current game board
            
        Returns:
            The best move as a tuple (row, col) or None if no moves are available
        """
        moves = valid_moves(board, self.color)
        if not moves:
            return None
        
        # Create the root node
        root = MCTSNode(copy.deepcopy(board), self.color)
        
        # Run MCTS for the specified number of iterations
        for _ in range(self.iterations):
            # Selection
            node = root
            while not node.fully_expanded() and node.children:
                node = node.select_child()
            
            # Expansion
            if not node.fully_expanded():
                node = node.expand()
                if node is None:  # No moves to expand
                    continue
            
            # Simulation
            result = self._simulate(node.board, node.color)
            
            # Backpropagation
            while node is not None:
                node.update(result if node.color == self.opponent_color else 1 - result)
                node = node.parent
        
        # Choose the move with the highest visit count
        best_visits = -1
        best_move = moves[0]  # Default to first move
        
        for child in root.children:
            if child.visits > best_visits:
                best_visits = child.visits
                best_move = child.move
        
        return best_move
    
    def _simulate(self, board, color):
        """
        Simulate a random game from the current board state.
        
        Args:
            board: The current game board
            color: The color to move next ('B' or 'W')
            
        Returns:
            1 if the agent wins, 0 if it loses, 0.5 for a draw
        """
        board_copy = copy.deepcopy(board)
        current_color = color
        
        # Play until the game is over
        no_move_count = 0
        while no_move_count < 2:  # Game ends when both players pass
            moves = valid_moves(board_copy, current_color)
            
            if not moves:
                no_move_count += 1
            else:
                no_move_count = 0
                # Make a random move
                move = random.choice(moves)
                make_move(board_copy, current_color, *move)
            
            # Switch player
            current_color = 'W' if current_color == 'B' else 'B'
        
        # Count pieces to determine the winner
        black_count, white_count = count_pieces(board_copy)
        
        if self.color == 'B':
            if black_count > white_count:
                return 1  # Win
            elif black_count < white_count:
                return 0  # Loss
            else:
                return 0.5  # Draw
        else:  # Agent is white
            if white_count > black_count:
                return 1  # Win
            elif white_count < black_count:
                return 0  # Loss
            else:
                return 0.5  # Draw
