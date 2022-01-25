from pieces import King, Queen, Rook, Bishop, Knight, Pawn
from utils import mat_2_uci
from collections import OrderedDict

class Board():
    """
    A class to represent a chess board, and all information necessary to save and load
    the board state in the form of a FEN.
    ...

    Attributes:
    -----------
    board : list[list[Piece]]
        represents a chess board

    turn : bool
        True if white's turn

    turn_counter : int
        Turn counter, relevant for FEN creation

    no_progress_plies: int
        Ply counter, relevant for draw criteria and FEN creation

    can_castle : dict
        Saves right to castle information.
        Obs: Right to castle != Castle legality
        Ex: Castle might be ILLEGAL at certain position, but you have the RIGHT
        to do it after, if criteria are met.
        After castling or moving king or rook you dont have the RIGHT to
        castle anymore.

    white_ghost_pawn : tup
    black_ghost_pawn : tup
        The coordinates of a white/black ghost piece representing a takeable pawn for en passant

    board_states : list[Board]
        List of boards, relevant for three fold repetition draw criteria.

    Methods:
    --------
    print_board() -> None
        Prints the current configuration of the board

    setup_board() -> None
        Populates board with initial position

    get_controlled_squares(color : bool) -> list[tup]
        Returns coordinates of squares controlled by chosen color

    remove_castling_rights(color: bool) -> None
        Remove castling rights of player

    board_2_FEN() -> str
        Make a string representation of the board in the well known FEN format

    get_ghost_pawn(color: bool) -> tup
        Returns the ghost pawn of the desired color

    deactivate_ghost_pawn(color : bool) -> None
        Deactivates ghost pawn of desired color

    activate_ghost_pawn(pos, color) -> None
        Activates ghost pawn of desired color

    get_all_pieces() -> list[Piece]
        Returns all board alive pieces in a list for easy iteration

    has_same_target(start : tup, color: bool, piece : Piece) -> str
        Check if two pieces could have gone to the same square and return
        information needed to discern the start piece.

    get_piece(name : str, color : bool) -> list[Piece]
        Get list of pieces of desired type and color

    get_king(color : bool) -> Piece
        Get king of desired color


    """
    def __init__(self, FEN=None):
        """
        Initializes the board per standard chess rules.
        """

        self.board = [[None]*8 for _ in range(8)]
        self.turn = True
        self.turn_counter = 1
        self.can_castle = {"K": True, "Q": True, "k": True, "q": True, None: False}
        self.no_progress_plies = 0
        self.white_ghost_pawn = None
        self.black_ghost_pawn = None
        self.board_states_counter = OrderedDict()

        if FEN:
            self.FEN_2_board(FEN)
        else:
            self.setup_initial_position()

    def __setitem__(self, key, value):
        self.board[key[0]][key[1]] = value


    def __getitem__(self, item):
        return self.board[item[0]][item[1]]

    def setup_initial_position(self):
        """
        Populate board with pieces starting position.

        """

        # White
        self.board[0][7] = Rook(True,0,7, rook_side = "Q")
        self.board[1][7] = Knight(True,1,7)
        self.board[2][7] = Bishop(True,2,7, color_complex = True)
        self.board[3][7] = Queen(True,3,7)
        self.board[4][7] = King(True,4,7)
        self.board[5][7] = Bishop(True,5,7, color_complex = False)
        self.board[6][7] = Knight(True,6,7)
        self.board[7][7] = Rook(True,7,7, rook_side = "K")

        for i in range(8):
            self.board[i][6] = Pawn(True,i,6)

        # Black
        self.board[0][0] = Rook(False,0,0, rook_side = "q")
        self.board[1][0] = Knight(False,1,0)
        self.board[2][0] = Bishop(False,2,0, color_complex = False)
        self.board[3][0] = Queen(False,3,0)
        self.board[4][0] = King(False,4,0)
        self.board[5][0] = Bishop(False,5,0, color_complex = True)
        self.board[6][0] = Knight(False,6,0)
        self.board[7][0] = Rook(False,7,0, rook_side = "k")

        for i in range(8):
            self.board[i][1] = Pawn(False,i,1)

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


    def FEN_2_board(self, FEN):
        fen_pieces, turn, castling, enpasseant, no_progress_counter, turn_counter = FEN.split(" ")

        self.can_castle = {"K": False, "Q": False, "k": False, "q": False, None: False}

        # Load turn
        self.turn = turn == "w"

        # Load castling rights
        for side_color in castling:
            self.can_castle[side_color] = True

        # Load counters
        self.no_progress_counter = int(no_progress_counter)
        self.turn_counter = int(turn_counter)

        # Load En Passeant
        if enpasseant != "-":
            if self.turn:
                self.black_ghost_pawn = mat_2_uci(enpasseant)
            else:
                self.white_ghost_pawn = mat_2_uci(enpasseant)

        # Load pieces

        skip = 0
        squares = 0
        fen_pieces = fen_pieces.replace("/","")
        i = 0
        while True:
            x, y = squares%8, squares//8
            char = fen_pieces[i]
            if char in "12345678":
                skip += int(char)
                squares += int(char)
                i+=1
            elif skip == 0:
                if char in "rnbqkpRNBQKP":
                    squares += 1
                    color = char.isupper() 
                    if char in "rR":
                        rook_side = None
                        if (x,y) == (0,0):
                            rook_side = "q"
                        if (x,y) == (0,7):
                            rook_side = "Q"
                        if (x,y) == (7,0):
                            rook_side = "k"
                        if (x,y) == (7,7):
                            rook_side = "K"
                        self[x,y] = Rook(color, x, y, rook_side)
                    if char in "nN":
                        self[x,y] = Knight(color, x, y)
                    if char in "bB":
                        self[x,y] = Bishop(color, x, y, color_complex = True)
                    if char in "qQ":
                        self[x,y] = Queen(color, x, y)
                    if char in "kK":
                        self[x,y] = King(color, x, y)
                    if char in "pP":
                        if (char == "p" and y == 1) or (char == "P" and y == 6):
                            self[x,y] = Pawn(color, x , y, first_move = True)
                        else:
                            self[x,y] = Pawn(color, x , y, first_move = False)

                    i+=1
            elif skip != 0:
                skip = max(0,skip-1)


            if squares == 64:
                break
        





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

        # Concatanate turn information
        FEN += " w " if self.turn else " b "
        can_castle = ""

        # Concatenate castling right information
        for key, value in self.can_castle.items():
            if value:
                can_castle += key
        can_castle = "-" if len(can_castle) == 0 else can_castle
        FEN += can_castle

        # Concatenate En passeant information
        if self.white_ghost_pawn:
            FEN += " " + mat_2_uci(self.white_ghost_pawn)
        elif self.black_ghost_pawn:
            FEN += " " + mat_2_uci(self.black_ghost_pawn)
        elif not self.white_ghost_pawn and not self.black_ghost_pawn:
            FEN += " " + "-"

        # Concatenate turn counter and no progress plies information
        FEN += " " + str(self.no_progress_plies)
        FEN += " " + str(self.turn_counter)

        return FEN





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

    def get_all_pieces(self):
        """
        Returns the board pieces in a vector for linear iteration.
        """

        l_pieces = []
        for i in range(8):
            for j in range(8):
                if self[i,j]:
                    l_pieces.append(self[i,j])
        return l_pieces

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
                uci_move = mat_2_uci(start)
                if start[0] == other_piece.x:
                    specifier = uci_move[1]
                elif start[1] == other_piece.y:
                    specifier = uci_move[0]
                else:
                    specifier = uci_move[0]
            self[piece.get_pos()] = piece
            return specifier
        return ""

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
                    if self[x,y].color:
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
        print(buffer)


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
                    if piece.color == color and piece.name == name:
                        l_pieces.append(piece)
        return l_pieces

    def get_king(self, color):
        """
        Get king of desired color

        """

        return self.get_piece("K", color)[0]

    def get_controlled_squares(self, color):
        """
        Returns squares which are target of pieces of a certain color.
        """

        enemy_moves = set()
        for otherpiece in self.get_all_pieces():
            if otherpiece.color == color:
                if otherpiece.name != "K":
                    for move in otherpiece.get_valid_moves(self):
                        enemy_moves.add(move[1])
                if otherpiece.name == "K":
                    for move in otherpiece.get_normal_valid_moves(self):
                        enemy_moves.add(move[1])
        return list(enemy_moves)
