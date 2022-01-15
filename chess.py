import board
import piece
import utils
import random
import time
import re
import sys
import copy
import logging

            
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

    movesWithoutCapturesOrPawnMovements : int
        Counter of moves without captures, or pawn movements relevant for draw criteria


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

    def __init__(self, board : object):
        self.board = board
        self.turn = True
        self.gameRunning = True
        self.movesList = []
        self.legalMoves = []
        self.movesWithoutCapturesOrPawnMovements = 0
        self.boardStates = {True: [], False: []}
        self.castlingRights = [True, True]



    def playMove(self, move):
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
        start = move[0]
        to = move[1]

        selected_piece = self.board[start]

        if selected_piece.name == "P":
            # Double pawn movement logic
            if abs(to[1]-start[1]) > 1:
                self.board.activateGhostPawn(selected_piece.get_pos(), selected_piece.color)
        
            if move == selected_piece.canEnPasseant:
                if to == self.board.getGhostPawn(not self.turn):
                    if selected_piece.color:
                        self.board[to[0],to[1]+1] = None
                    else:
                        self.board[to[0],to[1]-1] = None
            if str(move[2]) in "qrbn":
                promotion = move[2]
                print("promotion")
                color = selected_piece.color
                if promotion == "q":
                    promoted_piece = piece.Queen(color, selected_piece.x, selected_piece.y)
                elif promotion == "r":
                    promoted_piece = piece.Rook(color, selected_piece.x, selected_piece.y, first_move=False)
                elif promotion == "b":
                    promoted_piece = piece.Bishop(color, selected_piece.x, selected_piece.y)
                elif promotion == "n":
                    promoted_piece = piece.Knight(color, selected_piece.x, selected_piece.y)
                selected_piece = promoted_piece
            self.movesWithoutCapturesOrPawnMovements = 0

        # Castling logic

        if selected_piece.name == "K":
            if move in selected_piece.canCastle:
                if selected_piece.color:
                    rook = self.board[7,7] 
                    rook.move((5,7), self.board)
                else:
                    rook = self.board[7,0] 
                    rook.move((5,0), self.board)

            # LeftCastling
            if move in selected_piece.canCastle:
                if selected_piece.color:
                    rook = self.board[0,7] 
                    rook.move((3,7), self.board)
                else:
                    rook = self.board[0,0] 
                    rook.move((3,0), self.board)

            # After castle, a position can't be repeated
            if selected_piece.first_move == True:
                self.boardStates[self.turn] = []
                self.boardStates[not self.turn] = []


        captured_piece = selected_piece.move(to, self.board)
        if captured_piece:
            self.movesWithoutCapturesOrPawnMovements = 0
        else:
            self.movesWithoutCapturesOrPawnMovements += 1
        self.movesList.append(move)
        self.boardStates[self.turn].append(copy.deepcopy(self.board))
        self.turn = not self.turn
        self.board.turn = not self.board.turn

        # Remove first_move from pieces
        if selected_piece.name in ["P","R","K"]:
            selected_piece.first_move = False

    def checkThreeFoldRepetition(self):
        for color, boardStates in self.boardStates.items():
            boardStatesCounter = {}
            for board in boardStates[-6:]:
                if board in boardStatesCounter.keys():
                    boardStatesCounter[board] += 1
                else:
                    boardStatesCounter[board] = 1
            for key, val in boardStatesCounter.items():
                if val >= 3:
                    self.gameRunning = False
                    print("DRAW -- Three fold repetition")
                    pass




    def getLegalMoves(self):
        """
        Iterate through all pieces of turn color and get it's valid moves. 
        Then simulate the move and check if King ends in check.
        If not, it is legal move.
        After check Draw conditions
        """

        legalMoves = []
        for i in range(8):
            for j in range(8):
                piece = self.board[i,j]
                if piece:
                    if piece.color == self.turn:
                        piece_moves = piece.get_valid_moves(self.board)
                        # Simulate moves to see if it ends up with king in check
                        for move in piece_moves:
                            origin = move[0]
                            target = move[1]
                            # Do move
                            captured_piece = piece.move(target,self.board)

                            enemyTargets = self.board.getControlledSquares(not self.turn)
                            friendKing = self.board.getKingPiece(self.turn)

                            # If king not in enemy targets after move, is legal move
                            if friendKing.get_pos() not in enemyTargets:
                                legalMoves.append(move)

                            # Undo move
                            piece.move(origin,self.board)
                            if captured_piece:
                                captured_piece.move(target,self.board)

        return legalMoves
    
    def checkEndgameConditions(self):
        # Check if game has met checkmate or draw criteria
        if self.movesWithoutCapturesOrPawnMovements == 50:
            print("DRAW -- 50 moves without captures or pawn movements")
            self.gameRunning = False
            pass

        friendKing = self.board.getKingPiece(self.turn)
        enemyTargets = self.board.getControlledSquares(not self.turn)

        # If there is no legal moves while not in check,
        # there is stalemate, otherwise, checkmate
        if len(self.legalMoves) == 0:
            # Not in Check
            if (friendKing.x,friendKing.y) not in enemyTargets:
                self.gameRunning = False
                print("DRAW -- Stalemate")
            # In Check
            else:
                self.gameRunning = False
                print("CHECKMATE!!!!")
                if self.turn:
                    print("BLACK WINS!!!")
                else:
                    print("WHITE WINS!!!")

        # Check Insufficient material draw
        self.checkMaterialDraw()
        # self.checkThreeFoldRepetition()


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
                self.gameRunning = False
            if piece.name == "N":
                print("DRAW -- King and Knight cannot checkmate")
                self.gameRunning = False
        if len(piecesLeft) == 2:
            piece1 = piecesLeft[0]
            piece2 = piecesLeft[1]
            if piece1.color != piece2.color:
                if piece1.name == "B" and piece1.name == "B":
                    print("DRAW -- King and Bishop vs King and Bishop cannot checkmate")
                    self.gameRunning = False
                elif piece1.name == "B" and piece1.name == "N":
                    print("DRAW -- King and Bishop vs King and Knight cannot checkmate")
                    self.gameRunning = False
                elif piece1.name == "N" and piece1.name == "B":
                    print("DRAW -- King and Knight vs King and Bishop cannot checkmate")
                    self.gameRunning = False

                # OBS:
                # Although having two Knights does not imply forced checkmate, 
                # it is possible if your opponent doesn't defend with the right moves



    def uci2move(self, uci_move):
        match = re.match(r"([a-h][1-8])([a-h][1-8])([qbnr]?)", uci_move)
        """
        1. Check move grammar and
        2. Translates traditional board coordinates of chess into list indices
        """
        if not match:
            print(uci_move + " is not in the format '[a-h][1-8][a-h][1-8]([qbnr])'")
            return None

        start = match.group(1)
        end = match.group(2)
        promotion = match.group(3)
        for coord in [start,end]:
            row = abs(int(coord[1])-8) # Y: Number
            col = coord[0] # X: Letter
            col = "abcdefgh".find(col) # Find Index
            yield (col,row)
        if promotion:
            yield promotion
        else:
            yield 0


    def getMovePlayer(self):
        """
        Asks the user a move in the format '[a-h][1-8][a-h][1-8][qbnr]?'
        Returns in the format "move" which is (([0-7],[0-7]),([0-7],[0-7]),[qbnr]|0)

        """
        try:
            uci_move = input("Move: ")
            move = uci2move(uci_move)
            return move

        except:
            return "EOF"
            print("EOF")

    def getMoveRandom(self):
        """
        Get random move from legal moves

        """
        move = None
        r = random.randint(0,len(self.legalMoves)-1)
        move = self.legalMoves[r]
        return move


    def moveGenerationTest(self, depth):
        """
        Brute force all possible games within a certain ply depth (ply = half-move)

        """
        if depth == 0:
            return 1
        self.legalMoves = self.getLegalMoves()
        self.checkEndgameConditions()

        counter = 0
        for move in self.legalMoves:
            # Make move
            board = copy.deepcopy(self.board)
            self.playMove(move)

            counter += self.moveGenerationTest(depth-1)

            # Undo move

            self.turn = not self.turn
            self.board = board
        return counter

    def kingsInCheck(self):
        for color in [True, False]:
            King = self.board.getKingPiece(color)
            controlledSquares = self.board.getControlledSquares(not color)
            
            if King.get_pos() in controlledSquares:
                King.inCheck = True
            else:
                King.inCheck = False

    def printTurnDecorator(self):
        """
            Print which color it is to move and the board state
        """
        player_turn = "White" if self.turn else "Black"
        print(f"{player_turn}'s turn to move!")
        print(self.board.print_board())

    def playCLI(self, getMove):
        while self.gameRunning:
            self.printTurnDecorator()
            self.legalMoves = self.getLegalMoves()
            print("LegalMoves:", self.legalMoves)

            move = tuple(getMove())
            print("Move:", move)

            if move not in self.legalMoves:
                print("Illegal or impossible move")
                break
                # continue

            if not chess.gameRunning:
                break
            self.playMove(move)

    def playGUI(self):
        import GUI
        logging.basicConfig(filename='log/guiLog.log', level=logging.DEBUG)
        gui = GUI.GUI(self.board,640,640,self)
        gui.main()


    def playBruteForce(self):
        import time
        logging.basicConfig(filename='log/testBrute.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
        depth = sys.argv[2]
        logging.info(f"Initiating move generation test on depth: {depth}")
        l = []
        test_start = time.time()
        ply_depth_start = time.time()
        for i in range(1,int(depth)+1):
            result = self.moveGenerationTest(i)
            l.append(result)
            logging.info(f"Result of possible games with {i} ply: {result}")
            ply_elapsed_time = str(time.time() - ply_depth_start)[:4]
            logging.info(f"Elapsed time in {i} ply: {ply_elapsed_time} seconds")
            ply_depth_start = time.time()
        logging.info(f"Elapsed time: {time.time() - test_start}")



    def main(self):

        arg = sys.argv[1]

        if arg == "-cli" or arg == "-r":
            if arg == "-cli":
                getMove = self.getMovePlayer
            elif arg == "-r":
                getMove = self.getMoveRandom

            self.playCLI(getMove)

        if arg == "-gui":

            self.playGUI()

        elif arg == "-b":

            self.playBruteForce()

        elif arg == "-cligui":

            pass

            

if __name__ == "__main__":
    chess = Chess(board.Board())
    chess.main()





