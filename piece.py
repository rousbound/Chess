def translate(n):
    s = "abcdefgh"
    return s[int(n)]

def translateMoves(xstart,ystart,xend,yend):
    return str(translate(xstart))+str(ystart)+str(translate(xend))+str(yend)


class Piece():
    def __init__(self, color):
        self.color = color
        self.name = ""
        self.x = 0
        self.y = 0
    def is_valid_move(self,board,to):
        self.get_valid_moves(board)
        if translateMoves(self.x,self.y,to[0],to[1]) in self.moves:
            return True
        return False
    
    def __repr__(self):
        return self.name

def get_ortogonal_moves(board, piece):
    moves = []
    for i in range(0, piece.y):
        if board[i][piece.y].color == piece.color:
            break
        else:
            moves.append(translateMoves(piece.x,piece.y,i,piece.y))
    for i in range(piece.x, 7):
        if board[i][piece.y].color == piece.color:
            break
        else:
            moves.append(translateMoves(piece.x,piece.y,i,piece.y))
    for i in range(0, piece.y):
        if board[piece.x][i] == piece.color:
            break
        else:
            moves.append(translateMoves(piece.x,piece.y,piece.x,i))
    for i in range(piece.x, 7):
        if board[piece.x][i] == piece.color:
            break
        else:
            moves.append(translateMoves(piece.x,piece.y,piece.x,i))

def get_diagonal_moves(board, piece):
    moves = []
    for i in range(8):
        x_,y_ = piece.x-i, piece.y-i
        if x_ <= 7 and y_ <= 7:
            if board[x_][y_] == piece.color:
                break
            else:
                moves.append(translateMoves(piece.x,piece.y,x_,y_))
        break
    for i in range(8):
        x_,y_ = piece.x+i,piece.y+i
        if x_ <= 7 and y_ >= 0:
            if board[x_][y_] == piece.color:
                break
            else:
                moves.append(translateMoves(piece.x,piece.y,x_,y_))
        break
    for i in range(8):
        x_,y_ = piece.x+i,piece.y-i
        if x_ <= 7 and y_ >= 0:
            if board[x_][y_] == piece.color:
                break
            else:
                moves.append(translateMoves(piece.x,piece.y,x_,y_))
        break
    for i in range(8):
        x_,y_ = piece.x-i,piece.y+i
        if x_ >= 0 and y_ <= 7:
            if board[x_][y_] == piece.color:
                break
            else:
                moves.append(translateMoves(piece.x,piece.y,x_,y_))
        break

class Rook(Piece):
    def __init__(self, color, first_move = True):
        super().__init__(color)
        self.name = "R"
        self.first_move = first_move 
        self.moves = []

    def get_valid_moves(self, board):
        self.moves = get_ortogonal_moves(board, self)


class Bishop(Piece):
    def __init__(self, color, first_move = True):
        """
        Same as base class Piece, except `first_move` is used to check
        if this rook can castle.
        """
        super().__init__(color)
        self.name = "B"
        self.first_move = first_move 
        self.moves = []
        self.x = 0
        self.y = 0

    def get_valid_moves(self, board):
        self.moves = get_diagonal_moves(board, self)

class Knight(Piece):
    def __init__(self, color, first_move = True):
        """
        Same as base class Piece, except `first_move` is used to check
        if this rook can castle.
        """
        super().__init__(color)
        self.name = "N"
        self.first_move = first_move 
        self.moves = []
        self.x = 0
        self.y = 0

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
                [self.x + 2, self.y + 1],
                [self.x + 2, self.y - 1],
                [self.x - 2, self.y + 1],
                [self.x - 2, self.y - 1],
                [self.x + 1, self.y + 2],
                [self.x + 1, self.y - 2],
                [self.x - 1, self.y + 2],
                [self.x - 1, self.y - 2],
                ]
        self.moves = []
        for move in candidate_moves:
            if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                self.moves.append(translateMoves(self.x,self.y,move[0],move[1]))
        
class Queen(Piece):
    def __init__(self, color, first_move = True):
        super().__init__(color)
        self.name = "Q"
        self.first_move = first_move 
        self.moves = []
        self.x = 0
        self.y = 0

    def get_valid_moves(self, board):
        diag_moves = get_diagonal_moves(board, self)
        ortog_moves = get_ortogonal_moves(board, self)
        self.moves = diag_moves + ortog_moves

class Pawn(Piece):
    def __init__(self, color, first_move = True):
        super().__init__(color)
        self.name = "P"
        self.first_move = first_move 
        self.moves = []
        self.x = 0
        self.y = 0

    def get_valid_moves(self, board):
        ahead = 1 if self.color else -1
        candidate_moves = []
        if self.first_move:
            print(board.board[self.x][self.y + ahead])
            if board.board[self.x][self.y + ahead] == None:
                print("None")
                if board.board[self.x][self.y + (2*ahead)] == None:
                    print("En passent enabled")
                    candidate_moves += [self.x, self.y + (2*ahead)]
            
        if board.board[self.x][self.y + ahead] != None:
            candidate_moves.append([self.x, self.y + ahead])
        if board.board[self.x + 1][self.y + ahead].color != self.color:
            candidate_moves.append([self.x + 1, self.y + ahead])
        if board.board[self.x - 1][self.y + ahead].color != self.color:
            candidate_moves.append([self.x - 1, self.y + ahead])
        self.moves = candidate_moves
        print(self.moves)


class King(Piece):
    def __init__(self, color, first_move = True):
        super().__init__(color)
        self.name = "K"
        self.first_move = first_move 
        self.moves = []
        self.x = 0
        self.y = 0

    def get_valid_moves(self, board):
        candidate_moves = [
                [self.x + 1 , self.y ],
                [self.x + 1 , self.y -1  ],
                [self.x + 1 , self.y + 1 ],
                [self.x - 1 , self.y ],
                [self.x - 1 , self.y -1 ],
                [self.x - 1 , self.y + 1 ],
                [self.x , self.y - 1 ],
                [self.x , self.y + 1 ],
                [self.x , self.y ]
                ]

        # Filter squares that have friendly pieces on them
        candidate_moves = [ el for el in candidate_moves if board[el[0]][el[1]].color != self.color] 
        # Filter moves if enemy pieces attacking them
        self.moves = [ translateMoves(self.x,self.y,el[0],el[1]) for el in candidate_moves]
