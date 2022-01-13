import utils

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

    moveIsPossible(move:to, board:Board) -> bool
        Checks if move is withing board boundaries,
        and if target location is not occupied by allied piece

    get_diagonal_moves(board:Board) -> list[tup]
        Returns diagonal moves of selected piece

    get_ortogonal_moves(board:Board) -> list[tup]
        Returns diagonal moves of selected piece

    """
    def __init__(self, color, x,y):
        self.color = color
        self.name = ""
        self.x = x
        self.y = y
        self.pos = (x,y)
        self.pieceHeld = False

    def get_pos(self):
        return (self.x, self.y)

    def set_pos(self, pos):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]

    def move(self, to, board):
        print("TO:",to)
        board[self.get_pos()] = None
        captured_piece = board[to]
        board[to]= self
        self.x = to[0]
        self.y = to[1]
        return captured_piece
    
    def get_valid_moves_after(self, to , board):
        origin = (self.x,self.y)
        captured_piece = self.move(to, board)
        legal_moves_after = self.get_valid_moves(board)
        self.move(origin, board)
        if captured_piece:
            captured_piece.move(to, board)
        return legal_moves_after
    
    def __repr__(self):
        return self.name

    def moveIsPossible(self, move, board):
        if not ( 0 <= move[0] <= 7 and 0 <= move[1] <= 7):
            return False
        else:
            if board[move[0],move[1]]:
                if board[move[0],move[1]].color == self.color:
                    return False
        return True

    def get_diagonal_moves(self, board):
        target_squares = set()
        for i in range(1,8):
            x,y = self.x-i, self.y-i
            if x <= 7 and y <= 7 and x>=0 and y>=0:
                if board[x,y]:
                    if board[x,y].color == self.color:
                        break
                    else:
                        target_squares.add((x,y))
                        break
                else:
                    target_squares.add((x,y))
        for i in range(1,8):
            x,y = self.x+i,self.y+i
            if x <= 7 and y <= 7 and x>=0 and y>=0:
                if board[x,y]:
                    if board[x,y].color == self.color:
                        break
                    else:
                        target_squares.add((x,y))
                        break
                else:
                    target_squares.add((x,y))
        for i in range(1,8):
            x,y = self.x+i,self.y-i
            if x <= 7 and y <= 7 and x>=0 and y>=0:
                if board[x,y]:
                    if board[x,y].color == self.color:
                        break
                    else:
                        target_squares.add((x,y))
                        break
                else:
                    target_squares.add((x,y))
        for i in range(1,8):
            x,y = self.x-i,self.y+i
            if x <= 7 and y <= 7 and x>=0 and y>=0:
                if board[x,y]:
                    if board[x,y].color == self.color:
                        break
                    else:
                        target_squares.add((x,y))
                        break
                else:
                    target_squares.add((x,y))

        moves = [(self.get_pos(), target, 0) for target in target_squares]
        return moves

    def get_ortogonal_moves(self, board):
        target_squares = []
        for i in range(1, self.x+1):
            if board[self.x-i,self.y]:
                if board[self.x-i,self.y].color == self.color:
                    break
                else:
                    target_squares.append((self.x-i,self.y))
                    break
            else:
                target_squares.append((self.x-i,self.y))
        for i in range(1, 7-self.x+1):
            if board[self.x+i,self.y]:
                if board[self.x+i,self.y].color == self.color:
                    break
                else:
                    target_squares.append((self.x+i,self.y))
                    break
            else:
                target_squares.append((self.x+i,self.y))
        for i in range(1, self.y+1):
            if board[self.x,self.y-i]:
                if board[self.x,self.y-i].color == self.color:
                    break
                else:
                    target_squares.append((self.x,self.y-i))
                    break
            else:
                target_squares.append((self.x,self.y-i))
        for i in range(1, 7-self.y+1):
            if board[self.x,self.y+i]:
                if board[self.x,self.y+i].color == self.color:
                    break
                else:
                    target_squares.append((self.x,self.y+i))
                    break
            else:
                target_squares.append((self.x,self.y+i))
        moves = [(self.get_pos(), target, 0) for target in target_squares]
        return moves





class Rook(Piece):
    def __init__(self, color,x,y, first_move = True):
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
        self.first_move = first_move 
        self.moves = []
        self.x = x
        self.y = y

    def get_valid_moves(self, board):
        moves = self.get_ortogonal_moves(board)
        return moves


class Bishop(Piece):
    def __init__(self, color, x,y):
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
        self.x = x
        self.y = y

    def get_valid_moves(self, board):
        moves = self.get_diagonal_moves(board)
        return moves

class Knight(Piece):
    def __init__(self, color,x,y, first_move = True):
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
        moves = [
                (self.x + 2, self.y + 1),
                (self.x + 2, self.y - 1),
                (self.x - 2, self.y + 1),
                (self.x - 2, self.y - 1),
                (self.x + 1, self.y + 2),
                (self.x + 1, self.y - 2),
                (self.x - 1, self.y + 2),
                (self.x - 1, self.y - 2),
                ]
        moves = [(self.get_pos(), move, 0) for move in moves]
        moves = [move for move in moves if self.moveIsPossible(move[1], board)]
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
    def __init__(self, color, x,y,  first_move = True):
        super().__init__(color,x,y)
        self.name = "Q"
        self.first_move = first_move 
        self.moves = []
        self.x = x
        self.y = y

    def get_valid_moves(self, board):
        diag_moves = self.get_diagonal_moves(board)
        ortog_moves = self.get_ortogonal_moves(board)
        # moves = set()
        # for move in diag_moves+ortog_moves:
            # moves.add(move)
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

    def get_valid_moves(self, board):
        # Check promotion function for captures and normal movement
        def checkPromotion(moves, target):
            if lastRow == target[1]:
                for promotion in ["q","b","r","n"]:
                    moves.append((self.get_pos(), target, promotion))
            else:
                moves.append((self.get_pos(), target, 0))
            return moves

        ahead = 1 if self.color else -1
        lastRow = 0 if self.color else 7
        posAhead = (self.x, self.y - ahead)
        posAheadAhead = (self.x, self.y - (2*ahead))
        pieceAhead = board[posAhead]
        pieceAheadAhead = board[posAheadAhead]
        moves = []
        # Check double movement
        if self.first_move:
            if not pieceAhead:
                if not pieceAheadAhead:
                    moves.append((self.get_pos(), posAheadAhead,"dpm"))
            

        # Check Captures
        if 0 <= posAhead[1] <= 7:
            if pieceAhead == None:
                moves = checkPromotion(moves, posAhead)

            for side in [1,-1]:
                if 0 <= self.x + side <= 7:
                    target = (self.x + side, self.y - ahead)
                    if board[target]:
                        if board[target].color != self.color:
                            moves = checkPromotion(moves, target)

                    else:
                        # If there is no piece maybe there is ghostpawn
                        # Therefore, En Passeant
                        enemyGhostPawn = board.getGhostPawn(not self.color)
                        if enemyGhostPawn:
                            if enemyGhostPawn == target:
                                moves.append((self.get_pos(), target, "enp"))
        # Check Promotion


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
        self.inCheck = False

    
    def getNormalValidMoves(self, board):
        candidate_moves = [
                (self.x + 1 , self.y),
                (self.x - 1 , self.y),
                (self.x , self.y - 1),
                (self.x , self.y + 1),
                (self.x + 1 , self.y + 1),
                (self.x + 1 , self.y -1),
                (self.x - 1 , self.y -1),
                (self.x - 1 , self.y + 1),
                ]
        # Check if move is within borders, and target square is occupied by enemy piece
        candidate_moves = [(self.get_pos(), move, 0) for move in candidate_moves]
        candidate_moves = [move for move in candidate_moves if self.moveIsPossible(move[1], board)]
        return candidate_moves

    def get_valid_moves(self, board):
        enemyTargets = board.getControlledSquares(not self.color)

        candidate_moves = self.getNormalValidMoves(board)

        flag = 0
        # Check Castling possibility
        if self.first_move:
            for rook in board.getRooks(self.color):
                if rook.first_move:
                    if rook.x == 0:
                        squaresList = [(self.x-2,self.y),(self.x-1,self.y)]
                        kingTo = (self.x-2,self.y)
                        flag = "lc"
                    elif rook.x == 7:
                        squaresList = [(self.x+1,self.y),(self.x+2,self.y)]
                        kingTo = (self.x+2,self.y)
                        flag = "rc"
                    castleEnabled = True
                    for square in squaresList:
                        # If square doesn't have pieces,
                        # check if they are controlled by enemy pieces
                        if not board[square]:
                            if square in enemyTargets:
                                castleEnabled = False
                        # Else, castling not possible
                        else:
                            castleEnabled = False
                    if castleEnabled:
                        candidate_moves.append((self.get_pos(), kingTo, flag))
        self.moves = candidate_moves
        return self.moves

