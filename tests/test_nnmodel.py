import unittest
import chess
from nnmodel import NNModel


class NNModelTest(unittest.TestCase):
    random_seed = 13
    my_nn = NNModel(random_seed)

    def test_if_uniform_random(self):
        board_starting_position = chess.Board()
        position_estimate = self.my_nn.get_position_estimate(board_starting_position)
        self.assertTrue(-1.0 <= position_estimate <= 1.0)


if __name__ == '__main__':
    unittest.main()
