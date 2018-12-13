import unittest
import os
import chess
from utils import convert_result_string_to_value
from nnmodel import NNModel
from player import ModelPlayer, TablebasePlayer


class ModelPlayerTest(unittest.TestCase):
    random_seed = 13

    dir = os.path.dirname(os.path.abspath(__file__))
    actual_model_path = os.path.abspath(os.path.join(dir, '..', 'models', 'v1.h5'))

    KQ_vs_K_white_checkmates_in_one = "k7/8/KQ6/8/8/8/8/8 w - - 0 1"
    board = chess.Board(KQ_vs_K_white_checkmates_in_one)

    random_nn = NNModel(random_seed=random_seed, model_path="something random")
    bad_nn = NNModel(random_seed=random_seed, model_path=actual_model_path)

    bad_player = ModelPlayer(random_nn, 1, random_seed)
    actual_player = ModelPlayer(bad_nn, 0, random_seed)

    def test_next_move_for_random(self):
        next_move = self.bad_player.get_next_move(self.KQ_vs_K_white_checkmates_in_one)
        self.assertIsNotNone(next_move)
        self.assertTrue(self.board.is_legal(next_move))

    def test_next_move_for_actual_model(self):
        next_move = self.actual_player.get_next_move(self.KQ_vs_K_white_checkmates_in_one)
        self.assertIsNotNone(next_move)
        self.assertTrue(self.board.is_legal(next_move))


class TablebasePlayerTest(unittest.TestCase):
    dir = os.path.dirname(os.path.abspath(__file__))
    tablebase_path = os.path.abspath(os.path.join(dir, '..', 'tablebases', 'syzygy', 'regular'))
    tablebase_player = TablebasePlayer(tablebase_path)

    KQ_vs_K_white_checkmates_in_one = "k7/8/KQ6/8/8/8/8/8 w - - 0 1"
    KQ_vs_K_starting_in_center = "8/8/8/3k4/8/3KQ3/8/8 w - - 0 1"
    KQ_vs_K_black_can_capture_queen = "8/7k/5K1Q/8/8/8/8/8 b - - 0 1"
    KQ_vs_K_black_can_avoid_immediate_checkmate = "3k4/7Q/2K5/8/8/8/8/8 b - - 0 1"

    def test_tablebase_white_mates_in_one(self):
        next_move = self.tablebase_player.get_next_move(self.KQ_vs_K_white_checkmates_in_one)
        self.assertIsNotNone(next_move)

        board = chess.Board(self.KQ_vs_K_white_checkmates_in_one)
        self.assertTrue(board.is_legal(next_move))

        board.push(next_move)
        self.assertTrue(board.is_game_over())

        result = convert_result_string_to_value(board.result())
        self.assertEqual(result, 1.0)

    def test_tablebase_white_picks_most_efficient_win(self):
        next_move = self.tablebase_player.get_next_move(self.KQ_vs_K_starting_in_center)
        self.assertIsNotNone(next_move)

        expected_move = chess.Move.from_uci("e3e7")
        self.assertEqual(expected_move, next_move)

    def test_tablebase_black_captures_queen(self):
        next_move = self.tablebase_player.get_next_move(self.KQ_vs_K_black_can_capture_queen)
        self.assertIsNotNone(next_move)

        expected_move = chess.Move.from_uci("h7h6")
        self.assertEqual(expected_move, next_move)

    def test_tablebase_black_picks_best_defence(self):
        next_move = self.tablebase_player.get_next_move(self.KQ_vs_K_black_can_avoid_immediate_checkmate)
        self.assertIsNotNone(next_move)

        expected_move = chess.Move.from_uci("d8e8")
        self.assertEqual(expected_move, next_move)


if __name__ == '__main__':
    unittest.main()
