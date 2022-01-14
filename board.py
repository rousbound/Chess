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

    whiteGhostPawn : tup
        The coordinates of a white ghost piece representing a takeable pawn for en passant

    blackGhostPawn : tup
        The coordinates of a black ghost piece representing a takeable pawn for en passant

    Methods:
    --------
    print_board() -> None
        Prints the current configuration of the board

    getEnemyControlledSquares() -> list[tup]
        Returns coordinates of squares controlled by enemy pieces

    """
    def __init__(self):
        """
        Initializes the board per standard chess rules
        """

        self.board = []
        self.turn = True

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

        self.whiteGhostPawn = None
        self.blackGhostPawn = None

        for i in range(8):
            self.board[i][1] = piece.Pawn(False,i,1)


    def board2str(self):
        boardstr = ""
        getcolor = {True:"W", False:"B"}
        for i in range(8):
            for j in range(8):
                piece = self[i,j]
                if piece:
                    boardstr += getcolor[piece.color] + piece.name
                else:
                    boardstr += "%"
        return boardstr



    def __eq__(self, otherBoard):
        equal = True
        if self.board2str() != otherBoard.board2str():
            equal = False
        if self.turn != otherBoard.turn:
            equal = False
        return equal
    
    def __hash__(self):
        return hash(self.board2str())


    def __setitem__(self, key, value):
        self.board[key[0]][key[1]] = value
                    

    def __getitem__(self, item):
        return self.board[item[0]][item[1]]

    def getGhostPawn(self, color):
        if color:
            return self.whiteGhostPawn
        else:
            return self.blackGhostPawn

    def deactivateGhostPawn(self, color):
        if color:
            self.whiteGhostPawn = False
        else:
            self.blackGhostPawn = False

    def activateGhostPawn(self, pos, color):
        if color:
            self.whiteGhostPawn = (pos[0], pos[1] - 1)
        else:
            self.blackGhostPawn = (pos[0], pos[1] + 1)

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
        buffer += "\n"
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

            buffer += tmp_str + "\n"
        for i in range(8):
            buffer += f"   {s[i]}" 
        buffer += "\n"

        for i in range(33):
            buffer += "*" 
        buffer += "\n"
        return buffer

        

    def getRooks(self, color):
        rooks = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j]:
                    if self.board[i][j].name == "R":
                        if self.board[i][j].color == color:
                            rooks.append(self.board[i][j])
        return rooks

    def getKingPiece(self, color):
        for i in range(8):
            for j in range(8):
                if self.board[i][j]:
                    if self.board[i][j].name == "K":
                        if self.board[i][j].color == color:
                            return self.board[i][j]
        print("KING NOT FOUND")


    def getControlledSquares(self, color):
        enemyMoves = set()
        for otherpiece in self.vector():
            if otherpiece:
                if otherpiece.color == color:
                    if otherpiece.name != "K":
                        for move in otherpiece.get_valid_moves(self):
                            enemyMoves.add(move[1])
                    if otherpiece.name == "K":
                        for move in otherpiece.getNormalValidMoves(self):
                            enemyMoves.add(move[1])
        return list(enemyMoves)

