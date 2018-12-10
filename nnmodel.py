import os
import numpy as np


class NNModel:
    def __init__(self, random_seed=None, model_path=None):
        np.random.seed(random_seed)
        self.model_path = os.path.abspath(model_path) if model_path else None
        self.load_model()
        self.train()

    def load_model(self):
        if self.model_path is None or not os.path.isfile(self.model_path):
            self.get_position_estimate = self.random_position_estimate
        else:
            pass

    def train(self):
        pass

    def get_position_estimate(self, board):
        return None

    def random_position_estimate(self, board):
        # Uniform random on (-1, 1) for untrained NN
        return 2 * np.random.random() - 1
