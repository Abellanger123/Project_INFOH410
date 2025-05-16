import copy
import math
import random
from board import valid_moves, make_move, opponent, count_pieces

class Node:
    def __init__(self, state, parent=None, move=None, player=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.wins = 0
        self.visits = 0
        self.children = []
        self.untried_moves = valid_moves(state, player if player else "B")
        self.player = player  # Stocke le joueur associé au nœud


    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self, exploration=1.41):
        best_score = float("-inf")
        best_child = None

        for child in self.children:
            exploitation = child.wins / child.visits
            exploration_term = exploration * math.sqrt(math.log(self.visits) / child.visits)
            ucb1 = exploitation + exploration_term

            if ucb1 > best_score:
                best_score = ucb1
                best_child = child

        return best_child

    def expand(self):
        move = self.untried_moves.pop(0)
        new_state = copy.deepcopy(self.state)

        # Déterminer le joueur actif
        player = opponent(self.player) if self.move else self.player

        # Appliquer le coup
        make_move(new_state, player, move[0], move[1])

        # Créer le nœud enfant avec le joueur suivant
        child_node = Node(new_state, parent=self, move=(move[0], move[1], player), player=player)
        self.children.append(child_node)
        return child_node


    def update(self, result):
        self.visits += 1
        self.wins += result

class MCTSAgent:
    def __init__(self, color, simulations=100):
        self.color = color
        self.simulations = simulations

    def get_move(self, board):
        root = Node(copy.deepcopy(board), player=self.color)

        for _ in range(self.simulations):
            node = root

            # SELECTION
            while node.is_fully_expanded() and node.children:
                node = node.best_child()

            # EXPANSION
            if not node.is_fully_expanded():
                node = node.expand()

            # SIMULATION
            result = self.simulate(node)

            # BACKPROPAGATION
            while node:
                node.update(result)
                node = node.parent

        # Meilleur coup choisi
        best_child = max(root.children, key=lambda c: c.visits)
        return (best_child.move[0], best_child.move[1])


    def simulate(self, node):
        board = copy.deepcopy(node.state)
        current_player = self.color if node.move is None else opponent(node.move[1])

        while valid_moves(board, current_player):
            moves = valid_moves(board, current_player)
            move = random.choice(moves)
            make_move(board, current_player, *move)
            current_player = opponent(current_player)

        black_score, white_score = count_pieces(board)
        if self.color == "B":
            return 1 if black_score > white_score else 0
        else:
            return 1 if white_score > black_score else 0
