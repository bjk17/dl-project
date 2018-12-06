import copy
import numpy as np
import concurrent.futures


def convert_result_string_to_value(result):
    return float(eval(result)) / 2 + 0.5


class MCST:
    def __init__(self, nnmodel, board_position, simulations=1, random_seed=None):
        np.random.seed(random_seed)
        self.my_nn = nnmodel
        self.board = board_position
        self.simulations = simulations
        self.evaluation = self.simulate_games()

    def get_position_estimate(self):
        return self.evaluation

    def simulate_game_from_position(self, position, random_seed=None):
        if random_seed:
            np.random.seed(random_seed)

        board = copy.deepcopy(position)
        while not board.is_game_over():
            mpv = self.my_nn.get_move_probabiliy_vector(board)
            move = np.random.choice(list(mpv.keys()), 1, replace=False, p=list(mpv.values()))[0]
            board.push(move)

        result = board.result()
        return convert_result_string_to_value(result)

    def simulate_games(self):
        # ThreadPoolExecutor() would result in race conditions to the np.random object
        # resulting in non-deterministic outputs between simulations for fixed random seed
        with concurrent.futures.ProcessPoolExecutor() as ppe:
            futures = list()
            for i in range(self.simulations):
                futures.append(ppe.submit(self.simulate_game_from_position, self.board, random_seed=i))

            return np.mean([future.result() for future in concurrent.futures.as_completed(futures)])
