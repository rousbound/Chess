
class Piece():
    """
    Base class to represent Pieces

    Attributes:
    ----------
    color : bool
        White if true Black if false

    name : string
        Piece type

    x : int
        X coordinate of piece

    y : int
        Y coordinate of piece

    Methods:
    ----------

    move(to:tup, board:Board) -> captured_piece:Piece
        Moves piece to 'to'. Returns captured_piece if there is

    move_is_possible(move:to, board:Board) -> bool
        Checks if move is withing board boundaries,
        and if target location is not occupied by allied piece

    get_diagonal_moves(board:Board) -> list[tup]
        Returns diagonal moves of selected piece

    get_ortogonal_moves(board:Board) -> list[tup]
        Returns diagonal moves of selected piece

    """
    def __init__(self, color : bool, x,y):
        self.color = color
        self.name = ""
        self.x : int = x
        self.y : int = y
        self.pos = (x,y)
        self.piece_held = False

    def get_pos(self):
        """
        Gets position of piece in the board.
        """
        return (self.x, self.y)

    def set_pos(self, pos):
        """
        Sets position of piece in the board.
        Updates x and y.
        """
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]

    def move(self, to, board):
        """
        Make piece move.

        """
        ep_piece_captured = None
        if self.name == "P":
           ep_piece_captured = self.is_en_passeant((self.get_pos(), to), board)
           if ep_piece_captured:
               board[ep_piece_captured.get_pos()] = None

        board[self.get_pos()] = None
        captured_piece = board[to] if not ep_piece_captured else ep_piece_captured
        # captured_piece = board[to]
        board[to]= self
        self.set_pos(to)


        return captured_piece

    def __repr__(self):
        return self.name

    def move_is_possible(self, move, board):
        """
        Checks if move is inside board boundaries.

        """
        if not ( 0 <= move[0] <= 7 and 0 <= move[1] <= 7):
            return False
        if board[move[0],move[1]]:
            if board[move[0],move[1]].color == self.color:
                return False
        return True

    def get_valid_moves(self, board):
        """
        Get valid moves for the piece.

        """

    def get_diagonal_moves(self, board):
        """
        Get diagonal moves for Queen and Bishop.

        """
        target_squares = set()
        
        # North-West, South-East, Nort-East, South-West
        nw_min = min(self.x,self.y)
        se_min = min(8-self.x,8-self.y)
        ne_min = min(8-self.x,self.y)
        sw_min = min(self.x,8-self.y)
        nw = [(self.x-i, self.y-i) for i in range(1,nw_min+1)]
        se = [(self.x+i, self.y+i) for i in range(1,se_min+1)]
        ne = [(self.x+i, self.y-i) for i in range(1,ne_min+1)]
        sw = [(self.x-i, self.y+i) for i in range(1,sw_min+1)]
        for l_squares in [nw, se, ne, sw]:
            for x,y in l_squares:
                if  (0 <= x <= 7) and  (0 <= y <= 7):
                    if board[x,y]:
                        if board[x,y].color != self.color:
                            target_squares.add((x,y))
                        break
                    target_squares.add((x,y))

        moves = [(self.get_pos(), target, "%") for target in target_squares]
        return moves

    def get_ortogonal_moves(self, board):
        """
        Get ortogonal moves for Queen and Rook.

        """
        target_squares = []
        right = [(self.x-i, self.y) for i in range(1,self.x+1)]
        left = [(self.x+i, self.y) for i in range(1,7-self.x+1)]
        bottom = [(self.x, self.y-i) for i in range(1,self.y+1)]
        up = [(self.x, self.y+i) for i in range(1,7-self.y+1)]
        for l_squares in [right, left, bottom, up]:
            for x,y in l_squares:
                if board[x,y]:
                    if board[x,y].color != self.color:
                        target_squares.append((x,y))
                    break
                target_squares.append((x,y))
        moves = [(self.get_pos(), target, "%") for target in target_squares]
        return moves





class Rook(Piece):
    def __init__(self, color,x,y, rook_side = None):
        """
            Rook moves
        8 |_| |_|X|_| |_| |
        7 | |_| |X| |_| |_|
        6 |_| | |X| | |_| |
        5 | | | |X| | | |_|
        4 |X|X|X|N|X|X|X|X|
        3 | | | |X| | | |_|
        2 |_| | |X| | |_| |
        1 | |_| |X| |_| |_|
          a b c d e f g h
        """
        """
        Same as base class Piece, except `first_move` is used to check
        if this rook can castle.
        """
        super().__init__(color,x,y)
        self.name = "R"
        self.rook_side = rook_side
        self.moves = []
        self.x = x
        self.y = y

    def get_valid_moves(self, board):
        moves = self.get_ortogonal_moves(board)
        return moves


class Bishop(Piece):
    def __init__(self, color, x,y, color_complex = True):
        """
                    Bishop moves
               8 |_| |_| |_| |_|X|
               7 |X|_| | | |_|X|_|
               6 |_|X| | | |X|_| |
               5 | | |X| |X| | |_|
               4   | | |B| | | | |
               3 | | |X| |X| | |_|
               2 |_|X| | | |X|_| |
               1 |X|_| | | |_|X|_|
                  a b c d e f g h
        """
        super().__init__(color,x,y)
        self.name = "B"
        self.moves = []
        self.color_complex = color_complex
        self.x = x
        self.y = y

    def get_valid_moves(self, board):
        moves = self.get_diagonal_moves(board)
        return moves

class Knight(Piece):
    def __init__(self, color,x,y):
        """
                    Knight moves
               8 |_| |_| |_| |_| |
               7 | |_| |_| |_| |_|
               6 |_| |X| |X| |_| |
               5 | |X| |_| |X| |_|
               4 |_| |_|N|_| |_| |
               3 | |X| |_| |X| |_|
               2 |_| |X| |X| |_| |
               1 | |_| |_| |_| |_|
                  a b c d e f g h
        """
        super().__init__(color,x,y)
        self.name = "N"
        self.moves = []
        self.x = x
        self.y = y

    def get_valid_moves(self, board):
        targets = [
                (self.x + 2, self.y + 1),
                (self.x + 2, self.y - 1),
                (self.x - 2, self.y + 1),
                (self.x - 2, self.y - 1),
                (self.x + 1, self.y + 2),
                (self.x + 1, self.y - 2),
                (self.x - 1, self.y + 2),
                (self.x - 1, self.y - 2),
                ]
        moves = [(self.get_pos(), target, "%") for target in targets]
        moves = [move for move in moves if self.move_is_possible(move[1], board)]
        return moves

class Queen(Piece):
    """
                Queen moves
           8 |_| |_|X|_| |_|X|
           7 |X|_| |X| |_|X|_|
           6 |_|X| |X| |X|_| |
           5 | | |X|X|X| | |_|
           4 |X|X|X|Q|X|X|X|X|
           3 | | |X|X|X| | |_|
           2 |_|X| |X| |X|_| |
           1 |X|_| |X| |_|X|_|
              a b c d e f g h
    """
    def __init__(self, color, x,y):
        super().__init__(color,x,y)
        self.name = "Q"
        self.moves = []
        self.x = x
        self.y = y

    def get_valid_moves(self, board):
        diag_moves = self.get_diagonal_moves(board)
        ortog_moves = self.get_ortogonal_moves(board)
        moves = diag_moves + ortog_moves

        return moves

class Pawn(Piece):
    """
                Pawn Attack               Pawn Movement(One or two squares if first move)
           8 |_| |_| |_| |_| |         8 |_| |_| |_| |_| |
           7 | |_| | | |_| |_|         7 | |_| | | |_| |_|
           6 |_| | | | | |_| |         6 |_| | | | | |_| |
           5 | | | | | | | |_|         5 | | | | | | | |_|
           4   | | | | | | | |         4   | | |X| | | | |
           3 | | |X| |X| | |_|         3 | | | |X| | | |_|
           2 |_| | |P| | |_| |         2 |_| | |P| | |_| |
           1 | |_| | | |_| |_|         1 | |_| | | |_| |_|
              a b c d e f g h             a b c d e f g h
    """
    def __init__(self, color,x,y, first_move = True):
        super().__init__(color,x,y)
        self.name = "P"
        self.first_move = first_move
        self.moves = []
        self.x = x
        self.y = y

    def is_en_passeant(self, move, board):
        start = move[0]
        to = move[1]

        iscapture = lambda x,y : abs(x[0]-y[0]) == 1 and abs(x[1]-y[1]) == 1
        if iscapture(start, to):
            enemy_ghost_pawn = board.get_ghost_pawn(not board.turn)
            if to == enemy_ghost_pawn:
                if self.color:
                    piece_captured = board[to[0],to[1]+1]
                    
                else:
                    piece_captured = board[to[0],to[1]-1] 
                return piece_captured

    def get_valid_moves(self, board):
        # Check promotion function for captures and normal movement
        def check_promotion(moves, target):
            if last_row == target[1]:
                for promotion in ["q","b","r","n"]:
                    moves.append((self.get_pos(), target, promotion))
            else:
                moves.append((self.get_pos(), target, "%"))
            return moves

        ahead = -1 if self.color else 1
        last_row = 0 if self.color else 7
        pos_ahead = (self.x, self.y + ahead)
        pos_ahead_ahead = (self.x, self.y + (2*ahead)) if 0 < self.y + 2*ahead <= 7 else None
        piece_ahead = board[pos_ahead]
        piece_ahead_ahead = board[pos_ahead_ahead] if pos_ahead_ahead else None
        moves = []
        # Check double movement
        if self.first_move:
            if not piece_ahead:
                if not piece_ahead_ahead:
                    moves.append((self.get_pos(), pos_ahead_ahead, "%"))


        # Check Captures
        if 0 <= pos_ahead[1] <= 7:
            if piece_ahead is None:
                moves = check_promotion(moves, pos_ahead)

            for side in [1,-1]:
                if 0 <= self.x + side <= 7:
                    target = (self.x + side, self.y + ahead)
                    if board[target] and (board[target].color != self.color):
                            moves = check_promotion(moves, target)

                    else:
                        # If there is no piece maybe there is ghostpawn
                        # Therefore, En Passeant
                        enemy_ghost_pawn = board.get_ghost_pawn(not self.color)
                        if enemy_ghost_pawn == target:
                            move = (self.get_pos(), target, "%")
                            moves.append(move)
        self.moves = moves
        return self.moves


class King(Piece):
    """
                King moves
           8 |_| |_| |_| |_| |
           7 | |_| |_| |_| |_|
           6 |_| |_| |_| |_| |
           5 | |_|X|X|X|_| |_|
           4 |_| |X|K|X| |_| |
           3 | |_|X|X|X|_| |_|
           2 |_| |_| |_| |_| |
           1 | |_| |_| |_| |_|
              a b c d e f g h
    """
    def __init__(self, color, x, y, first_move = True):
        super().__init__(color, x, y)
        self.name = "K"
        self.first_move = first_move
        self.moves = []
        self.x = x
        self.y = y
        self.in_check = False


    def get_normal_valid_moves(self, board):
        """
        King needs a separate function to get possible moves
        and avoid recursion.

        """
        targets = [
                (self.x + 1 , self.y),
                (self.x - 1 , self.y),
                (self.x , self.y - 1),
                (self.x , self.y + 1),
                (self.x + 1 , self.y + 1),
                (self.x + 1 , self.y -1),
                (self.x - 1 , self.y -1),
                (self.x - 1 , self.y + 1),
                ]
        # Create move
        candidate_moves = [(self.get_pos(), target, "%") for target in targets]
        candidate_moves = [move for move in candidate_moves if self.move_is_possible(move[1], board)]
        return candidate_moves

    def get_valid_moves(self, board):
        enemy_targets = board.get_controlled_squares(not self.color)

        candidate_moves = self.get_normal_valid_moves(board)

        # Check Castling possibility
        if not self.in_check:
            for rook in board.get_piece("R", self.color):
                castle_enabled = True
                if not board.can_castle[rook.rook_side]:
                    continue
                if rook.rook_side in "qQ":
                    in_between_squares = [(self.x-2, self.y), (self.x-1, self.y)]
                    king_to = (self.x-2, self.y)
                elif rook.rook_side in "kK":
                    in_between_squares = [(self.x+1, self.y), (self.x+2, self.y)]
                    king_to = (self.x+2, self.y)
                for square in in_between_squares:
                    # If square have pieces, castle is not possible
                    # Still, if square doesn't have pieces,
                    # check if they are controlled by enemy pieces
                    if board[square]:
                        castle_enabled = False
                    else:
                        if square in enemy_targets:
                            castle_enabled = False
                if castle_enabled:
                    move = (self.get_pos(), king_to, "%")
                    candidate_moves.append(move)
        self.moves = candidate_moves
        return self.moves

