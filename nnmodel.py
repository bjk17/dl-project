import os
import numpy as np
from utils import convert_chess_board_to_nn_matrix
from keras.models import load_model


class NNModel:
    def __init__(self, random_seed=None, model_path=None):
        np.random.seed(random_seed)
        self._load_model(model_path)

    def _load_model(self, model_path):
        if model_path is None or not os.path.isfile(model_path):
            self.model = None
            self.get_position_estimate = self._random_position_estimate
        else:
            self.model = load_model(model_path)

    def is_random(self):
        return self.model is None

    def get_position_estimate(self, board):
        nn_matrix = convert_chess_board_to_nn_matrix(board)
        model_input = np.array([nn_matrix.flatten(), ])
        return self.model.predict(model_input)[0][0]

    def _random_position_estimate(self, board):
        # Uniform random on (-1, 1) for untrained NN
        return 2 * np.random.random() - 1
