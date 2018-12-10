import numpy as np


class NNModel:
    def __init__(self, random_seed):
        self.train()
        np.random.seed(random_seed)

    def train(self):
        pass

    def get_position_estimate(self, board):
        # Uniform random on (-1, 1) for untrained NN
        return 2 * np.random.random() - 1
