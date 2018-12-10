import chess
import numpy as np


class Player:
    def __init__(self, nnmodel, board_position, exploration=0, random_seed=None):
        np.random.seed(random_seed)
        self.my_nn = nnmodel
        self.exploration = exploration
        self.board = chess.Board(board_position)

    def return_next_move(self):
        moves = {
            move: self.my_nn.get_position_estimate(self.board) for move in self.board.legal_moves
        }

        random_number = np.random.rand()  # [0, 1)

        if random_number > self.exploration:
            best_moves = sorted(moves.items(), key=lambda x: x[1], reverse=True)
            return best_moves[0][0]
        else:
            return np.random.choice(moves, 1)[0]
