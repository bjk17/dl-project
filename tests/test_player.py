import unittest
import os
import chess
from player import Player
from nnmodel import NNModel


class PlayerTest(unittest.TestCase):
    random_seed = 13

    dir = os.path.dirname(os.path.abspath(__file__))
    actual_model_path = os.path.abspath(os.path.join(dir, '..', 'models', 'v1.h5'))

    winning_KQ_vs_K = "k7/8/KQ6/8/8/8/8/8 w - - 0 1"
    black_to_move = "rnbqkb1r/pp2pp1p/3p1np1/8/3NP3/2N5/PPP1BPPP/R1BQK2R b KQkq - 1 6"

    random_nn = NNModel(random_seed=random_seed, model_path="something random")
    bad_nn = NNModel(random_seed=random_seed, model_path=actual_model_path)

    bad_player = Player(random_nn, 1, random_seed)
    actual_player = Player(bad_nn, 0, random_seed)

    board = chess.Board(winning_KQ_vs_K)

    def test_next_move_for_random(self):
        next_move = self.bad_player.get_next_move(self.winning_KQ_vs_K)
        self.assertIsNotNone(next_move)
        self.assertTrue(self.board.is_legal(next_move))

    def test_next_move_for_actual_model(self):
        next_move = self.actual_player.get_next_move(self.winning_KQ_vs_K)
        self.assertIsNotNone(next_move)
        self.assertTrue(self.board.is_legal(next_move))


if __name__ == '__main__':
    unittest.main()
