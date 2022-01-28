"""
Test which brute forces certain complex positions, compares with a proof table, and also 
prints games which differ from python-chess, a more mature chess library.
This way we can debug positions that have errors in them.

"""

import copy
import time
import datetime
import sys
import logging
import os
import chess as debug_chess

from mychess import Chess


os.chdir("tests")

now = datetime.datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")
logging.basicConfig(filename=f'log/test_brute_{dt_string}.log',
        level=logging.INFO,
        format='%(asctime)s %(message)s',
        datefmt='%H:%M:%S',)


def move_generation_test(depth, chess, original_fen):
    """
    Brute force all possible games within a certain ply depth (ply = half-move) to check
    program correctness against a proof table

    """
    if depth == 0:
        return 1
    chess.legal_moves = chess.get_legal_moves()
    counter = 0
    for move in chess.legal_moves:
        # Make move
        board = copy.deepcopy(chess.board)
        chess.play_move(move)

        # Compare with a more mature library result
        debug_board = debug_chess.Board(original_fen)
        for saved_move in chess.board.uci_moves_list:
            try:
                debug_board.push_uci(saved_move)
            except:
                # Save information need to debug wrong position
                fen = chess.board.board_2_fen()
                logging.info(fen)
                logging.info(debug_board.fen())
                logging.info(chess.board.uci_moves_list)

        counter += move_generation_test(depth-1, chess, original_fen)

        # Undo move

        chess.board = board
    return counter


def brute_force_position(depth, expected_results, fen):
    logging.info("----------------------------------------")
    logging.info(f"Initiating move generation test on depth: {depth}")
    if fen:
        logging.info(f"FEN of position to be brute forced:{fen}")

    result_list = []

    test_start = time.time()
    ply_depth_start = time.time()

    for current_depth, expected_result in zip(range(1,depth+1), expected_results):
        game = Chess(fen=fen, print_turn_decorator=False)
        result = move_generation_test(current_depth, game, fen)
        result_list.append(result)
        str_result = 'OK' if result == expected_result else 'ERROR'

        logging.info(f"Result of possible games with {current_depth} ply: {result}/{expected_result} - {str_result} ")

        ply_elapsed_time = (time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - ply_depth_start)))

        logging.info(f"Elapsed time in {current_depth} ply: {ply_elapsed_time} seconds")

        ply_depth_start = time.time()

    all_elapsed_time = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - test_start))

    logging.info(f"Total Elapsed time: ({all_elapsed_time})")

    return result_list[:depth]

def test_initial_position():
    depth = 3
    expected_results = [20,400,8_902,197_281,4_865_609]
    fen =  "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0"
    assert brute_force_position(depth,
                                expected_results,
                                fen = fen) == expected_results[:depth]

def test_position_1():
    depth = 3
    expected_results = [48, 2_039, 97_862, 4_085_603]
    fen = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 0"
    assert brute_force_position(depth,
                                expected_results,
                                fen = fen) == expected_results[:depth]

def test_position_2():
    depth = 4
    expected_results = [14, 191, 2_812, 43_238]
    fen =  "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 0"
    assert brute_force_position(depth,
                                expected_results,
                                fen = fen) == expected_results[:depth]

def test_position_3():
    depth = 4
    expected_results = [6, 264 , 9_467, 422_333]
    fen = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"
    assert brute_force_position(depth,
                                expected_results,
                                fen = fen) == expected_results[:depth]

def test_position_4():
    depth = 4
    expected_results = [44, 1_486 , 62_379, 2_103_487]
    fen = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8"
    assert brute_force_position(depth,
                                expected_results,
                                fen = fen) == expected_results[:depth]

def test_position_5(): 
    depth = 3
    expected_results = [46 , 2_079, 89_890]
    fen = "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10"
    assert brute_force_position(depth,
                                expected_results,
                                fen = fen) == expected_results[:depth]
