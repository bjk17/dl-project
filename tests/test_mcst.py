import unittest
import chess
from mcst import MCST, convert_result_string_to_value
from nnmodel import NNModel


class ResultStringValueConversion(unittest.TestCase):
    def test_white_wins(self):
        result = "1-0"
        result_value = convert_result_string_to_value(result)
        self.assertEqual(1.0, result_value)

    def test_draw(self):
        result = "1/2-1/2"
        result_value = convert_result_string_to_value(result)
        self.assertEqual(0.5, result_value)

    def test_black_wins(self):
        result = "0-1"
        result_value = convert_result_string_to_value(result)
        self.assertEqual(0.0, result_value)


class MonteCarloSearchTree(unittest.TestCase):
    my_nn = NNModel()
    winning_KQ_vs_K = "k7/8/KQ6/8/8/8/8/8 w - - 0 1"
    winning_board_position = chess.Board(winning_KQ_vs_K)
    my_mcst = MCST(nnmodel=my_nn, board_position=winning_board_position, simulations=10)

    def test_evaluation(self):
        winning_position_estimate = self.my_mcst.get_position_estimate()
        self.assertGreaterEqual(winning_position_estimate, 0.5)
        self.assertLessEqual(winning_position_estimate, 1.0)

    def test_starting_position(self):
        result = self.my_mcst.simulate_game_from_position(chess.Board())
        self.assertIn(result, [1.0, 0.5])


if __name__ == '__main__':
    unittest.main()
