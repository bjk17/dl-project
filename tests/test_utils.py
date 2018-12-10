import unittest
import chess
import numpy as np
from utils import convert_chess_board_to_nn_matrix


class BoardToMatrixConversion(unittest.TestCase):
    winning_KQ_vs_K = "k7/8/KQ6/8/8/8/8/8 w - - 0 1"
    winning_board_position = chess.Board(winning_KQ_vs_K)

    def test_KQ_vs_K(self):
        expected_matrix = np.zeros((2, 6, 8, 8), dtype=bool)

        # Black King on a8
        expected_matrix[0][5][0][7] = True

        # White King on a6 and White Queen on b6
        expected_matrix[1][5][0][5] = True
        expected_matrix[1][4][1][5] = True

        generated_matrix = convert_chess_board_to_nn_matrix(self.winning_board_position)
        np.testing.assert_array_equal(generated_matrix, expected_matrix)


if __name__ == '__main__':
    unittest.main()
