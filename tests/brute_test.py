import sys
sys.path.insert(0,'.')
from chess import Chess as Chess
from board import Board as Board
import copy
import time
import datetime
import sys
import logging



def move_generation_test(depth, chess=Chess(Board())):
    """
    Brute force all possible games within a certain ply depth (ply = half-move) to check
    program correctness against the Shannon number table

    """
    if depth == 0:
        return 1
    chess.legal_moves = chess.get_legal_moves()
    counter = 0
    for move in chess.legal_moves:
        # Make move
        board = copy.deepcopy(chess.board)
        chess.play_move(move)

        counter += move_generation_test(depth-1, chess)

        # Undo move

        chess.board = board
    return counter



if len(sys.argv) == 1:
    depth = 5
else:
    depth = int(sys.argv[2])

now = datetime.datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")

logging.basicConfig(filename=f'tests/log/testBrute_{dt_string}.log', level=logging.INFO, format='%(asctime)s %(message)s')
logging.info(f"Initiating move generation test on depth: {depth}")

result_list = []

test_start = time.time()
ply_depth_start = time.time()

expected_results = [20,400,8902,197_281,4_865_609]

for current_depth, expected_result in zip(range(1,depth+1), expected_results):
    result = move_generation_test(current_depth)
    result_list.append(result)
    logging.info(f"Result of possible games with {current_depth} ply: {result}/{expected_result} - {'OK' if result == excepted_result else 'ERROR'}")

    ply_elapsed_time = (time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - ply_depth_start)))
    logging.info(f"Elapsed time in {i} ply: {ply_elapsed_time} seconds")
    ply_depth_start = time.time()

all_elapsed_time = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - test_start))

logging.info(f"Total Elapsed time: ({all_elapsed_time})")
