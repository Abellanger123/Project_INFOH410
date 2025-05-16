from board import create_board, make_move, valid_moves, opponent, count_pieces
from random_ai import RandomAgent
from greedy_ai import GreedyAgent
from minimax_ai import MinimaxAgent
from mcts_ai import MCTSAgent

def play_game(agent_black, agent_white, verbose=False):
    board = create_board()
    current_agent = agent_black
    other_agent = agent_white

    current_color = "B"
    other_color = "W"

    no_move_passes = 0

    while True:
        moves = valid_moves(board, current_color)
        if not moves:
            no_move_passes += 1
            if no_move_passes == 2:
                break  # les deux passent → fin
            # sinon on passe le tour
            current_agent, other_agent = other_agent, current_agent
            current_color, other_color = other_color, current_color
            continue
        no_move_passes = 0

        move = current_agent.get_move(board)
        if move:
            make_move(board, current_color, *move)
        current_agent, other_agent = other_agent, current_agent
        current_color, other_color = other_color, current_color

    black_score, white_score = count_pieces(board)
    if verbose:
        print(f"Score final - Noir (B): {black_score}, Blanc (W): {white_score}")
    return black_score, white_score

def tournament(n_games=10):
    black_wins = 0
    white_wins = 0
    draws = 0

    for i in range(n_games):
        black = GreedyAgent("B")
        white = MCTSAgent("W", simulations=500)
        b_score, w_score = play_game(black, white)

        if b_score > w_score:
            black_wins += 1
        elif w_score > b_score:
            white_wins += 1
        else:
            draws += 1

    print(f"Sur {n_games} parties :")
    print(f"Greedy (Noir) gagne {black_wins} fois")
    print(f"MCTS (Blanc) gagne {white_wins} fois")
    print(f"Égalités : {draws}")

if __name__ == "__main__":
    tournament(n_games=10)
