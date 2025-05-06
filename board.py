EMPTY, BLACK, WHITE = ".", "B", "W"
BOARD_SIZE = 8
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),         (0, 1),
              (1, -1), (1, 0), (1, 1)]

def create_board():
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    board[3][3], board[4][4] = WHITE, WHITE
    board[3][4], board[4][3] = BLACK, BLACK
    return board

def opponent(player):
    return BLACK if player == WHITE else WHITE

def on_board(x, y):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

def is_valid_move(board, player, x, y):
    if board[x][y] != EMPTY:
        return False
    opp = opponent(player)
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        has_opponent = False
        while on_board(nx, ny) and board[nx][ny] == opp:
            nx += dx
            ny += dy
            has_opponent = True
        if has_opponent and on_board(nx, ny) and board[nx][ny] == player:
            return True
    return False

def valid_moves(board, player):
    return [(x, y) for x in range(BOARD_SIZE)
                   for y in range(BOARD_SIZE)
                   if is_valid_move(board, player, x, y)]

def make_move(board, player, x, y):
    board[x][y] = player
    opp = opponent(player)
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        to_flip = []
        while on_board(nx, ny) and board[nx][ny] == opp:
            to_flip.append((nx, ny))
            nx += dx
            ny += dy
        if on_board(nx, ny) and board[nx][ny] == player:
            for fx, fy in to_flip:
                board[fx][fy] = player

def count_pieces(board):
    b = sum(row.count(BLACK) for row in board)
    w = sum(row.count(WHITE) for row in board)
    return b, w
