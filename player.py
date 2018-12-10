import chess
import numpy as np


class Player:
    def __init__(self, nnmodel, exploration=0, random_seed=None):
        np.random.seed(random_seed)
        self.my_nn = nnmodel
        self.exploration = exploration

    def get_next_move(self, board_position):
        board = chess.Board(board_position)

        moves = {
            move: self.my_nn.get_position_estimate(board) for move in board.legal_moves
        }

        random_number = np.random.rand()  # [0, 1)

        if random_number > self.exploration:
            best_moves = sorted(moves.items(), key=lambda x: x[1], reverse=True)
            return best_moves[0][0]
        else:
            move = np.random.choice(list(moves.keys()), 1)[0]
            return move
