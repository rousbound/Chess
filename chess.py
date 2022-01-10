import board
import piece
import utils
import random
import time
import re
import sys
            
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

    gameRunning : bool
        True if none of draw or win conditions are met.

    movesList : list[str]
        Record of game moves in uci format


    Methods:
    --------

    move(move:str, start:tup, to:tup, promotion:str) -> None
        Make move

    getLegalMoves() -> list[tup]
        Check legal moves

    checkMaterialDraw() -> None
        Check for material-criteria draws

    checkMoveGrammar(uci_move:str) -> start:str, to:str, promotion:str
        Check grammar of move input by user

    uci2indices(start:str, end:str) -> list[tup]
        Convert uci2indices
        Ex: "e2" "e4" -> [(4,6),(4,4)]

    getMoveRandom(moves:list[str])-> uci_move:str, index_start:tup, index_to:tup, promotion:str
        Get random moves based on legal moves avaiable
    getMovePlayer(moves:list[str])-> uci_move:str, index_start:tup, index_to:tup, promotion:str
        Ask the user for input and check if it is legal move
    main() -> None
        Execute Game

    """

    def __init__(self):
        self.board = board.Board()
        self.turn = True
        self.gameRunning = True
        self.movesList = []



    def move(self, move, start, to, promotion):
        """
        Moves a piece at `start` to `to`. 

        move: str
            Requested move
            Ex: "e2e4"

        start : tup
            Index of the piece to be moved
            Ex: (1,2)

        to : tup
            Index of target square
            Ex: (2,4)
        """

        target_piece = self.board.board[start[0]][start[1]]
        # Remove first_move from pieces
        if target_piece.name in ["P","R","K"]:
            target_piece.first_move = False

        if target_piece.name == "P":
            # This move was pawn double movement
            if abs(to[1]-start[1]) > 1:
                self.board.activateGhostPawn((target_piece.x,target_piece.y), self.turn)
            else:
                # Capture happened, detect if was En Passeant and delete captured pawn
                if abs(to[0]-start[0]) == 1 and abs(to[1]-start[1]) == 1:
                    if self.board.board[to[0]][to[1]] == None:
                        if to == self.board.ghostPawn(self.turn):
                            if target_piece.color:
                                self.board.board[to[0]][to[1]+1] = None
                            else:
                                self.board.board[to[0]][to[1]-1] = None
            # Promotion logic
            if promotion:
                if target_piece.color and to[1] == 0:
                    color = True
                elif not target_piece.color and to[1] == 7:
                    color = False
                if promotion == "q":
                    promoted_piece = piece.Queen(color,target_piece.x,target_piece.y)
                elif promotion == "r":
                    promoted_piece = piece.Rook(color,target_piece.x,target_piece.y, first_move=False)
                elif promotion == "b":
                    promoted_piece = piece.Bishop(color,target_piece.x,target_piece.y)
                elif promotion == "n":
                    promoted_piece = piece.Knight(color,target_piece.x,target_piece.y)
                target_piece = promoted_piece
        # Castling logic
        if target_piece.name == "K":
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


        enemyKing = self.board.getKingPiece(not self.turn)
        pieceMoves = target_piece.get_valid_moves(self.board)
        if (enemyKing.x,enemyKing.y) in pieceMoves:
            print("CHECK!!")

        self.turn = not self.turn
        self.board.deactivateGhostPawn(self.turn)
        target_piece.move(to, self.board)
        self.movesList.append(move)
        print(" ".join(self.movesList))


    def getLegalMoves(self):
        legalMoves = []
        for i in range(8):
            for j in range(8):
                piece = self.board.board[i][j]
                if piece:
                    if piece.color == self.turn:
                        piece_targets = piece.get_valid_moves(self.board)
                        for target in piece_targets:
                            origin = (piece.x,piece.y)
                            # Play move
                            captured_piece = piece.move(target,self.board)

                            enemyControlledSquares = self.board.getEnemyControlledSquares(self.turn)
                            friendKing = self.board.getKingPiece(self.turn)
                            # If king not in enemy controlled square after move, is legal move
                            if (friendKing.x,friendKing.y) not in enemyControlledSquares:
                                uci_move = "".join(utils.mat2uci([origin,target]))
                                # Check for promotion pawns
                                if piece.name == "P":
                                    lastrow = 0 if piece.color else 7
                                    if target[1] == lastrow:
                                        promotion = ["q","r","n","b"]
                                        for p in promotion:
                                            legalMoves.append(uci_move + p)
                                    else:
                                        legalMoves.append(uci_move)
                                else:
                                    legalMoves.append(uci_move)
                            # Undo move
                            piece.move(origin,self.board)
                            if captured_piece:
                                captured_piece.move(target,self.board)


        friendKing = self.board.getKingPiece(self.turn)
        enemyControlledSquares = self.board.getEnemyControlledSquares(self.turn)
        # If there is no legal moves while not in check,
        # there is stalemate, otherwise, checkmate
        if len(legalMoves) == 0:
            if (friendKing.x,friendKing.y) not in enemyControlledSquares:
                self.gameRunning = False
                print("DRAW -- Stalemate")
            else:
                self.gameRunning = False
                print("CHECKMATE!!!!")
                if self.turn:
                    print("BLACK WINS!!!")
                else:
                    print("WHITE WINS!!!")
        self.checkMaterialDraw()
        return legalMoves

    def checkMaterialDraw(self):
        piecesLeft = []
        for piece in self.board.vector():
            if piece:
                if piece.name != "K":
                    piecesLeft.append(piece)
        if not piecesLeft:
            self.gameRunning = False
            print("DRAW -- Only kings left")
        if len(piecesLeft) == 1:
            piece = piecesLeft[0]
            if piece.name == "B":
                print("DRAW -- King and Bishop cannot checkmate")
            if piece.name == "N":
                print("DRAW -- King and Knight cannot checkmate")
        if len(piecesLeft) == 2:
            piece1 = piecesLeft[0]
            piece2 = piecesLeft[1]
            if piece1.color != piece2.color:
                if piece1.name == "B" and piece1.name == "B":
                    print("DRAW -- King and Bishop vs King and Bishop cannot checkmate")
                elif piece1.name == "B" and piece1.name == "N":
                    print("DRAW -- King and Bishop vs King and Knight cannot checkmate")
                elif piece1.name == "N" and piece1.name == "B":
                    print("DRAW -- King and Knight vs King and Bishop cannot checkmate")

                # Although having two Knights does not imply forced checkmate, 
                # it is possible if your opponent doesn't do the right moves





    def checkMoveGrammar(self, uci_move):
        match = re.match("([abcdefgh][12345678])([abcdefgh][12345678])([qbnr]?)", uci_move)
        if not match:
            print(uci_move + " is not in the format '[a-h][1-8][a-h][1-8]([qbnr])'")
            return None, None, None
        start = match.group(1)
        end = match.group(2)
        promotion = match.group(3)
        return start, end, promotion



    def getMovePlayer(self, moves):
            uci_move = input("Move: ")
            uci_start, uci_to, promotion = self.checkMoveGrammar(uci_move)
            index_start, index_to = utils.uci2indices(uci_start, uci_to)
            if uci_move in moves:
                return uci_move, index_start, index_to, promotion
            return None, None, None, None



    def getMoveRandom(self, moves):
            uci_move = None
            if len(moves) > 0:
                r = random.randint(0,len(moves)-1)
                uci_move = moves[r]
            uci_start, uci_to, promotion = self.checkMoveGrammar(uci_move)
            index_start, index_to = utils.uci2indices(uci_start, uci_to)
            if uci_move in moves:
                return uci_move, index_start, index_to, promotion
            return None, None, None, None


    def main(self):

        if sys.argv[1] == "-p":
            getMove = self.getMovePlayer
        elif sys.argv[1] == "-r":
            getMove = self.getMoveRandom
        while chess.gameRunning:
            player_turn = "White" if self.turn else "Black"
            print(f"{player_turn}'s turn to move!")
            self.board.print_board()
            moves = self.getLegalMoves()
            uci_move, index_start, index_to, promotion = getMove(moves)

            if not self.gameRunning:
                break

            if not uci_move:
                print("Illegal or impossible move")
                continue

            self.move(uci_move, index_start, index_to, promotion)


if __name__ == "__main__":
    chess = Chess()
    chess.main()



