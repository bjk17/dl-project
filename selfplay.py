import os
import chess
import concurrent.futures
from utils import convert_result_string_to_value
from nnmodel import NNModel
from player import Player


def simulate_game_from_position(nn_model, start_position, random_seed=None):
    white_player = Player(nn_model, exploration=1, random_seed=random_seed)
    black_player = Player(nn_model, exploration=1, random_seed=random_seed)

    game = chess.Board(start_position)
    while not game.is_game_over():
        if game.turn == chess.WHITE:
            next_move = white_player.get_next_move(game.fen())
        else:
            next_move = black_player.get_next_move(game.fen())

        game.push(next_move)

    return game


def simulate_games(nn_model, start_position, simulations=1, random_seed=None):
    # ThreadPoolExecutor() would result in race conditions to the np.random object
    # resulting in non-deterministic outputs between simulations for fixed random seed
    with concurrent.futures.ProcessPoolExecutor() as ppe:
        futures = list()
        for i in range(simulations):
            futures.append(
                ppe.submit(simulate_game_from_position, nn_model, start_position, random_seed=random_seed + i))

        results = []
        for future in concurrent.futures.as_completed(futures):
            game = future.result()
            result = convert_result_string_to_value(game.result())
            results.append(result)

        return results


def main(arg1, arg2, arg3, arg4=None):
    try:
        output_games_file = os.path.abspath(arg1)
        nr_of_simulations = int(arg2)
        nn_model_path = os.path.abspath(arg3)
        random_seed = int(arg4) if arg4 else None
    except ValueError as e:
        print("Second parameter should be an integer.")
        print(e)
        raise

    my_nn = NNModel(random_seed=random_seed, model_path=nn_model_path)

    # Simulate games now


if __name__ == '__main__':
    import sys

    args = sys.argv
    main(args[1], args[2], args[3], arg[4])
