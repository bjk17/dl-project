import unittest
import os
import chess
import chess.syzygy
from collections import Counter
from nnmodel import NNModel
from player import ModelPlayer
from selfplay import main, simulate_game_from_position, simulate_games


class SelfPlayTest(unittest.TestCase):
    exploration = 0
    output_path = "/dev/null"
    KQ_vs_K_white_checkmates_in_one = "k7/8/KQ6/8/8/8/8/8 w - - 0 1"
    backtrack_with_learning_signal = True

    white_random_seed = 13
    black_random_seed = 42

    dir = os.path.dirname(os.path.abspath(__file__))
    nonsense_path = os.path.abspath(os.path.join(dir, '..', 'nonsense', 'path'))
    tablebase_path = os.path.abspath(os.path.join(dir, '..', 'tablebases', 'syzygy', 'regular'))

    white_nn = NNModel(random_seed=white_random_seed)
    black_nn = NNModel(random_seed=black_random_seed)
    white_player = ModelPlayer(white_nn, exploration, white_random_seed)
    black_player = ModelPlayer(black_nn, exploration, black_random_seed)

    def test_simulation_from_position(self):
        result, selfplay_training_data = simulate_game_from_position(
            self.KQ_vs_K_white_checkmates_in_one,
            self.white_player,
            self.black_player,
            self.backtrack_with_learning_signal
        )

        # beacuse of fixed random_seed
        # self.assertEqual(result, 0)
        # self.assertEqual(len(selfplay_training_data), 87)

    def test_one_game_simulation_with_tablebases(self):
        results = simulate_games(
            self.KQ_vs_K_white_checkmates_in_one,
            1,
            self.nonsense_path,
            self.tablebase_path,
            self.exploration,
            self.output_path,
            self.black_random_seed
        )

    def test_starting_positions(self):
        results = simulate_games(
            chess.STARTING_FEN,
            4,
            self.nonsense_path,
            self.nonsense_path,
            self.exploration,
            self.output_path,
            self.black_random_seed
        )

        # beacuse of fixed random_seed
        counter = Counter(results)
        self.assertEqual(len(results), 4)
        # self.assertEqual(counter[1], 0, "#White wins")
        # self.assertEqual(counter[0], 0, "#Draws")
        # self.assertEqual(counter[-1], 4, "#Black wins")


class ArgumentsTest(unittest.TestCase):
    arg1 = "/dev/null"  # output path to write training data
    arg2 = 10  # simulations
    arg3 = "path/to/model/v1"
    arg4 = "path/to/model/v2"
    arg5 = 0.50  # exploration

    def test_not_an_integer(self):
        not_an_integer = "!#$%&/()="
        self.assertRaises(ValueError, main, self.arg1, not_an_integer, self.arg3, self.arg4, self.arg5)

    def test_not_a_float(self):
        not_a_float = "!#$%&/()="
        self.assertRaises(ValueError, main, self.arg1, self.arg2, self.arg3, self.arg4, not_a_float)


if __name__ == '__main__':
    unittest.main()
