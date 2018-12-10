import chess
import numpy as np


def convert_result_string_to_value(result):
    return float(eval(result))


def convert_chess_board_to_nn_matrix(board):
    # (White, Black) x (Pawn, Knight, Bishop, Rook, Queen, King) x (a, ..., h) x (1, ..., 8)
    nn_matrix = np.zeros((2, 6, 8, 8), dtype=bool)

    # chess.WHITE = True
    # chess.BLACK = False
    for color in (chess.WHITE, chess.BLACK):
        color_index = 1 if color else 0

        # chess.PAWN = 1, ..., chess.KING = 6
        for piece in (chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING):
            piece_index = piece - 1

            for square in board.pieces(piece_type=piece, color=color):
                letter_index = chess.square_file(square)
                number_index = chess.square_rank(square)
                nn_matrix[color_index][piece_index][letter_index][number_index] = True

    return nn_matrix
