import board
import piece
import utils
import random
import time
            
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
        self.checkmate = False
        self.movesList = []



    def move(self, start, to, promotion, move):
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
        print("Target piece:", target_piece)
        if self.turn != target_piece.color:
            print("That's not your piece to move")
            return

        end_piece = self.board.board[to[0]][to[1]]
        is_end_piece = end_piece != None

        # Checks if a player's own piece is at the `to` coordinate
        if is_end_piece and self.board.board[start[0]][start[1]].color == end_piece.color:
            print("There's a piece in the end location.")
            return

        legalMoves = self.getMoves(self.turn, self.board)


        print(legalMoves)




        if target_piece.is_valid_move(self.board, to):
            # Make move and check if friend King is in enemy attacking squares after requested move.
            original_piece = self.board.board[to[0]][to[1]]
            self.board.board[to[0]][to[1]] = target_piece
            self.board.board[start[0]][start[1]] = None
            enemyMoves = self.board.getEnemyControlledSquares(self.turn)
            friendKing = self.getKingPiece(self.turn)
            # If in check, undo move
            if (friendKing.x,friendKing.y) in enemyMoves:
                print("King in check, please make other move")
                self.board.board[to[0]][to[1]] = original_piece
                self.board.board[start[0]][start[1]] = target_piece
            else:
                # Check Pawn specific logic, in order, En Passeant and Promotion
                if target_piece.name in ["P","R","K"]:
                    target_piece.first_move = False
                    if target_piece.name == "P":
                        # En passeant logic
                        if abs(to[1]-start[1]) > 1:
                            print("Ghost pawn created")
                            if target_piece.color:
                                self.board.ghostPawn = (target_piece.x,target_piece.y+1)
                            else:
                                self.board.ghostPawn = (target_piece.x,target_piece.y-1)
                        else:
                            if abs(to[0]-start[0]) == 1 and abs(to[1]-start[1]) == 1:
                                # This move was En passeant
                                if target_piece.color:
                                    self.board.board[target_piece.x][target_piece.y+1] = None
                                else:
                                    self.board.board[target_piece.x][target_piece.y-1] = None
                        # Promotion logic
                        if promotion:
                            print("Promotion")
                            color = None
                            if target_piece.color and target_piece.y == 0:
                                color = True
                            elif not target_piece.color and target_piece.y == 7:
                                color = False
                            if color == None:
                                print("No Pawn can be promoted")
                            else:
                                if promotion == "q":
                                    promoted_piece = piece.Queen(color,target_piece.x,target_piece.y)
                                elif promotion == "r":
                                    promoted_piece = piece.Rook(color,target_piece.x,target_piece.y, first_move=False)
                                elif promotion == "b":
                                    promoted_piece = piece.Bishop(color,target_piece.x,target_piece.y)
                                elif promotion == "n":
                                    promoted_piece = piece.Knight(color,target_piece.x,target_piece.y)
                                self.board.board[target_piece.x][target_piece.y] = promoted_piece
                    # Castling logic
                    if target_piece.name == "K":
                        # Castling logic
                        if to[0]-start[0] > 1:
                            if target_piece.color:
                                rook = self.board.board[7][7] 
                                rook.x = 5
                                self.board.board[7][7] = None
                                self.board.board[5][7] = rook
                            else:
                                rook = self.board.board[0][0] 
                                rook.x = 5
                                self.board.board[0][0] = None
                                self.board.board[5][0] = rook

                        elif to[0]-start[0] < -1:
                            if target_piece.color:
                                rook = self.board.board[0][7] 
                                rook.x = 3
                                self.board.board[0][7] = None
                                self.board.board[3][7] = rook
                            else:
                                rook = self.board.board[0][0] 
                                rook.x = 3
                                self.board.board[0][0] = None
                                self.board.board[3][0] = rook


                enemyKing = self.getKingPiece(not target_piece.color)
                pieceMoves = target_piece.get_valid_moves(self.board)
                if (enemyKing.x,enemyKing.y) in pieceMoves:
                    print("CHECK!!")

                self.turn = not self.turn
                self.board.ghostPawn = None
                target_piece.move(to)
                self.movesList.append(move)

    def getKingPiece(self, color):
        for i in range(8):
            for j in range(8):
                if self.board.board[i][j]:
                    if self.board.board[i][j].name == "K":
                        if self.board.board[i][j].color == color:
                            return self.board.board[i][j]

    def getMoves(self, color, board):
        legalMoves = []
        for i in range(8):
            for j in range(8):
                piece = board.board[i][j]
                if piece:
                    if piece.color == color:
                        piece_targets = piece.get_valid_moves(self.board)
                        for target in piece_targets:
                            # legalMoves.append(uci_move)
                            origin = (piece.x,piece.y)
                            # uci_move = "".join(utils.mat2algebric([origin,target]))
                            legalMoves.append(uci_move)
        for move in legalMoves:
            # Play move
            start,to,promotion = translate(move)
            start_piece = board.board[start[[0]][start[1]]
            end_piece = board.board[to[0]][to[1]] 
            board.board[to[0]][to[1]] = start_piece
            board.board[start[0]][start[1]] = None

            enemyControlledSquares = board.getEnemyControlledSquares(self.turn)
            friendKing = self.getKingPiece(self.turn)
            # if piece.name == "K":
                # print(utils.mat2algebric([(friendKing.x,friendKing.y)]))
                # print(utils.mat2algebric(enemyControlledSquares))
            # If king not in enemy controlled square after move, is legal move
            if (friendKing.x,friendKing.y) in enemyControlledSquares:
                # uci_move = "".join(utils.mat2algebric([origin,target]))
                # legalMoves.append(uci_move)
                # If has at least one legal move, not checkmate
                # checkmate = False
                legalMoves.remove(move)
            # Undo move
            board.board[to[0]][to[1]] = end_piece
            board.board[start[0]][start[1]] = start_piece
        if len(legalMoves) == 0:
            self.checkmate = True
            print("CHECKMATE!!!!")
            if self.turn:
                print("BLACK WINS!!!")
            else:
                print("WHITE WINS!!!")
            print("\\n".join(self.movesList))
        return legalMoves
        # return legalMoves
        # checkmate = True
        # for move in possibleMoves:
            # _start, _to, _promotion = translate(move)
            # #print("_Start,_to:",utils.mat2algebric([_start,_to]))
            # start_piece = board.board[_start[0]][_start[1]]
            # end_piece = board.board[_to[0]][_to[1]] 

            # self.board.board[_to[0]][_to[1]] = start_piece
            # self.board.board[_start[0]][_start[1]] = None

            # enemyControlledSquares = board.getEnemyControlledSquares(self.turn)
            # friendKing = self.getKingPiece(self.turn)
            # # print("FriendKing:", utils.mat2algebric([(friendKing.x, friendKing.y)]))
            # if (friendKing.x,friendKing.y) in enemyControlledSquares:
                # # In this move the king can be captured
                # #print("ENEMYMOVES:",utils.mat2algebric(enemyControlledSquares))
                # print("FriendKing:",(friendKing.x,friendKing.y))
                # print(enemyControlledSquares)
                # board.board[_to[0]][_to[1]] = end_piece
                # board.board[_start[0]][_start[1]] = start_piece
            # else:
                # # There is a move that doesn't put the king in check
                # # print("There is a move to save from checkmate")
                # board.board[_to[0]][_to[1]] = end_piece
                # board.board[_start[0]][_start[1]] = start_piece
                # legalMoves.append(move)
                # checkmate = False
        # if checkmate:
            # self.checkmate = True
            # print("CHECKMATE!!!!")
            # if self.turn:
                # print("BLACK WINS!!!")
            # else:
                # print("WHITE WINS!!!")
        # return legalMoves



def translate(s):
    """
    Translates traditional board coordinates of chess into list indices
    """
    start = s[0:2] 
    end = s[2:4]
    promotion = None
    if len(s) == 5:
        promotion = s[4]
    coords = [start,end]
    r = []
    for coord in coords:
        try:
            row = abs(int(coord[1])-8) # Y: Number
            col = coord[0] # X: Letter
            if row < 0 or row > 8:
                print(coord[1] + " is not in the range from 1 - 8")
                return None
            if col < 'a' or col > 'h':
                print(coord[0] + " is not in the range from a - h")
                return None
            dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
            r.append((dict[col],row))
        except:
            print(s + "is not in the format '[number][letter]'")
            return None, None
    r.append(promotion)
    return r




if __name__ == "__main__":
    chess = Chess()
    chess.board.print_board()
    import sys

    if sys.argv[1] == "-p":
        while not chess.checkmate:
            move = input("Move: ")
            
            print("Requested move:", move)
            start, to, promotion = translate(move)
            moves = chess.getMoves(chess.turn, chess.board)
            print("EnemyControlledSquares:",utils.mat2algebric(chess.board.getEnemyControlledSquares(chess.turn)))
            print("Legal Moves:", moves)
            if not moves:
                break

            if start == None or to == None:
                continue

            chess.move(start, to, promotion, move)

            chess.board.print_board()
    elif sys.argv[1] == "-r":
        while not chess.checkmate:
            # time.sleep(0.3)
            moves = chess.getMoves(chess.turn, chess.board)
            print("EnemyControlledSquares:",board.getEnemyControlledSquares(self.turn))
            print("Legal Moves:", moves)
            if not moves:
                break
            
            r = random.randint(0,len(moves)-1)
            print(r)

            move = moves[r]

            print("UCI move:",move)
            start, to, promotion = translate(move)
            print("Start:", start)
            print("To:", to)

            if start == None or to == None:
                continue

            chess.move(start, to, promotion, move)

            player_turn = "White" if chess.turn else "Black"
            print(f"{player_turn}'s turn to move!")
            chess.board.print_board()
