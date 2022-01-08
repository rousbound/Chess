def translate(n):
    s = "abcdefgh"
    return s[int(n+1)]

def translateMoves(xstart,ystart,xend,yend):
    move = str(translate(xstart))+str(ystart-1)+str(translate(xend))+str(yend-1)
    return move

def mat2algebric(l):
    l2 = []
    for el in l:
        s = "abcdefgh"
        a = s[int(el[0])]
        b = str(abs(el[1]-8))
        l2.append(a+b)
    return l2


class Piece():
    def __init__(self, color, x,y):
        self.color = color
        self.name = ""
        self.x = x
        self.y = y
    def is_valid_move(self,board,to, movePiece=True):
        self.moves = self.get_valid_moves(board)
        print("Move:", mat2algebric([to]))
        print("Moves:", mat2algebric(self.moves))
        if movePiece:
            if to in self.moves:
                self.x = to[0]
                self.y = to[1]
                return True
        
        return False
    
    def __repr__(self):
        return self.name

def get_ortogonal_moves(board, piece):
    moves = []
    for i in range(1, piece.x+1):
        if board.board[piece.x-i][piece.y]:
            if board.board[piece.x-i][piece.y].color == piece.color:
                break
            else:
                moves.append((piece.x-i,piece.y))
                break
        else:
            moves.append((piece.x-i,piece.y))
    for i in range(1, 7-piece.x+1):
        if board.board[piece.x+i][piece.y]:
            if board.board[piece.x+i][piece.y].color == piece.color:
                break
            else:
                moves.append((piece.x+i,piece.y))
                break
        else:
            moves.append((piece.x+i,piece.y))
    for i in range(1, piece.y+1):
        if board.board[piece.x][piece.y-i]:
            if board.board[piece.x][piece.y-i].color == piece.color:
                break
            else:
                moves.append((piece.x,piece.y-i))
                break
        else:
            moves.append((piece.x,piece.y-i))
    for i in range(1, 7-piece.y+1):
        if board.board[piece.x][piece.y+i]:
            if board.board[piece.x][piece.y+i].color == piece.color:
                break
            else:
                moves.append((piece.x,piece.y+i))
                break
        else:
            moves.append((piece.x,piece.y+i))
    return moves

def get_diagonal_moves(board, piece):
    moves = set()
    for i in range(1,8):
        x_,y_ = piece.x-i, piece.y-i
        if x_ <= 7 and y_ <= 7 and x_>=0 and y_>=0:
            if board.board[x_][y_]:
                if board.board[x_][y_].color == piece.color:
                    break
                else:
                    moves.add((x_,y_))
                    break
            else:
                moves.add((x_,y_))
    for i in range(1,8):
        x_,y_ = piece.x+i,piece.y+i
        if x_ <= 7 and y_ <= 7 and x_>=0 and y_>=0:
            if board.board[x_][y_]:
                if board.board[x_][y_].color == piece.color:
                    break
                else:
                    moves.add((x_,y_))
                    break
            else:
                moves.add((x_,y_))
    for i in range(1,8):
        x_,y_ = piece.x+i,piece.y-i
        if x_ <= 7 and y_ <= 7 and x_>=0 and y_>=0:
            if board.board[x_][y_]:
                if board.board[x_][y_].color == piece.color:
                    break
                else:
                    moves.add((x_,y_))
                    break
            else:
                moves.add((x_,y_))
    for i in range(1,8):
        x_,y_ = piece.x-i,piece.y+i
        if x_ <= 7 and y_ <= 7 and x_>=0 and y_>=0:
            if board.board[x_][y_]:
                if board.board[x_][y_].color == piece.color:
                    break
                else:
                    moves.add((x_,y_))
                    break
            else:
                moves.add((x_,y_))

    return list(moves)

class Rook(Piece):
    def __init__(self, color,x,y, first_move = True):
        super().__init__(color,x,y)
        self.name = "R"
        self.first_move = first_move 
        self.moves = []
        self.x = x
        self.y = y

    def get_valid_moves(self, board):
        moves = get_ortogonal_moves(board, self)
        return moves


class Bishop(Piece):
    def __init__(self, color, x,y, first_move = True):
        """
        Same as base class Piece, except `first_move` is used to check
        if this rook can castle.
        """
        super().__init__(color,x,y)
        self.name = "B"
        self.moves = []
        self.x = x
        self.y = y

    def get_valid_moves(self, board):
        moves = get_diagonal_moves(board, self)
        return moves

class Knight(Piece):
    def __init__(self, color,x,y, first_move = True):
        """
        Same as base class Piece, except `first_move` is used to check
        if this rook can castle.
        """
        super().__init__(color,x,y)
        self.name = "N"
        self.first_move = first_move 
        self.moves = []
        self.x = x
        self.y = y

    def get_valid_moves(self, board):
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
        candidate_moves = [
                (self.x + 2, self.y + 1),
                (self.x + 2, self.y - 1),
                (self.x - 2, self.y + 1),
                (self.x - 2, self.y - 1),
                (self.x + 1, self.y + 2),
                (self.x + 1, self.y - 2),
                (self.x - 1, self.y + 2),
                (self.x - 1, self.y - 2),
                ]
        moves = []
        for move in candidate_moves:
            if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                if board.board[move[0]][move[1]] != None:
                    if board.board[move[0]][move[1]].color != self.color:
                        moves.append(move)
                else:
                    moves.append(move)
        return moves
        
class Queen(Piece):
    def __init__(self, color, x,y,  first_move = True):
        super().__init__(color,x,y)
        self.name = "Q"
        self.first_move = first_move 
        self.moves = []
        self.x = x
        self.y = y

    def get_valid_moves(self, board):
        diag_moves = get_diagonal_moves(board, self)
        ortog_moves = get_ortogonal_moves(board, self)
        moves = set()
        for move in diag_moves+ortog_moves:
            moves.add(move)

        return moves

class Pawn(Piece):
    def __init__(self, color,x,y, first_move = True):
        super().__init__(color,x,y)
        self.name = "P"
        self.first_move = first_move 
        self.moves = []
        self.x = x
        self.y = y

    def get_valid_moves(self, board):
        ahead = 1 if self.color else -1
        candidate_moves = []
        if self.first_move:
            if board.board[self.x][self.y - ahead] == None:
                if board.board[self.x][self.y - (2*ahead)] == None:
                    candidate_moves.append((self.x, self.y - (2*ahead)))
            
        if 0 <= self.y-ahead <= 7:
            if board.board[self.x][self.y - ahead] == None:
                candidate_moves.append((self.x, self.y - ahead))
            if 0 <= self.x + 1 <= 7:
                if board.board[self.x + 1][self.y - ahead]:
                    if board.board[self.x + 1][self.y - ahead].color != self.color:
                        candidate_moves.append((self.x + 1, self.y - ahead))
                else:
                    # If there is no piece maybe there is ghostpawn
                    if board.ghostPawn:
                        if board.ghostPawn == (self.x + 1, self.y - ahead):
                            candidate_moves.append((self.x + 1, self.y - ahead))

            if 0 <= self.x - 1 <= 7:
                if board.board[self.x - 1][self.y - ahead]:
                    if board.board[self.x - 1][self.y - ahead].color != self.color:
                        candidate_moves.append((self.x - 1, self.y - ahead))
                else:
                    # If there is no piece maybe there is ghostpawn
                    if board.ghostPawn:
                        print(board.ghostPawn)
                        print(mat2algebric([board.ghostPawn]))
                        if board.ghostPawn == (self.x - 1, self.y - ahead):
                            candidate_moves.append((self.x - 1, self.y - ahead))
        candidate_moves2 = []
        self.moves = candidate_moves
        return self.moves


class King(Piece):
    def __init__(self, color, x, y, first_move = True):
        super().__init__(color, x, y)
        self.name = "K"
        self.first_move = first_move 
        self.moves = []
        self.x = x
        self.y = y



    def get_valid_moves(self, board):
        enemyMoves = board.getEnemyMoves(self.color)
        candidate_moves = [
                (self.x + 1 , self.y ),
                (self.x - 1 , self.y ),
                (self.x , self.y - 1 ),
                (self.x , self.y + 1 ),
                (self.x + 1 , self.y + 1 ),
                (self.x + 1 , self.y -1  ),
                (self.x - 1 , self.y -1 ),
                (self.x - 1 , self.y + 1 ),
                ]
        candidate_moves2 = []
        for move in candidate_moves:
            if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                if board.board[move[0]][move[1]]:
                    if board.board[move[0]][move[1]].color != self.color:
                        candidate_moves2.append(move)
                else:
                    candidate_moves2.append(move)
        if self.first_move:
            for rook in board.getRooks(self.color):
                if rook.first_move:
                    if rook.x == 0:
                        castleEnabled = True
                        for square in [(self.x-2,self.y),(self.x-1,self.y)]:
                            if not board.board[square[0]][square[1]]:
                                if square in enemyMoves:
                                    castleEnabled = False
                            else:
                                castleEnabled = False
                        if castleEnabled:
                            candidate_moves2.append((self.x-2,self.y))
                    if rook.x == 7:
                        castleEnabled = True
                        for square in [(self.x+1,self.y),(self.x+2,self.y)]:
                            if not board.board[square[0]][square[1]]:
                                if square in enemyMoves:
                                    castleEnabled = False
                            else:
                                castleEnabled = False
                        if castleEnabled:
                            candidate_moves2.append((self.x+2,self.y))
        self.moves = [move for move in candidate_moves2 if move not in enemyMoves]
        return self.moves

