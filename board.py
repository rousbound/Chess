import piece

class Board():
    """
    A class to represent a chess board.

    ...

    Attributes:
    -----------
    board : list[list[Piece]]
        represents a chess board
        
    turn : bool
        True if white's turn

    white_ghost_piece : tup
        The coordinates of a white ghost piece representing a takeable pawn for en passant

    black_ghost_piece : tup
        The coordinates of a black ghost piece representing a takeable pawn for en passant

    Methods:
    --------
    print_board() -> None
        Prints the current configuration of the board

    move(start:tup, to:tup) -> None
        Moves the piece at `start` to `to` if possible. Otherwise, does nothing.
        
    """
    def __init__(self):
        """
        Initializes the board per standard chess rules
        """

        self.board = []

        # Board set-up
        for i in range(8):
            self.board.append([None] * 8)
        # White
        self.board[0][7] = piece.Rook(True,0,7)
        self.board[1][7] = piece.Knight(True,1,7)
        self.board[2][7] = piece.Bishop(True,2,7)
        self.board[3][7] = piece.Queen(True,3,7)
        self.board[4][7] = piece.King(True,4,7)
        self.board[5][7] = piece.Bishop(True,5,7)
        self.board[6][7] = piece.Knight(True,6,7)
        self.board[7][7] = piece.Rook(True,7,7)

        for i in range(8):
            self.board[i][6] = piece.Pawn(True,i,6)

        # Black
        self.board[0][0] = piece.Rook(False,0,0)
        self.board[1][0] = piece.Knight(False,1,0)
        self.board[2][0] = piece.Bishop(False,2,0)
        self.board[3][0] = piece.Queen(False,3,0)
        self.board[4][0] = piece.King(False,4,0)
        self.board[5][0] = piece.Bishop(False,5,0)
        self.board[6][0] = piece.Knight(False,6,0)
        self.board[7][0] = piece.Rook(False,7,0)

        self.ghostPawn = None

        for i in range(8):
            self.board[i][1] = piece.Pawn(False,i,1)

        def __getitem__(self, item):
            return self.board[item]

    def vector(self):
        vec = []
        for i in range(8):
            for j in range(8):
                vec.append(self.board[i][j])
        return vec

    def print_board(self):
        """
        Prints the current state of the board.
        """

        s = "abcdefgh"
        buffer = ""
        for i in range(33):
            buffer += "*"
        print(buffer)
        # for i in range(len(self.board)):
            # tmp_str = "|"
            # for j in self.board[i][]:
                # if j == None or j.name == 'GP':
                    # tmp_str += "   |"
                # else:
                    # tmp_str += (" " + str(j) + " |")
            # print(tmp_str)
        for i in range(len(self.board)):
            tmp_str = f"{8-i}|"
            for j in range(len(self.board)):
                if self.board[j][i] == None:
                    tmp_str += "   |"
                else:
                    if self.board[j][i].color == True:
                        tmp_str += (" " + str(self.board[j][i]) + " |")
                    else:
                        tmp_str += (" " + str(self.board[j][i]).lower() + " |")

            print(tmp_str)
        buffer = " "
        for i in range(8):
            buffer += f"  {s[i]} "
        print(buffer)

        buffer = ""
        for i in range(33):
            buffer += "*"
        print(buffer)

    def getRooks(self, color):
        rooks = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j]:
                    if self.board[i][j].name == "R":
                        if self.board[i][j].color == color:
                            rooks.append(self.board[i][j])
        return rooks


    def getEnemyControlledSquares(self, color):
        enemyMoves = set()
        for otherpiece in self.vector():
            if otherpiece:
                if otherpiece.color != color:
                    if otherpiece.name != "K":
                        for move in otherpiece.get_valid_moves(self):
                            enemyMoves.add(move)
        return list(enemyMoves)

