import sys
sys.path.insert(0,'.')
from chess import Chess as Chess
from board import Board as Board
import copy
import time
import datetime
import sys
import logging



def move_generation_test(depth, chess):
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
        FEN = board.board_2_FEN()
        # print(FEN)

        counter += move_generation_test(depth-1, chess)

        # Undo move

        chess.board = board
    return counter



if len(sys.argv) == 1:
    depth = 5
else:
    depth = int(sys.argv[2])



def test_position(depth, expected_results, FEN=None):
    now = datetime.datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")

    logging.basicConfig(filename=f'tests/log/testBrute_{dt_string}.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info(f"----------------------------------------")
    logging.info(f"Initiating move generation test on depth: {depth}")

    result_list = []

    test_start = time.time()
    ply_depth_start = time.time()
    for current_depth, expected_result in zip(range(1,depth+1), expected_results):
        chess = Chess(Board(FEN=FEN))
        result = move_generation_test(current_depth, chess)
        result_list.append(result)
        logging.info(f"Result of possible games with {current_depth} ply: {result}/{expected_result} - {'OK' if result == expected_result else 'ERROR'}")

        ply_elapsed_time = (time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - ply_depth_start)))
        logging.info(f"Elapsed time in {current_depth} ply: {ply_elapsed_time} seconds")
        ply_depth_start = time.time()

    all_elapsed_time = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - test_start))

    logging.info(f"Total Elapsed time: ({all_elapsed_time})")
    logging.info(f"-----------------------------------------")


test_position(5, [20,400,8902,197_281,4_865_609])
test_position(2, [48, 2039, 97862, 4085603], FEN = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 0")
test_position(3, [14, 191, 2812, 43238], FEN = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 0")
test_position(3, [6, 264 , 9467, 422333], FEN = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1")
test_position(3, [44, 1486 , 62379, 2103487], FEN = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8")
test_position(3, [46 , 2079, 89890], FEN = "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10")
