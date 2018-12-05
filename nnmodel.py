class NNModel:
    def __init__(self):
        self.train()

    def train(self):
        pass

    def get_move_probabiliy_vector(self, board):
        # Uniform random for untrained NN
        legal_moves = board.legal_moves
        nr_of_moves = len(list(legal_moves))
        return {move: 1.0 / nr_of_moves for move in legal_moves}
