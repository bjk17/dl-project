import unittest
import chess
from collections import Counter
from nnmodel import NNModel
from selfplay import main, simulate_game_from_position, simulate_games


class SelfPlayTest(unittest.TestCase):
    random_seed = 13
    my_nn = NNModel(random_seed=13, model_path="eitthvad bull")
    winning_KQ_vs_K = "k7/8/KQ6/8/8/8/8/8 w - - 0 1"
    output_path = "/dev/null"  # output path to write training data

    def test_single_simulation(self):
        result, selfplay_training_data = simulate_game_from_position(self.my_nn, self.winning_KQ_vs_K,
                                                                     random_seed=self.random_seed)
        self.assertEqual(result, 0)
        self.assertEqual(len(selfplay_training_data), 2)

    def test_starting_positions(self):
        results = simulate_games(self.my_nn, chess.STARTING_FEN, 4, self.output_path, random_seed=42)
        c = Counter(results)
        self.assertEqual(c[1], 0)
        self.assertEqual(c[0], 3)
        self.assertEqual(c[-1], 1)


class ArgumentsTest(unittest.TestCase):
    arg1 = "/dev/null"  # output path to write training data
    arg2 = 10
    arg3 = "path/to/model/v3"

    def test_not_integer(self):
        not_an_integer = "!#$%&/()="
        self.assertRaises(ValueError, main, self.arg1, not_an_integer, self.arg3)


if __name__ == '__main__':
    unittest.main()
