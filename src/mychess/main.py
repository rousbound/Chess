"""
main.py -- Execution options
Author: Geraldo Luiz Pereira
www.github.com/rousbound
"""
import sys

from mychess import Chess


def main(args):
    """
    Main function. Receives as argument the type of execution

    """

    if len(args) == 1:
        arg = None
    else:
        arg = args[1]

    chess = Chess(print_turn_decorator=False)
    if arg == "-cli":

        chess.play_cli(chess.get_move_player)

    if arg == "-clir":
        chess.play_cli(chess.get_move_random)

    if arg in ["-gui", None]:

        chess.play_gui()

if __name__ == "__main__":
    main(sys.argv)
