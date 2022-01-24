import sys
import logging

import board
import utils
import pieces
from chess import Chess


def play_cli(chess, get_move, input_list_test=None):
    """
    Play game with command line interface.

    """
    print(chess.board.print_board())
    while chess.game_running:
        chess.print_turn_decorator()
        chess.legal_moves = chess.get_legal_moves()

        if not chess.game_running:
            break
            
        if input_list:
            try:
                move = utils.uci_2_move(next(input_list_test))
            except:
                break
        else:
            move = get_move()

        if move not in chess.legal_moves:
            print("Illegal or impossible move")
            continue

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
    gui = GUI.GUI(640,640,chess)
    gui.main()

def play_gui_test(chess, argv):
    """
    Test game with command line interface

    """

    moves_list = argv[2:]
    print("Moves list:", moves_list)

    import GUI
    logging.basicConfig(filename='tests/log/guiLog.log', level=logging.DEBUG)
    gui = GUI.GUI(640,640,chess)
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
        elif arg == "-clitest":
            get_move = chess.get_move_list
        elif arg == "-r":
            get_move = chess.get_move_random

        play_cli(chess, get_move)

    if arg in ["-gui", None]:

        play_gui(chess)

    elif arg == "-guitest":

        play_gui_test(chess, args)

    elif arg == "-clitest":

        play_cli(chess, get_move)

if __name__ == "__main__":
    main(sys.argv)
