import sys
import logging

from chess import *


def main(args):
    """
    Main function.

    """

    if len(args) == 1:
        arg = None
    else:
        arg = args[1]

    if arg == "-cli":

        chess = Chess(print_turn_decorator=False)
        chess.play_cli()

    if arg in ["-gui", None]:

        chess = Chess(print_turn_decorator=False)
        chess.play_gui()

if __name__ == "__main__":
    main(sys.argv)
