import unittest
import chess
from nnmodel import NNModel


class ProbabilityVector(unittest.TestCase):
    my_nn = NNModel()

    def test_starting_position(self):
        board_starting_position = chess.Board()
        mpv = self.my_nn.get_move_probabiliy_vector(board_starting_position)
        self.assertEqual(len(list(mpv)), 2 * 8 + 4)
        # self.assertEqual(sum(probability_vector.values()), 1.0)
        self.assertAlmostEqual(first=sum(mpv.values()), second=1.0, delta=0.01)


if __name__ == '__main__':
    unittest.main()
