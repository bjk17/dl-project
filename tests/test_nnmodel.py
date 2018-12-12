import unittest
import os
import chess
from nnmodel import NNModel


class NNModelTest(unittest.TestCase):
    random_seed = 13
    board_starting_position = chess.Board()

    def test_random_model(self):
        model_random = NNModel(self.random_seed)
        self.assertTrue(model_random.is_random())
        position_estimate = model_random.get_position_estimate(self.board_starting_position)
        self.assertTrue(-1.0 <= position_estimate <= 1.0)

    def test_shitty_model(self):
        model_shitty_path = NNModel(self.random_seed, "shitty path")
        self.assertTrue(model_shitty_path.is_random())

    def test_v1_model(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.abspath(os.path.join(dir, '..', 'models', 'a_pretty_bad_one.h5'))
        model_v1 = NNModel(self.random_seed, model_path)
        self.assertFalse(model_v1.is_random())
        position_estimate = model_v1.get_position_estimate(self.board_starting_position)
        self.assertTrue(-1.0 <= position_estimate <= 1.0)


if __name__ == '__main__':
    unittest.main()
