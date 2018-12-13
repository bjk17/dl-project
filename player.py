import chess
import numpy as np
from interface import implements, Interface


class Player(Interface):
    def get_position_estimate(self, board):
        pass

    def get_next_move(self, board_position):
        pass


class ModelPlayer(implements(Player)):
    def __init__(self, nnmodel, exploration=0, random_seed=None):
        np.random.seed(random_seed)
        self.my_nn = nnmodel
        self.exploration = exploration

    def get_position_estimate(self, board):
        return self.my_nn.get_position_estimate(board)

    def get_next_move(self, board_position):
        board = chess.Board(board_position)

        moves = dict()
        for move in board.legal_moves:
            board.push(move)  # changes the board object
            moves[move] = self.get_position_estimate(board)
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


class TablebasePlayer(implements(Player)):
    def __init__(self, tablebases_path):
        self.tablebases_path = tablebases_path

    def _get_wdl_score(self, board):
        with chess.syzygy.open_tablebases(self.tablebases_path) as tablebase:
            # Returns 2 if the side to move is winning
            # Returns 0 if the position is a draw
            # Returns -2 if the side to move is losing
            # ( Returns 1 in case of a cursed win )
            # ( Returns -1 in case of a blessed loss )
            # ( Mate can be forced but the position can be drawn due to the fifty-move rule )
            return tablebase.probe_wdl(board)

    def _get_dtz_score(self, board):
        with chess.syzygy.open_tablebases(self.tablebases_path) as tablebase:
            # Returns a positive value if the side to move is winning
            # Returns 0 if the position is a draw
            # Returns a negative value if the side to move is losing
            return tablebase.probe_dtz(board)

    def get_position_estimate(self, board):
        wdl_score = self._get_wdl_score(board)
        if board.turn == chess.WHITE:
            return int(wdl_score / 2)
        else:
            return -int(wdl_score / 2)

    def get_next_move(self, board_position):
        board = chess.Board(board_position)

        moves = dict()
        for move in board.legal_moves:
            board.push(move)  # changes the board object
            moves[move] = (-self._get_wdl_score(board), self._get_dtz_score(board))
            board.pop()

        best_moves = sorted(moves.items(), key=lambda tup: (tup[1][0], tup[1][1]), reverse=True)
        return best_moves[0][0]
