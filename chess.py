import board
import piece

class Chess():
    """
    A class to represent the game of chess.
    
    ...

    Attributes:
    -----------
    board : Board
        represents the chess board of the game

    turn : bool
        True if white's turn

    white_ghost_piece : tup
        The coordinates of a white ghost piece representing a takeable pawn for en passant

    black_ghost_piece : tup
        The coordinates of a black ghost piece representing a takeable pawn for en passant

    Methods:
    --------
    promote(pos:stup) -> None
        Promotes a pawn that has reached the other side to another, or the same, piece

    move(start:tup, to:tup) -> None
        Moves the piece at `start` to `to` if possible. Otherwise, does nothing.
    """

    def __init__(self):
        self.board = board.Board()

        self.turn = True



    def move(self, start, to):
        """
        Moves a piece at `start` to `to`. Does nothing if there is no piece at the starting point.
        Does nothing if the piece at `start` belongs to the wrong color for the current turn.
        Does nothing if moving the piece from `start` to `to` is not a valid move.

        start : tup
            Position of a piece to be moved

        to : tup
            Position of where the piece is to be moved
        
        precondition: `start` and `to` are valid positions on the board
        """

        if self.board.board[start[0]][start[1]] == None:
            print("There is no piece to move at the start place")
            return

        target_piece = self.board.board[start[0]][start[1]]
        if self.turn != target_piece.color:
            print("That's not your piece to move")
            return

        end_piece = self.board.board[to[0]][to[1]]
        is_end_piece = end_piece != None

        # Checks if a player's own piece is at the `to` coordinate
        if is_end_piece and self.board.board[start[0]][start[1]].color == end_piece.color:
            print("There's a piece in the path.")
            return

        if target_piece.is_valid_move(self.board, to):
            print("is valid move")
            self.board.board[to[0]][to[1]] = target_piece
            self.board.board[start[0]][start[1]] = None
            self.turn = not self.turn


def translate(s):
    """
    Translates traditional board coordinates of chess into list indices
    """
    start = s[0:2]
    end = s[2:4]
    coords = [start,end]
    print(coords)
    r = []
    for coord in coords:
        try:
            row = int(coord[1])
            col = coord[0]
            if row < 1 or row > 8:
                print(coord[0] + "is not in the range from 1 - 8")
                return None
            if col < 'a' or col > 'h':
                print(coord[1] + "is not in the range from a - h")
                return None
            dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
            r.append((8 - row, dict[col]))
        except:
            print(s + "is not in the format '[number][letter]'")
            return None, None
    return r



if __name__ == "__main__":
    chess = Chess()
    chess.board.print_board()

    while True:
        move = input("Move: ")
        
        start, to = translate(move)
        print(start,to)

        if start == None or to == None:
            continue

        chess.move(start, to)

        # check for promotion pawns
        # i = 0
        # while i < 8:
            # if not chess.turn and chess.board.board[0][i] != None and \
                # chess.board.board[0][i].name == 'P':
                # chess.promotion((0, i))
                # break
            # elif chess.turn and chess.board.board[7][i] != None and \
                # chess.board.board[7][i].name == 'P':
                # chess.promotion((7, i))
                # break
            # i += 1

        chess.board.print_board()
