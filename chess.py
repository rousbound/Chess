import copy
import random
import logging

from mychess.utils import mat_2_uci, move_2_algebric, uci_2_move, move_2_uci
import mychess.pieces
from mychess.board import Board



class Chess():
    """
    A class made to use the Board class information to create legal moves and play the game.
    ...

    Attributes:
    -----------

    ----------- DEBUG ------------

    moves_list : list[tup]
        Record of game moves in tuple format

    legal_moves : list[tup]
        List of current legal moves in tuple format

    algebric_legal_moves : list[str]
        List of current legal moves in algebric format

    last_move_algebric : str
        Last move played in algebric format

    pgn_game : str
        List of game moves in algebric format i.e PGN of the game

    uci_game : str
        List of game moves in UCI format

    ----------- GAME LOGIC ------------

    board : Board
        represents the chess board of the game

    game_running : bool
        True if none of draw or win conditions are met.

    board_states : list[Board]
        List of boards, relevant for three fold repetition draw criteria.

    Methods:
    --------

    -------- DEBUG ---------

    turn_debug(move: tup) -> None
        Print last move played, pgn of game until last move and FEN of current board position

    debug_algebric_legal_moves(move : tup, piece : Piece, captured_piece : Piece) -> None
        Converts and save current legal moves in algebric format

    debug_game_uci(move : tup) -> None
        Save moves list in uci format

    debug_game_pgn(move : tup, selected_piece : Piece, captured_piece : Piece, castling : str) -> None
        Save moves  list in pgn format

    -------- GAME LOGIC ---------

    play_move(move:up) -> None
        Make move, check special cases, update board information

    get_legal_moves() -> list[tup]
        Check legal moves

    check_endgame_conditions() -> None
        Check checkmate and draw criteria

    kings_in_check() -> None
        Update king pieces with information whether they are in check or not

    print_turn_decorator() -> None
        Print turn information

    get_move_random(moves:list[str])-> uci_move:str, index_start:tup, index_to:tup, promotion:str
        Get random moves based on legal moves avaiable

    get_move_player(moves:list[str])-> uci_move:str, index_start:tup, index_to:tup, promotion:str
        Ask the user for input and check if it is legal move


    """

    def __init__(self, FEN=None):
        self.board = Board(FEN)
        self.game_running = True
        self.board_states = []

        self.algebric_legal_moves = []
        self.uci_legal_moves = []
        self.legal_moves = self.get_legal_moves()
        self.moves_list = []
        self.last_move_algebric = ""
        self.pgn_game = ""
        self.uci_game = ""
        self.print_turn_decorator()
        self.board.print_board()
        
    def uci_moves(self):
        print(" ".join(self.uci_legal_moves))

    def algebric_moves(self):
        print(" ".join(self.algebric_legal_moves))

    def turn_debug(self):
        """
        Print last turn information.
        """

        print("")
        print("-------------------------------")
        print("Move: ", self.last_move_algebric)
        print("")
        print("LegalMoves: ", " ".join(self.algebric_legal_moves))
        print("")
        print("PGN:", self.pgn_game)
        print("")
        print("FEN:", self.board.board_2_FEN())

    def debug_algebric_legal_moves(self, move, piece, captured_piece):
        """
        Returns list of legal moves in algebric format.
        Ex: Nc3, e4, exd4, O-O, O-O-O

        """

        castling = None
        origin = move[0]
        target = move[1]
        if piece.name == "K":
            res = res = tuple(map(lambda i, j: i - j, origin, target))
            if res[0] < -1:
                castling = "O-O"
            elif res[0] > 1:
                castling = "O-O-O"
        algebric_move = move_2_algebric(self.board, move, piece, captured_piece, castling)
        self.algebric_legal_moves.append(algebric_move)

    def debug_game_uci(self, move):
        """
        Saves list of moves in UCI notation.
        Ex: e2e4 e7e5 g1f3 b1f6 f1b5

        """

        start = mat_2_uci(move[0])
        to = mat_2_uci(move[1])
        promotion = move[2]
        self.uci_game += f"{start}{to}{promotion} "

    def debug_game_pgn(self, move, selected_piece, captured_piece, castling):
        """
        Save list of moves in PGN notation.
        Ex: 1. e4 e5 2. Nf3 Nc6 3. Bb5

        """

        algebric_move = move_2_algebric(self.board,
                                              move,
                                              selected_piece,
                                              captured_piece,
                                              castling)
        self.last_move_algebric = algebric_move

        if self.board.turn:
            algebric_move = f"{str(self.board.turn_counter)}. {algebric_move} "
        else:
            algebric_move = f"{algebric_move} "

        self.pgn_game += algebric_move

    def get_legal_moves(self):
        """
        Iterate through all pieces of turn color and get it's valid moves.
        Then simulate the move and check if King ends in check.
        If not, it is legal move.
        After check Draw conditions.
        """

        legal_moves = []
        self.algebric_legal_moves = []
        self.uci_legal_moves = []
    
        for piece in self.board.get_all_pieces():
            if piece.color == self.board.turn:
                piece_moves = piece.get_valid_moves(self.board)
                # Simulate moves to see if it ends up with king in check
                for move in piece_moves:
                    origin = move[0]
                    target = move[1]

                    # Do move
                    captured_piece = piece.move(target, self.board)

                    enemy_targets = self.board.get_controlled_squares(not self.board.turn)
                    if piece.name != "K":
                        friend_king = self.board.get_king(self.board.turn)
                    else:
                        friend_king = piece

                    # If king not in enemy targets after move, is legal move
                    if friend_king.get_pos() not in enemy_targets:
                        legal_moves.append(move)
                        self.debug_algebric_legal_moves(move, piece, captured_piece)
                        self.uci_legal_moves.append("".join(move_2_uci(move)))

                    # Undo move
                    piece.move(origin,self.board)
                    if captured_piece:
                        captured_piece.move(captured_piece.get_pos(),self.board)
                        # captured_piece.move(target,self.board)



        self.check_endgame_conditions(legal_moves)


        return legal_moves


    def get_promotion(self, promotion, selected_piece):
        color = selected_piece.color
        if promotion == "q":
            promoted_piece = pieces.Queen(color, selected_piece.x, selected_piece.y)
        elif promotion == "r":
            promoted_piece = pieces.Rook(color, selected_piece.x, selected_piece.y)
        elif promotion == "b":
            promoted_piece = pieces.Bishop(color, selected_piece.x, selected_piece.y)
        elif promotion == "n":
            promoted_piece = pieces.Knight(color, selected_piece.x, selected_piece.y)
        return promoted_piece

    def apply_castle(self, move, selected_piece):
        logging.debug("Castling")
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
        elif move[1][0] == 2:
            castling = "O-O-O"
            if selected_piece.color:
                rook = self.board[0,7]
                rook.move((3,7), self.board)
            else:
                rook = self.board[0,0]
                rook.move((3,0), self.board)
        return castling

    def play_move(self, move):
        """
        Moves a piece at `start` to `to`.
        Checks if the move is a special one, and apply the
        correct transformation to the board.

        move: tup
            UCI in the form of a tuple
            Ex: ((4,4),(4,6),%)
            Where the first tuple is the 'start' square,
            the second is the 'to' square and
            the third is the promotion.

        """
        start = move[0]
        to = move[1]
        promotion = move[2]

        selected_piece = self.board[start]
        castling = None


        if selected_piece.name == "P":
            start = move[0]
            to = move[1]
            # Double pawn movement logic
            if abs(to[1]-start[1]) > 1:
                self.board.activate_ghost_pawn(selected_piece.get_pos(), selected_piece.color)

            # Check Promotion
            if promotion in "qrbn":
                selected_piece = self.get_promotion(promotion, selected_piece)

            # Pawn moves resets no progress counter
            self.board.no_progress_plies = 0

        if selected_piece.name == "K":
            # If king moves, whether is castle or normal move:
            # Removes all castling rights
            self.board.remove_castling_rights(self.board.turn)

            # If king moves more than one square, it is castling
            if abs(start[0]-to[0]) > 1:
                castling = self.apply_castle(move, selected_piece)

                # After castle, a position can't be repeated
                if selected_piece.first_move == True:
                    self.board_states = []


        captured_piece = selected_piece.move(to, self.board)

        # Check if move made progress to the game
        # whether it captured or moved a pawn
        if captured_piece:
            self.board.no_progress_plies = 0
        else:
            if selected_piece.name != "P":
                self.board.no_progress_plies += 1

        # Save move in different formats for debugging
        self.debug_game_pgn(move, selected_piece, captured_piece, castling)
        self.debug_game_uci(move)
        self.moves_list.append(move)

        # Save board state for draw criteria
        self.board_states.append(copy.deepcopy(self.board))

        # Increment turn counter for draw criteria
        if not self.board.turn:
            self.board.turn_counter += 1


        # Remove first_move from pieces that has special movement
        if selected_piece.name in ["P", "K"]:
            selected_piece.first_move = False
        if selected_piece.name in ["R"]:
            self.board.can_castle[selected_piece.rook_side] = False

        # Flip turn
        self.board.turn = not self.board.turn

        # Update castling rights
        self.board.check_castling_rights()

        # Deactivate ghost pawn
        self.board.deactivate_ghost_pawn(self.board.turn)

        # Check if king is in check
        self.kings_in_check()

    def check_endgame_conditions(self, legal_moves):
        """
        Check endgame conditions such as checkmate and draw.

        """
        def check_material_draw():
            """
            Certain combinations of pieces are impossible to deliver checkmate with.
            What constitutes objetively a draw.

            """
            pieces_left = [] # Other than both kings
            for piece in self.board.get_all_pieces():
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
                        if piece1.color_complex != piece2.color_complex:
                            print("DRAW -- Kings and Bishop vs Bishop of different color complexes cannot checkmate")
                            self.game_running = False

        def check_no_progress_draw():
            """
            No captures or no pawn movements counts as no progress moves.
            If there are 100 no progress half-moves, there is a draw.

            """

            if self.board.no_progress_plies >= 100:
                print("DRAW -- 100 moves without captures or pawn movements")
                self.game_running = False

        def check_stalemate_or_checkmate(legal_moves):
            """
            If there is no legal moves and king in check, it is checkmate,
            otherwise it is a stalemate.

            """
            friend_king = self.board.get_king(self.board.turn)

            if len(legal_moves) == 0:
                if not friend_king.in_check:
                    self.game_running = False
                    print("DRAW -- Stalemate")
                else:
                    self.game_running = False
                    print("CHECKMATE!!!!")
                    logging.debug("CHECKMATE")
                    if self.board.turn:
                        print("BLACK WINS!!!")
                    else:
                        print("WHITE WINS!!!")

        def check_three_fold_repetition():
            """
            Checks if set of legal moves already repeated three times.
            However, we only check last 6 turns-12 plies, otherwise it becomes very
            computationally expensive.
            """
            board_states_counter = {}
            for board in self.board_states[-12:]:
                if board in board_states_counter.keys():
                    board_states_counter[board] += 1
                else:
                    board_states_counter[board] = 1
            for val in board_states_counter.values():
                if val >= 3:
                    self.game_running = False
                    print("DRAW -- Three fold repetition")

        # Check Insufficient material draw

        check_stalemate_or_checkmate(legal_moves)
        check_no_progress_draw()
        check_material_draw()
        # check_three_fold_repetition()

    def kings_in_check(self):
        """
        Check if kings are in check

        """

        for color in [True, False]:
            king = self.board.get_king(color)
            controlled_squares = self.board.get_controlled_squares(not color)

            if king.get_pos() in controlled_squares:
                logging.debug("CHECK")
                king.in_check = True
            else:
                king.in_check = False

    def push_uci(self, uci_move):
        if self.game_running:
            self.legal_moves = self.get_legal_moves()

            if not self.game_running:
                return
                
            move = uci_2_move(uci_move)

            if move not in self.legal_moves:
                print("Illegal or impossible move")
            else:
                # self.turn_debug()
                self.play_move(move)
        self.print_turn_decorator()
        self.board.print_board()
        self.get_legal_moves()

    def get_move_list(self, l):
        l = iter(l)
        n = next(l) 
        print(n)
        return n

    def get_move_player(self):
        """
        Asks the user a move in the format '[a-h][1-8][a-h][1-8][qbnr]?'
        Returns in the format "move" which is (([0-7],[0-7]),([0-7],[0-7]),[qbnr]|%)

        """
        try:
            uci_move = input("Move: ")
            move = uci_2_move(uci_move)
            return move

        except Exception as e:
            print("EOF")
            return "EOF"

    def play_gui(self):
        """
        Play game with Graphical User Interface.

        """
        from mychess.GUI import GUI
        gui = GUI(640,640,self)
        gui.main()

    def get_move_random(self):
        """
        Get random move from legal moves

        """
        move = None
        r = random.randint(0,len(self.legal_moves)-1)
        move = self.legal_moves[r]
        return move

    def print_turn_decorator(self):
        """
        Print which color it is to move and the board state
        """

        player_turn = "White" if self.board.turn else "Black"
        print(f"{player_turn}'s turn to move!")
