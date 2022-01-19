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

    white_ghost_pawn : tup
        The coordinates of a white ghost piece representing a takeable pawn for en passant

    black_ghost_pawn : tup
        The coordinates of a black ghost piece representing a takeable pawn for en passant

    Methods:
    --------
    print_board() -> None
        Prints the current configuration of the board

    get_controlled_squares(color : bool) -> list[tup]
        Returns coordinates of squares controlled by chosen color

    """
    def __init__(self):
        """
        Initializes the board per standard chess rules
        """

        self.board = []
        self.turn = True
        self.moves_list = []
        self.algebric_legal_moves = []

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

        self.white_ghost_pawn = None
        self.black_ghost_pawn = None

        for i in range(8):
            self.board[i][1] = piece.Pawn(False,i,1)


    def board_2_str(self):
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



    def __eq__(self, other_board):
        """
        Called when comparing two board objects.
        A board is considered equal when having the same pieces, legal moves and player to move.
        Because we delete the board when player castles, we only need to check if the turn and piece positions are the same.
        """
        equal = True
        if self.board2str() != other_board.board2str():
            equal = False
        if self.turn != other_board.turn:
            equal = False
        return equal
    
    def __hash__(self):
        """
        Called when used as key in a dictionary.
        A board is considered equal when having the same pieces, legal moves and player to move.
        Because we delete the board when player castles, we only need to check if the turn and piece positions are the same.
        """

        return hash((self.board_2_str(), self.turn))


    def __setitem__(self, key, value):
        self.board[key[0]][key[1]] = value
                    

    def __getitem__(self, item):
        return self.board[item[0]][item[1]]

    def get_ghost_pawn(self, color):
        if color:
            return self.white_ghost_pawn
        else:
            return self.black_ghost_pawn

    def deactivate_ghost_pawn(self, color):
        if color:
            self.white_ghost_pawn = None
        else:
            self.black_ghost_pawn = None

    def activate_ghost_pawn(self, pos, color):
        if color:
            self.white_ghost_pawn = (pos[0], pos[1] - 1)
        else:
            self.black_ghost_pawn = (pos[0], pos[1] + 1)

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

    def has_same_target(self, piece1, piece2):
        targets1 = piece1.get_valid_moves()
        targets2 = piece1.get_valid_moves()
        same_targets = [move for move in targets1 if move in targets2]
        return len(same_targets)


    def get_piece(self, name, color):
        l = []
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece:
                    if piece.name == name:
                        if piece.color == color:
                            l.append(piece)
        return l

    def pieces_in_same_column(self, name, color):
        two_piece_types = False
        for j in range(8):
            has_piece = False
            for i in range(8):
                piece = self.board[i,j]
                if piece:
                    if piece.name == name and piece.color == color:
                        if has_piece:
                            two_piece_types = True
                        else:
                            has_piece = True



    def get_controlled_squares(self, color):
        enemy_moves = set()
        for otherpiece in self.vector():
            if otherpiece:
                if otherpiece.color == color:
                    if otherpiece.name != "K":
                        for move in otherpiece.get_valid_moves(self):
                            enemy_moves.add(move[1])
                    if otherpiece.name == "K":
                        for move in otherpiece.get_normal_valid_moves(self):
                            enemy_moves.add(move[1])
        return list(enemy_moves)

