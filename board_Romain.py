def create_board():
    """Create a new Othello board with the initial setup."""
    # Create an 8x8 board filled with empty spaces
    board = [[' ' for _ in range(8)] for _ in range(8)]
    
    # Set up the initial four pieces in the center
    board[3][3] = 'W'
    board[3][4] = 'B'
    board[4][3] = 'B'
    board[4][4] = 'W'
    
    return board

def print_board(board):
    """Print the current state of the board."""
    print("  0 1 2 3 4 5 6 7")
    for i, row in enumerate(board):
        print(f"{i} {' '.join(row)}")
    print()

def count_pieces(board):
    """Count the number of pieces for each player."""
    black_count = sum(row.count('B') for row in board)
    white_count = sum(row.count('W') for row in board)
    return black_count, white_count

def opponent(color):
    """Return the opponent's color."""
    return 'W' if color == 'B' else 'B'

def valid_moves(board, color):
    """Find all valid moves for the given player."""
    moves = []
    
    for row in range(8):
        for col in range(8):
            if is_valid_move(board, color, row, col):
                moves.append((row, col))
                
    return moves

def is_valid_move(board, color, row, col):
    """Check if placing a piece at the given position is valid."""
    # Check if the cell is empty
    if board[row][col] != ' ':
        return False
    
    # Directions to check (all 8 directions)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    # The opponent's color
    other_color = opponent(color)
    
    # Check each direction
    valid = False
    for dr, dc in directions:
        r, c = row + dr, col + dc
        
        # Check if we have at least one opponent's piece in this direction
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == other_color:
            r += dr
            c += dc
            
            # Keep going in this direction
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == ' ':
                    # Empty cell, not valid in this direction
                    break
                if board[r][c] == color:
                    # Found our own color, valid move
                    valid = True
                    break
                
                # Keep going
                r += dr
                c += dc
                
    return valid

def make_move(board, color, row, col):
    """Place a piece on the board and flip the opponent's pieces."""
    if not is_valid_move(board, color, row, col):
        return False
    
    # Directions to check
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    # The opponent's color
    other_color = opponent(color)
    
    # Place the piece
    board[row][col] = color
    
    # Check each direction and flip pieces
    for dr, dc in directions:
        pieces_to_flip = []
        r, c = row + dr, col + dc
        
        # Collect pieces to flip in this direction
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == other_color:
            pieces_to_flip.append((r, c))
            r += dr
            c += dc
            
        # If we found a valid line ending with our color, flip the pieces
        if pieces_to_flip and 0 <= r < 8 and 0 <= c < 8 and board[r][c] == color:
            for flip_r, flip_c in pieces_to_flip:
                board[flip_r][flip_c] = color
    
    return True
