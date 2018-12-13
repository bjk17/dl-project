import os
import chess
import concurrent.futures
from collections import Counter
from utils import convert_result_string_to_value
from nnmodel import NNModel
from player import ModelPlayer


def simulate_game_from_position(start_position, white_player, black_player, backtrack_with_learning_signal):
    # Generating game
    game = chess.Board(start_position)
    while not game.is_game_over():
        if game.turn == chess.WHITE:
            next_move = white_player.get_next_move(game.fen())
        else:
            next_move = black_player.get_next_move(game.fen())

        game.push(next_move)

    result = game.result()
    signal = convert_result_string_to_value(result)
    decay = 0.99

    # Backtracking with learning signal
    fen_signal_list = []
    if backtrack_with_learning_signal:
        while len(game.move_stack) > 0:
            if game.turn == chess.WHITE:
                fen_signal_list.append("{},{}".format(game.fen(), signal))
            else:
                fen_signal_list.append("{},{}".format(game.mirror().fen(), -signal))

            signal = signal * decay
            game.pop()

        # At last, add starting position with weak signal
        fen_signal_list.append("{},{}".format(game.fen(), signal))

    return convert_result_string_to_value(result), fen_signal_list


def simulate_games(start_position, simulations, nn_model_white, nn_model_black, exploration, output_file='/dev/null',
                   random_seed=None, multi_process=True):

    if output_file.startswith('/dev/null'):
        # save computation time
        backtrack_with_learning_signal = False
    else:
        backtrack_with_learning_signal = True

    # ThreadPoolExecutor() would result in race conditions to the np.random object
    # resulting in non-deterministic outputs between simulations for fixed random seed
    with concurrent.futures.ProcessPoolExecutor() as ppe:
        futures = list()
        for i in range(simulations):
            player_random_seed = random_seed + i if random_seed else None
            white_player = ModelPlayer(nn_model_white, exploration, player_random_seed)
            black_player = ModelPlayer(nn_model_black, exploration, player_random_seed)
            if multi_process:
                futures.append(ppe.submit(simulate_game_from_position, start_position, white_player, black_player,
                                          backtrack_with_learning_signal))
            else:
                futures.append(simulate_game_from_position(start_position, white_player, black_player,
                                                           backtrack_with_learning_signal))

    with open(output_file, 'w') as file:
        results = []
        thing_to_loop_over = concurrent.futures.as_completed(futures) if multi_process else futures
        for future in thing_to_loop_over:
            if multi_process:
                result, selfplay_training_data = future.result()
            else:
                result, selfplay_training_data = future
            results.append(result)
            for line in selfplay_training_data:
                file.write(line)
                file.write("\n")

    return results


def main(arg1, arg2, arg3, arg4, arg5, arg6=None):
    try:
        output_games_file = os.path.abspath(arg1)
        nr_of_simulations = int(arg2)
        white_model_path = os.path.abspath(arg3)
        black_model_path = os.path.abspath(arg4)
        exploration = float(arg5) if arg5 else None
        random_seed = int(arg6) if arg6 else None
    except ValueError as e:
        print("Second parameter (simulations) should be an integer and the fith (exploration) a float.")
        print(e)
        raise

    # hardcoded starting position
    KQ_vs_K = "8/8/8/3k4/8/3KQ3/8/8 w - - 0 1"

    white_model = NNModel(random_seed=random_seed, model_path=white_model_path)
    black_model = NNModel(random_seed=random_seed, model_path=black_model_path)

    print("White player: '{}'".format('random' if white_model.is_random() else white_model_path))
    print("Black player: '{}'".format('random' if black_model.is_random() else black_model_path))
    print("Simulating {} games with exploration '{}' and random_seed '{}' from position".format(nr_of_simulations,
                                                                                                exploration,
                                                                                                random_seed))
    print(chess.Board(KQ_vs_K))
    print()

    # Temporarily disabling multi-processing of game simulation because of an unknown bug
    multi_process = False
    results = simulate_games(KQ_vs_K, nr_of_simulations, white_model, black_model, exploration, output_games_file,
                             random_seed, multi_process)
    counter = Counter(results)

    print(" -> White wins: {}".format(counter[1]))
    print(" -> Draws: {}".format(counter[0]))
    print(" -> Black wins: {}".format(counter[-1]))


if __name__ == '__main__':
    import sys

    args = sys.argv
    if len(args) <= 6:
        main(args[1], args[2], args[3], args[4], args[5])
    else:
        main(args[1], args[2], args[3], args[4], args[5], args[6])
