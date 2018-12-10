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

    # Generating game
    while not game.is_game_over():
        if game.turn == chess.WHITE:
            next_move = white_player.get_next_move(game.fen())
        else:
            next_move = black_player.get_next_move(game.fen())

        game.push(next_move)

    result = game.result()
    signal = convert_result_string_to_value(result)
    target_signal = signal / 10
    weakening_factor = 0.9

    # because we will only be training on endgames that are
    # winning for White we will try this for the time being
    if result == "1/2-1/2":
        signal = 0.5
        target_signal = 0.1

    # Backtracking with learning signal
    fen_signal_list = []
    while len(game.move_stack) > 0:
        fen_signal_list.append("{},{}".format(game.fen(), signal))
        game.pop()
        signal = (signal - target_signal) * weakening_factor + target_signal

    # At last, add starting position with weak signal
    fen_signal_list.append("{},{}".format(game.fen(), signal))

    return convert_result_string_to_value(result), fen_signal_list


def simulate_games(nn_model, start_position, simulations, output_file, random_seed=None):
    # ThreadPoolExecutor() would result in race conditions to the np.random object
    # resulting in non-deterministic outputs between simulations for fixed random seed
    with concurrent.futures.ProcessPoolExecutor() as ppe:
        futures = list()
        for i in range(simulations):
            futures.append(
                ppe.submit(simulate_game_from_position, nn_model, start_position,
                           random_seed + i if random_seed else None))

    with open(output_file, 'w') as file:
        results = []
        for future in concurrent.futures.as_completed(futures):
            result, selfplay_training_data = future.result()
            results.append(result)
            for line in selfplay_training_data:
                file.write(line)
                file.write("\n")

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
    KQ_vs_K = "8/8/8/3k4/8/3KQ3/8/8 w - - 0 1"

    simulate_games(my_nn, KQ_vs_K, nr_of_simulations, output_games_file, random_seed)


if __name__ == '__main__':
    import sys

    args = sys.argv
    if len(args) <= 4:
        main(args[1], args[2], args[3])
    else:
        main(args[1], args[2], args[3], args[4])
