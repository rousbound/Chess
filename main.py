import sys
import logging

import board
import utils
import pieces
from chess import Chess


def play_cli(chess, get_move):
    """
    Play game with command line interface.

    """
    print(chess.board.print_board())
    while chess.game_running:
        chess.print_turn_decorator()
        chess.legal_moves = chess.get_legal_moves()
        if not chess.game_running:
            break
        move = get_move()

        if move not in chess.legal_moves:
            print("Illegal or impossible move")
            continue

        chess.turn_debug()
        chess.play_move(move)
        print(chess.board.print_board())


def play_cli_test(chess, input_moves):
    """
    Test game with list of moves as input.

    """
    print("Input moves:", input_moves)
    for move in input_moves:
        move = utils.uci_2_move(move)
        chess.print_turn_decorator()
        chess.legal_moves = chess.get_legal_moves()
        if move not in chess.legal_moves:
            print("Illegal or impossible move")
            break
        if not chess.game_running:
            break
        chess.turn_debug()
        chess.play_move(move)
        print(chess.board.print_board())
    return chess.board.board_2_FEN()


def play_gui(chess):
    """
    Play game with Graphical User Interface.

    """
    import GUI
    logging.basicConfig(filename='tests/log/guiLog.log', level=logging.DEBUG)
    gui = GUI.GUI(chess.board,640,640,chess)
    gui.main()

def play_gui_test(chess, argv):
    """
    Test game with command line interface

    """

    moves_list = argv[2:]
    print("Moves list:", moves_list)

    import GUI
    logging.basicConfig(filename='tests/log/guiLog.log', level=logging.DEBUG)
    gui = GUI.GUI(chess.board,640,640,chess)
    gui.cli_gui_main(moves_list)



def main(args):
    """
    Main function.

    """
    chess = Chess(board.Board())

    if len(args) == 1:

        arg = None
    else:

        arg = args[1]

    if arg in ["-cli", "-r"]:

        if arg == "-cli":
            get_move = chess.get_move_player
        elif arg == "-r":
            get_move = chess.get_move_random

        chess.play_cli(chess, get_move)

    if arg in ["-gui", None]:

        play_gui(chess)

    elif arg == "-guitest":

        play_gui_test(chess, args)

    elif arg == "-clitest":

        play_cli_test(chess, args[2:])

if __name__ == "__main__":
    main(sys.argv)
