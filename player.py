import chess
import numpy as np


class Player:
    def __init__(self, nnmodel, exploration=0, random_seed=None):
        np.random.seed(random_seed)
        self.my_nn = nnmodel
        self.exploration = exploration

    def get_next_move(self, board_position):
        board = chess.Board(board_position)

        moves = dict()
        for move in board.legal_moves:
            board.push(move)  # changes the board object
            moves[move] = self.my_nn.get_position_estimate(board)
            board.pop()

        random_number = np.random.random()  # [0, 1)
        if random_number >= self.exploration:
            # pick best move
            reverse_order = True if board.turn == chess.WHITE else False
            best_moves = sorted(moves.items(), key=lambda x: x[1], reverse=reverse_order)
            return best_moves[0][0]
        else:
            # pick random move
            move = np.random.choice(list(moves.keys()), 1)[0]
            return move
