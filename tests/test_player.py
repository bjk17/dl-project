import unittest
import chess
from player import Player
from nnmodel import NNModel


class PlayerTest(unittest.TestCase):
    random_seed = 13
    steady_exploration = 0
    my_nn = NNModel(random_seed)
    winning_KQ_vs_K = "k7/8/KQ6/8/8/8/8/8 w - - 0 1"
    winning_board_position = chess.Board(winning_KQ_vs_K)
    steady_player = Player(my_nn, winning_KQ_vs_K, steady_exploration, random_seed)

    def test_next_move(self):
        next_move = self.steady_player.return_next_move()
        self.assertIsNotNone(next_move)
        self.assertTrue(self.winning_board_position.is_legal(next_move))


if __name__ == '__main__':
    unittest.main()
