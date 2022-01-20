import board
import piece
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

    game_running : bool
        True if none of draw or win conditions are met.

    moves_list : list[str]
        Record of game moves in uci format

    legal_moves : list[str]
        List of current legal moves

    no_progress_moves : int
        Counter of moves without captures, or pawn movements relevant for draw criteria


    Methods:
    --------

    move(move:str, start:tup, to:tup, promotion:str) -> None
        Make move

    get_legal_moves() -> list[tup]
        Check legal moves

    check_material_draw() -> None
        Check for material-criteria draws

    get_move_random(moves:list[str])-> uci_move:str, index_start:tup, index_to:tup, promotion:str
        Get random moves based on legal moves avaiable

    get_move_player(moves:list[str])-> uci_move:str, index_start:tup, index_to:tup, promotion:str
        Ask the user for input and check if it is legal move

    main() -> None
        Execute Game

    """

    def __init__(self, board : object):
        self.board = board
        self.turn = True
        self.turn_counter = 0
        self.game_running = True
        self.algebric_played_moves = ""
        self.legal_moves = []
        self.moves_list = []
        self.algebric_legal_moves = []
        self.no_progress_moves = 0
        self.board_states = []


    def move_2_algebric(self, move, selected_piece, captured_piece, castling):
        def mat_2_uci(el):
            s = "abcdefgh"
            a = s[el[0]]
            b = str(abs(el[1]-8))
            return a + b
        to = move[1]
        start = move[0]
        if castling:
            return castling
        algebric_to = mat_2_uci(to)
        capture = "x" if captured_piece else ""
        if selected_piece.name == "P":
            if capture == "x":
                piece_name = 'abcdefgh'[start[0]]
            else:
                piece_name = ""
        else:
            piece_name = selected_piece.name
        return piece_name + capture + algebric_to



    def play_move(self, move):
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
                self.board.activate_ghost_pawn(selected_piece.get_pos(), selected_piece.color)
        
            # if move == selected_piece.can_en_passeant:
            iscapture = lambda x,y : abs(x[0]-y[0]) == 1 and abs(x[1]-y[1]) == 1
            if iscapture(to,start):
                enemy_ghost_pawn = self.board.get_ghost_pawn(not self.turn)
                if to == enemy_ghost_pawn:
                    logging.info("En passeant game:")
                    logging.info("Game:", self.moves_list)
                    logging.info("Game:(algebric)", self.algebric_played_moves)
                    if selected_piece.color:
                        self.board[to[0],to[1]+1] = None
                    else:
                        self.board[to[0],to[1]-1] = None
            if str(move[2]) in "qrbn":
                promotion = move[2]
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
            self.no_progress_moves = 0

        # Castling logic

        castling = False
        if selected_piece.name == "K":
            # if move in selected_piece.can_castle:
            if abs(start[0]-to[0]) > 1:
            # ShortCastling
                if move[1][0] == 6:
                    castling = "O-O"
                    if selected_piece.color:
                        rook = self.board[7,7] 
                        rook.move((5,7), self.board)
                    else:
                        rook = self.board[7,0] 
                        rook.move((5,0), self.board)

            # LongCastling
                if move[1][0] == 2:
                    castling = "O-O-O"
                    if selected_piece.color:
                        rook = self.board[0,7] 
                        rook.move((3,7), self.board)
                    else:
                        rook = self.board[0,0] 
                        rook.move((3,0), self.board)
            # logging.info("Castle game:")
            # logging.info("Game:", self.moves_list)
            # logging.info("Game:(algebric)", self.algebric_played_moves)

            # After castle, a position can't be repeated
            if selected_piece.first_move == True:
                self.board_states = []


        captured_piece = selected_piece.move(to, self.board)
        if captured_piece:
            self.no_progress_moves = 0
        else:
            self.no_progress_moves += 1
        self.moves_list.append(move)

        algebric_move = self.move_2_algebric(move, selected_piece, captured_piece, castling)
        if self.turn:
            falgebric_move = f"{str(self.turn_counter+1)}. {algebric_move} "
        else:
            falgebric_move = f"{algebric_move} "
        self.algebric_played_moves += falgebric_move
        self.board_states.append(copy.deepcopy(self.board))
        self.turn = not self.turn
        self.board.turn = not self.board.turn
        if self.turn:
            self.turn_counter += 1

        # Remove first_move from pieces
        if selected_piece.name in ["P","R","K"]:
            selected_piece.first_move = False
        self.kings_in_check() 
        return algebric_move





    def get_legal_moves(self):
        """
        Iterate through all pieces of turn color and get it's valid moves. 
        Then simulate the move and check if King ends in check.
        If not, it is legal move.
        After check Draw conditions
        """

        legal_moves = []
        self.algebric_legal_moves = []
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

                            enemy_targets = self.board.get_controlled_squares(not self.turn)
                            friend_king = self.board.get_piece("K", self.turn)[0]

                            # If king not in enemy targets after move, is legal move
                            if friend_king.get_pos() not in enemy_targets:
                                legal_moves.append(move)

                            # Undo move
                            piece.move(origin,self.board)
                            castling = None
                            if piece.name == "K":
                                res = res = tuple(map(lambda i, j: i - j, origin, target))
                                if res[0] < -1:
                                    castling = "O-O"
                                elif res[0] > 1:
                                    castling = "O-O-O"
                            algebric_move = self.move_2_algebric(move, piece, captured_piece, castling)
                            self.algebric_legal_moves.append(algebric_move)
                            if captured_piece:
                                captured_piece.move(target,self.board)

        return legal_moves
    
    def check_endgame_conditions(self):
        def check_material_draw():
            pieces_left = []
            for piece in self.board.vector():
                if piece:
                    if piece.name != "K":
                        pieces_left.append(piece)
            if not pieces_left:
                self.game_running = False
                print("DRAW -- Only kings left")
            if len(pieces_left) == 1:
                piece = pieces_left[0]
                if piece.name == "B":
                    print("DRAW -- King and Bishop cannot checkmate")
                    self.game_running = False
                if piece.name == "N":
                    print("DRAW -- King and Knight cannot checkmate")
                    self.game_running = False
            if len(pieces_left) == 2:
                piece1 = pieces_left[0]
                piece2 = pieces_left[1]
                if piece1.color != piece2.color:
                    if piece1.name == "B" and piece1.name == "B":
                        print("DRAW -- King and Bishop vs King and Bishop cannot checkmate")
                        self.game_running = False
                    elif piece1.name == "B" and piece1.name == "N":
                        print("DRAW -- King and Bishop vs King and Knight cannot checkmate")
                        self.game_running = False
                    elif piece1.name == "N" and piece1.name == "B":
                        print("DRAW -- King and Knight vs King and Bishop cannot checkmate")
                        self.game_running = False

                    # OBS:
                    # Although having two Knights does not imply forced checkmate, 
                    # it is possible if your opponent doesn't defend with the right moves
        # Check if game has met checkmate or draw criteria
        def check_no_progress_draw():
            if self.no_progress_moves == 50:
                print("DRAW -- 50 moves without captures or pawn movements")
                self.game_running = False
                pass

        def check_stalemate_or_checkmate():
            friend_king = self.board.get_piece("K", self.turn)[0]
            enemy_targets = self.board.get_controlled_squares(not self.turn)

            # If there is no legal moves while not in check,
            # there is stalemate, otherwise, checkmate
            if len(self.legal_moves) == 0:
                # Not in Check
                if (friend_king.x,friend_king.y) not in enemy_targets:
                    self.game_running = False
                    print("DRAW -- Stalemate")
                # In Check
                else:
                    self.game_running = False
                    print("CHECKMATE!!!!")
                    logging.info("Game:", self.moves_list)
                    logging.info("Game:(algebric)", self.algebric_played_moves)
                    if self.turn:
                        print("BLACK WINS!!!")
                    else:
                        print("WHITE WINS!!!")

        def check_three_fold_repetition():
            board_states_counter = {}
            # Counts repetition in the lasts 6 turns or 12 plys
            for board in self.board_states[-12:]:
                if board in board_states_counter.keys():
                    board_states_counter[board] += 1
                else:
                    board_states_counter[board] = 1
            for key, val in board_states_counter.items():
                if val >= 3:
                    self.game_running = False
                    print("DRAW -- Three fold repetition")
                    pass

        # Check Insufficient material draw

        check_stalemate_or_checkmate()
        check_no_progress_draw()
        check_material_draw()
        check_three_fold_repetition()






    def uci_2_move(self, uci_move):
        """
        1. Check move grammar and
        2. Translates uci notation as 'e2e4' into our move index notation as '((4,4)(4,6),0)'

        """
        match = re.match(r"([a-h][1-8])([a-h][1-8])([qbnr]?)", uci_move)
        if not match:
            print(uci_move + " is not in the format '[a-h][1-8][a-h][1-8]([qbnr])'")
            return None

        start = match.group(1)
        end = match.group(2)
        promotion = match.group(3)
        
        move = []
        for coord in [start,end]:
            row = abs(int(coord[1])-8) # Y: Number
            col = coord[0] # X: Letter
            col = "abcdefgh".find(col) # Find Index
            move.append((col,row))
        if promotion:
            move.append(promotion)
        else:
            move.append(0)

        return tuple(move)


    def get_move_player(self):
        """
        Asks the user a move in the format '[a-h][1-8][a-h][1-8][qbnr]?'
        Returns in the format "move" which is (([0-7],[0-7]),([0-7],[0-7]),[qbnr]|0)

        """
        try:
            uci_move = input("Move: ")
            move = self.uci_2_move(uci_move)
            return move

        except:
            return "EOF"
            print("EOF")

    def get_move_random(self):
        """
        Get random move from legal moves

        """
        move = None
        r = random.randint(0,len(self.legal_moves)-1)
        move = self.legal_moves[r]
        return move


    def kings_in_check(self):
        """
        Check if kings are in check
        
        """

        for color in [True, False]:
            king = self.board.get_piece("K", color)[0]
            controlled_squares = self.board.get_controlled_squares(not color)
            
            if king.get_pos() in controlled_squares:
                king.in_check = True
            else:
                king.in_check = False

    def print_turn_decorator(self):
        """
        Print which color it is to move and the board state
        """
        player_turn = "White" if self.turn else "Black"
        print(f"{player_turn}'s turn to move!")
        print(self.board.print_board())

    def play_cli(self, get_move):
        while self.game_running:
            self.print_turn_decorator()
            self.legal_moves = self.get_legal_moves()
            print("LegalMoves:", self.algebric_played_moves)

            move = get_move()
            print("Move:", move)

            if move not in self.legal_moves:
                print("Illegal or impossible move")
                continue

            if not chess.game_running:
                break
            self.play_move(move)

    def play_cli_test(self, input_moves):
        print("Input moves:", input_moves)
        for move in input_moves:
            print("Move:", move)
            move = self.uci_2_move(move)
            self.print_turn_decorator()
            self.legal_moves = self.get_legal_moves()
            print("LegalMoves:", self.legal_moves)
            if move not in self.legal_moves:
                print("Illegal or impossible move")
                break
                # continue

            if not chess.game_running:
                break
            self.play_move(move)

        while self.game_running:
            self.print_turn_decorator()
            self.legal_moves = self.get_legal_moves()
            print("LegalMoves:", self.legal_moves)

            move = self.get_move_player()
            print("Move:", move)

            if move not in self.legal_moves:
                print("Illegal or impossible move")
                break
                # continue

            if not chess.game_running:
                break
            self.play_move(move)

    def play_gui(self):
        import GUI
        logging.basicConfig(filename='log/guiLog.log', level=logging.DEBUG)
        gui = GUI.GUI(self.board,640,640,self)
        gui.main()

    def play_cli_gui(self, argv):

        moves_list = argv[2:]
        print("Moves list:", moves_list)

        import GUI
        logging.basicConfig(filename='log/guiLog.log', level=logging.DEBUG)
        gui = GUI.GUI(self.board,640,640,self)
        gui.cli_gui_main(moves_list)

    def play_brute_force(self):
        import time
        import datetime

        logging.basicConfig(filename='log/testBrute.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
        depth = int(sys.argv[2])
        logging.info(f"Initiating move generation test on depth: {depth}")
        l = []
        test_start = time.time()
        ply_depth_start = time.time()
        expected_results = [20,400,8902,197_281,4_865_609]
        for i,j in zip(range(1,depth+1), expected_results):
            result = self.move_generation_test(i)
            l.append(result)
            logging.info(f"Result of possible games with {i} ply: {result}/{j} - {'OK' if result == j else 'ERROR'}")
            ply_elapsed_time = (time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - ply_depth_start)))
            logging.info(f"Elapsed time in {i} ply: {ply_elapsed_time} seconds")
            ply_depth_start = time.time()
        
        all_elapsed_time = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - test_start))

        logging.info(f"Total Elapsed time: ({all_elapsed_time})")



    def main(self, args=sys.argv):

        if len(args) == 1:
            arg = ""
        else:
            arg = args[1]

        if arg == "-cli" or arg == "-r":
            if arg == "-cli":
                get_move = self.get_move_player
            elif arg == "-r":
                get_move = self.get_move_random

            self.play_cli(get_move)

        if arg == "-gui" or arg == "":

            self.play_gui()

        elif arg == "-guitest":
            self.play_cli_gui(sys.argv)
        elif arg == "-clitest":
            self.play_cli_test(sys.argv[2:])

            

if __name__ == "__main__":
    chess = Chess(board.Board())
    chess.main()





