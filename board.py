import pieces
import utils

"""
Module made for Board class.
It encompasses every information that is relevant to save the position in the form of a FEN string.

"""

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
        Initializes the board per standard chess rules.
        """

        self.board = []
        self.turn = True
        self.turn_counter = 1
        self.moves_list = []
        self.algebric_legal_moves = []
        self.can_castle = {"K": True, "Q": True, "k": True, "q": True}
        self.no_progress_plies = 0
        self.setup_board()
        self.white_ghost_pawn = None
        self.black_ghost_pawn = None

    def setup_board(self):
        """
        Populate board with pieces starting position.

        """
        # Board set-up
        for i in range(8):
            self.board.append([None] * 8)

        # White
        self.board[0][7] = pieces.Rook(True,0,7)
        self.board[1][7] = pieces.Knight(True,1,7)
        self.board[2][7] = pieces.Bishop(True,2,7)
        self.board[3][7] = pieces.Queen(True,3,7)
        self.board[4][7] = pieces.King(True,4,7)
        self.board[5][7] = pieces.Bishop(True,5,7)
        self.board[6][7] = pieces.Knight(True,6,7)
        self.board[7][7] = pieces.Rook(True,7,7)

        for i in range(8):
            self.board[i][6] = pieces.Pawn(True,i,6)

        # Black
        self.board[0][0] = pieces.Rook(False,0,0)
        self.board[1][0] = pieces.Knight(False,1,0)
        self.board[2][0] = pieces.Bishop(False,2,0)
        self.board[3][0] = pieces.Queen(False,3,0)
        self.board[4][0] = pieces.King(False,4,0)
        self.board[5][0] = pieces.Bishop(False,5,0)
        self.board[6][0] = pieces.Knight(False,6,0)
        self.board[7][0] = pieces.Rook(False,7,0)

        for i in range(8):
            self.board[i][1] = pieces.Pawn(False,i,1)

    def remove_castling_rights(self, color):
        """
        Completely remove castling rights of player.
        Done after moving king.
        """
        if color:
            self.can_castle["Q"] = False
            self.can_castle["K"] = False
        else:
            self.can_castle["q"] = False
            self.can_castle["k"] = False


    def check_castling_rights(self):
        """
        Check which rook has moved and the correspondent
        castling right that should be disabled by its move.
        """
        if self[0,7]:
            if self[0,7].name != "R":
                self.can_castle["Q"] = False
        else:
            self.can_castle["Q"] = False

        if self[7,7]:
            if self[7,7].name != "R":
                self.can_castle["K"] = False
        else:
            self.can_castle["K"] = False
        if self[0,0]:
            if self[0,0].name != "R":
                self.can_castle["q"] = False
        else:
            self.can_castle["q"] = False
        if self[7,0]:
            if self[7,0].name != "R":
                self.can_castle["k"] = False
        else:
            self.can_castle["k"] = False

    def board_2_FEN(self):
        """
        Converts game state to FEN,
        which encodes the group of all possible legal moves in a position.
        For that matter it is necessary:
        pieces position, castling rights, En passeant capture possibility, and
        number of "no progress moves" and turn counter.

        """
        FEN = ""
        for y in range(8):
            no_piece = 0
            for x in range(8):
                piece = self[x,y]
                if piece:
                    if no_piece != 0:
                        FEN += str(no_piece)
                        no_piece = 0
                    if piece.color:
                        FEN += piece.name
                    else:
                        FEN += piece.name.lower()
                elif x != 7:
                    no_piece += 1
                elif x == 7:
                    no_piece += 1
                    if no_piece != 0:
                        FEN += str(no_piece)
            if y != 7:
                FEN += "/"
        FEN += " w " if self.turn else " b "
        can_castle = ""
        for key, value in self.can_castle.items():
            if value:
                can_castle += key
        can_castle = "-" if len(can_castle) == 0 else can_castle
        FEN += can_castle
        if self.white_ghost_pawn:
            FEN += " " + utils.mat_2_uci(self.white_ghost_pawn)
        elif self.black_ghost_pawn:
            FEN += " " + utils.mat_2_uci(self.black_ghost_pawn)
        elif not self.white_ghost_pawn and not self.black_ghost_pawn:
            FEN += " " + "-"
        FEN += " " + str(self.no_progress_plies)
        FEN += " " + str(self.turn_counter)

        return FEN




    def __eq__(self, other_board):
        """
        Called when comparing two board objects.
        A board is considered equal when having the same pieces, legal moves and player to move.
        Because we delete the board when player castles,
        we only need to check if the turn and piece positions are the same.
        """
        return self.board_2_FEN() != other_board.board_2_FEN()

    def __hash__(self):
        """
        Called when used as key in a dictionary.
        A board is considered equal when having the same pieces, legal moves and player to move.
        Because we delete the board when player castles,
        we only need to check if the turn and piece positions are the same.
        """

        return hash((self.board_2_FEN()))


    def __setitem__(self, key, value):
        self.board[key[0]][key[1]] = value


    def __getitem__(self, item):
        return self.board[item[0]][item[1]]

    def get_ghost_pawn(self, color):
        """
        Return ghost pawn of desired color
        """

        if color:
            return self.white_ghost_pawn
        return self.black_ghost_pawn

    def deactivate_ghost_pawn(self, color):
        """
        Sets the value of ghost pawn of desired color to none

        """

        if color:
            self.white_ghost_pawn = None
        else:
            self.black_ghost_pawn = None

    def activate_ghost_pawn(self, pos, color):
        """
        Sets the value of ghost pawn of desired color to a certain position
        """

        if color:
            self.white_ghost_pawn = (pos[0], pos[1] - 1)
        else:
            self.black_ghost_pawn = (pos[0], pos[1] + 1)

    def vector(self):
        """
        Returns the board pieces in a vector for linear iteration.
        """
        
        vec = []
        for i in range(8):
            for j in range(8):
                vec.append(self[i,j])
        return vec

    def print_board(self):
        """
        Prints the current state of the board.
        """

        column_labels = "abcdefgh"
        BOARD_LEN = 8
        buffer = ""
        for i in range(33):
            buffer += "*"
        buffer += "\n"
        for y in range(BOARD_LEN):
            tmp_str = f"{8-y}|"
            for x in range(BOARD_LEN):
                if self[x,y] is None:
                    tmp_str += "   |"
                else:
                    if self[x,y].color == True:
                        tmp_str += (" " + str(self[x,y]) + " |")
                    else:
                        tmp_str += (" " + str(self[x,y]).lower() + " |")

            buffer += tmp_str + "\n"
        for i in range(BOARD_LEN):
            buffer += f"   {column_labels[i]}"
        buffer += "\n"

        for i in range(33):
            buffer += "*"
        buffer += "\n"
        return buffer


    def has_same_target(self, start, piece, color):
        """
        Designed to check if two pieces can go to the same square.
        Returns the information needed to distinct the start square.

        """
        specifier = ""
        l_pieces = self.get_piece(piece.name, color)
        if len(l_pieces) == 2:
            other_piece = l_pieces[0] if l_pieces[0].get_pos() != piece.get_pos() else l_pieces[1]
            self[piece.get_pos()] = None
            other_piece_targets = other_piece.get_valid_moves(self)
            other_piece_targets = [move[1] for move in other_piece_targets]
            if piece.get_pos() in other_piece_targets:
                uci_move = utils.mat_2_uci(start)
                if start[0] == other_piece.x:
                    specifier = uci_move[1]
                elif start[1] == other_piece.y:
                    specifier = uci_move[0]
                else:
                    specifier = uci_move[0]
            self[piece.get_pos()] = piece
            return specifier
        return ""


    def get_piece(self, name, color):
        """
        Iterates through board and return desired piece in a list.
        If it is king return just the piece object.
        """

        l_pieces = []
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece:
                    if piece.color == color:
                        if name == "K":
                            if piece.name == "K":
                                return piece
                        elif piece.name == name:
                            l_pieces.append(piece)
        return l_pieces



    def get_controlled_squares(self, color):
        """
        Returns squares which are target of pieces of a certain color.
        """

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
