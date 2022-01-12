import board
import piece
import utils
import random
import time
import re
import sys
import copy
            
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

    legalMoves : list[str]
        List of current legal moves

    movesWithoutCaptures : int
        Counter of moves without captures, relevant for draw criteria


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
        self.legalMoves = []
        self.movesWithoutCaptures = 0
        self.boardStates = []



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
                self.board.activateGhostPawn(target_piece.get_pos(), target_piece.color)
            else:
                # Capture happened, detect if was En Passeant and delete captured pawn
                if abs(to[0]-start[0]) == 1 and abs(to[1]-start[1]) == 1:
                    if self.board.board[to[0]][to[1]] == None:
                        if to == self.board.getGhostPawn(not self.turn):
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
            # RightCastling
            if to[0]-start[0] > 1:
                if target_piece.color:
                    rook = self.board.board[7][7] 
                    rook.move((5,7), self.board)
                else:
                    rook = self.board.board[7][0] 
                    rook.move((5,0), self.board)

            # LeftCastling
            elif to[0]-start[0] < -1:
                if target_piece.color:
                    rook = self.board.board[0][7] 
                    rook.move((3,7), self.board)
                else:
                    rook = self.board.board[0][0] 
                    rook.move((3,0), self.board)



        self.turn = not self.turn
        captured_piece = target_piece.move(to, self.board)
        if captured_piece:
            self.movesWithoutCaptures = 0
        else:
            self.movesWithoutCaptures += 1
        self.movesList.append(move)
        # print(" ".join(self.movesList))


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

                            enemyControlledSquares = self.board.getControlledSquares(not self.turn)
                            friendKing = self.board.getKingPiece(self.turn)
                            # If king not in enemy controlled square after move, is legal move
                            # KINGINCHECK
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
        enemyControlledSquares = self.board.getControlledSquares(not self.turn)
        # If there is no legal moves while not in check,
        # there is stalemate, otherwise, checkmate
        if self.movesWithoutCaptures == 50:
            # print("DRAW -- 50 moves without captures")
            self.gameRunning = False
            pass
        if len(legalMoves) == 0:
            if (friendKing.x,friendKing.y) not in enemyControlledSquares:
                self.gameRunning = False
                # print("DRAW -- Stalemate")
            else:
                self.gameRunning = False
                # print("CHECKMATE!!!!")
                if self.turn:
                    # print("BLACK WINS!!!")
                    pass
                else:
                    # print("WHITE WINS!!!")
                    pass
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
            # print("DRAW -- Only kings left")
        if len(piecesLeft) == 1:
            piece = piecesLeft[0]
            if piece.name == "B":
                # print("DRAW -- King and Bishop cannot checkmate")
                self.gameRunning = False
            if piece.name == "N":
                # print("DRAW -- King and Knight cannot checkmate")
                self.gameRunning = False
        if len(piecesLeft) == 2:
            piece1 = piecesLeft[0]
            piece2 = piecesLeft[1]
            if piece1.color != piece2.color:
                if piece1.name == "B" and piece1.name == "B":
                    # print("DRAW -- King and Bishop vs King and Bishop cannot checkmate")
                    self.gameRunning = False
                elif piece1.name == "B" and piece1.name == "N":
                    # print("DRAW -- King and Bishop vs King and Knight cannot checkmate")
                    self.gameRunning = False
                elif piece1.name == "N" and piece1.name == "B":
                    # print("DRAW -- King and Knight vs King and Bishop cannot checkmate")
                    self.gameRunning = False

                # Although having two Knights does not imply forced checkmate, 
                # it is possible if your opponent doesn't do the right moves





    def checkMoveGrammar(self, uci_move):
        match = re.match(r"([a-h][1-8])([a-h][1-8])([qbnr]?)", uci_move)
        if not match:
            print(uci_move + " is not in the format '[a-h][1-8][a-h][1-8]([qbnr])'")
            return False
        else:
            return match


    def getMovePlayer(self):
        """
        Asks the user a move in the format '[a-h][1-8][a-h][1-8][qbnr]?'

        """
        try:
            uci_move = input("Move: ")
            if self.checkMoveGrammar(uci_move):
                return uci_move
        except:
            return "EOF"
            print("EOF")

    def getMoveCLIGUI(self):
        """
        Asks the user a move in the format '[a-h][1-8][a-h][1-8][qbnr]?'

        """
        uci_move = input("Move: ")
        if self.checkMoveGrammar(uci_move):
            return uci_move


    def getMoveRandom(self):
        uci_move = None
        r = random.randint(0,len(self.legalMoves)-1)
        uci_move = self.legalMoves[r]
        return uci_move


    def moveGenerationTest(self, depth):
        if depth == 0:
            return 1
        self.legalMoves = self.getLegalMoves()
        counter = 0
        for uci_move in self.legalMoves:
            # Make move
            index_start, index_to, promotion = utils.splitUci2indices(uci_move)
            board = copy.deepcopy(self.board)
            self.move(uci_move, index_start, index_to, promotion)

            counter += self.moveGenerationTest(depth-1)

            # Undo move

            self.turn = not self.turn
            self.board = board
        return counter

    def kingsInCheck(self):
        for color in [True, False]:
            King = self.board.getKingPiece(color)
            controlledSquares = self.board.getControlledSquares(not color)
            
            if (King.x,King.y) in controlledSquares:
                King.inCheck = True
            else:
                King.inCheck = False



    def main(self):

        arg = sys.argv[1]

        if arg == "-cli":
            getMove = self.getMovePlayer
        elif arg == "-r":
            getMove = self.getMoveRandom
        elif arg == "-cligui":
            import GUI
            gui = GUI.GUI(self.board,640,640,self)
            getMove = self.getMovePlayer

            while chess.gameRunning:
                player_turn = "White" if self.turn else "Black"
                print(f"{player_turn}'s turn to move!")
                self.board.print_board()
                gui.mainUnplayable(0.3)
                self.legalMoves = self.getLegalMoves()
                print("LegalMoves:", self.legalMoves)
                uci_move = getMove()
                print("Move:", uci_move)
                if uci_move in self.legalMoves:
                    index_start, index_to, promotion = utils.splitUci2indices(uci_move)
                else:
                    print("Illegal or impossible move")
                    continue

                if not self.gameRunning:
                    break

                self.move(uci_move, index_start, index_to, promotion)


        if arg == "-cli" or arg == "-r":

            while chess.gameRunning:
                player_turn = "White" if self.turn else "Black"
                print(f"{player_turn}'s turn to move!")
                self.board.print_board()
                self.legalMoves = self.getLegalMoves()
                print("LegalMoves:", self.legalMoves)
                uci_move = getMove()
                if uci_move in self.legalMoves:
                    index_start, index_to, promotion = utils.splitUci2indices(uci_move)
                elif uci_move == "EOF":
                    break
                else:
                    print("Illegal or impossible move")
                    continue

                if not chess.gameRunning:
                    break


                self.move(uci_move, index_start, index_to, promotion)
        if arg == "-gui":
            import GUI
            gui = GUI.GUI(self.board,640,640,self)
            gui.main()


        elif arg == "-b":
            depth = sys.argv[2]
            print(f"Initiating move generation test on depth: {depth}")
            l = []
            for i in range(1,int(depth)+1):
                result = self.moveGenerationTest(i)
                l.append(result)
                print(f"Result of possible games with {i} ply:",result)

            

if __name__ == "__main__":
    chess = Chess()
    chess.main()





