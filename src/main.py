import sys

from mychess import Chess


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
        chess.play_cli(chess.get_move_player)

    if arg == "-clir":
        chess = Chess(print_turn_decorator=False)
        chess.play_cli(chess.get_move_random)

    if arg in ["-gui", None]:

        chess = Chess(print_turn_decorator=False)
        chess.play_gui()

if __name__ == "__main__":
    main(sys.argv)
