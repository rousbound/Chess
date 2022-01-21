import pygame
from pygame.locals import *
import sys
import copy

import time
import colors

from piece import Queen, Knight, Rook, Bishop

class GUI():

    def __init__(self, board, width, height, game):
        pygame.init()

        self.cell : int = width//8
        self.game : object = game
        self.promoting : bool = False
        self.promoting_column : int = None
        self.promoting_move : list = []

        self.screen = pygame.display.set_mode((width, height))

        self.board : object = board 
        self.spritesheet = pygame.image.load("res/pieces.png").convert_alpha()
        self.capture_visual_indicator : object = pygame.image.load("res/capture2.png").convert_alpha()
        self.in_check_visual_indicator : object = pygame.image.load("res/Check.png").convert_alpha()
        self.last_move_from = None
        self.last_move_to = None

        self.pieces_dict = {
                "WP": 5,
                "WN": 3,
                "WB": 2,
                "WR": 4,
                "WK": 0,
                "WQ": 1,
                "BP": 11,
                "BN": 9,
                "BB": 8,
                "BR": 10,
                "BK": 6,
                "BQ": 7
                }
        self.piece_held = None
        self.xoffset = -1
        self.yoffset = -2
        self.get_sprite_sheet()

    def get_piece_sprite_coordinates(self, piece):
        piece_color = "W" if piece.color else "B"
        piece_index = self.pieces_dict[piece_color+piece.name]
        return self.sprite_sheet_piece_coordinates[piece_index]

    def get_sprite_sheet(self):
        cols = 6
        rows = 2
        cell_count = cols * rows

        rect = self.spritesheet.get_rect()
        w = cell_width = rect.width // cols
        h = cell_height = rect.height // rows

        self.sprite_sheet_piece_coordinates = list([(i % cols * w, i // cols * h, w, h) for i in range(cell_count)])


    def get_mouse_pos(self):
        x = pygame.mouse.get_pos()[0]//self.cell
        y = pygame.mouse.get_pos()[1]//self.cell
        return (x,y)

    def get_piece_pixel_pos(self, piece):
        x = (piece.get_pos()[0]*self.cell) + self.xoffset
        y = (piece.get_pos()[1]*self.cell) + self.yoffset
        return (x,y)


    def draw_piece(self, piece, pos=None):
        if not pos:
            piece_pixel_pos = self.get_piece_pixel_pos(piece)
        else:
            piece_pixel_pos = pos
        coord = self.get_piece_sprite_coordinates(piece)
        self.screen.blit(self.spritesheet, piece_pixel_pos, coord)

    def draw_square(self, pos, bright, dark):
        if (pos[0] + pos[1]) % 2 == 0:
            square_color = bright
        else:
            square_color = dark
        pygame.draw.rect(self.screen,square_color,(pos[0]*self.cell,pos[1]*self.cell,self.cell,self.cell))

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                # Original Colors
                square_bright = colors.square_bright
                square_dark = colors.square_dark
                # If square was involved in last move, change colors
                if (i,j) == self.last_move_from or (i,j) == self.last_move_to:
                    square_bright = colors.last_move_square_bright
                    square_dark = colors.last_move_square_dark

                # Alternate square colors based on i,j
                self.draw_square((i, j), square_bright, square_dark)

                piece = self.board[i, j]
                # Draw pieces, except the one held and check if king is in check
                if piece:
                    if not piece.piece_held:
                        piece_pixel_pos = self.get_piece_pixel_pos(piece)
                        if piece.name == "K" and piece.in_check:
                            self.screen.blit(self.in_check_visual_indicator, piece_pixel_pos)
                        self.draw_piece(piece)
    

    def draw_piece_held(self):
        index2pixel = lambda x: (x[0]*self.cell, x[1]*self.cell)
        piece_moves = self.piece_held.get_valid_moves(self.board)
        # Draw legal moves of piece held
        for move in piece_moves:
            if move in self.game.legal_moves:
                to = move[1]
                is_piece = self.board[to]
                mouse_pos = self.get_mouse_pos()

                # If mouse over legal move, draw green background, else redraw default colors in case
                # they are displaying last move colors
                if to == mouse_pos:
                    self.draw_square(to, colors.capturing_square_bright, colors.capturing_square_dark)
                else:
                    self.draw_square(to, colors.square_bright, colors.square_dark)
                if is_piece:
                    # Redraw piece in case its has been overlayed
                    self.draw_piece(is_piece)

                    # If mouse not over it, display capture possibility
                    if not to == mouse_pos:
                        self.screen.blit(self.capture_visual_indicator, index2pixel(to))
                else:
                    # If there is no piece and mouse is not over, display normal move possibility
                    # in the form of a green circle
                    if not to == mouse_pos:
                        x,y = index2pixel(to)
                        x += (self.cell//2)
                        y += (self.cell//2)
                        pygame.draw.circle(self.screen, colors.circle_color, (x,y) , 11, width=0)

        mouse_pixel_pos = pygame.mouse.get_pos()
        # Center piece at mouse pos
        x = mouse_pixel_pos[0] - (self.cell//2)
        y = mouse_pixel_pos[1] - (self.cell//2)
        self.draw_piece(self.piece_held, (x,y))

    def draw(self):
        self.draw_board()
        if self.piece_held:
            self.draw_piece_held()


    def init_promotion(self, to, start):
        self.promoting_column = to[0]
        self.promoting = True
        self.promoting_move = [start, to, ""]
        self.piece_held.piece_held = False
        self.piece_held = None
        behind = 1 if self.game.turn else -1
        last_row = 0 if self.game.turn else 7
        color = self.game.turn
        queen = Queen(color, self.promoting_column, last_row)
        knight = Knight(color, self.promoting_column, last_row + behind)
        rook = Rook(color, self.promoting_column, last_row + (2*behind), first_move=False)
        bishop = Bishop(color, self.promoting_column, last_row + (3*behind))

        self.promoting_pieces = [queen, knight, rook, bishop]

    def draw_promotion(self):
        mouse_pos = self.get_mouse_pos()
        for piece in self.promoting_pieces:
            if piece.get_pos() == mouse_pos:
                self.draw_square(piece.get_pos(), colors.red, colors.red)
            self.draw_piece(piece)

    def choose_promotion(self):
        mouse_pos = self.get_mouse_pos()
        for piece in self.promoting_pieces:
            if piece.get_pos() == mouse_pos:
                self.promoting = False
                self.promoting_move[2] = piece.name.lower()
                self.play_move(tuple(self.promoting_move))
                self.promoting_move = []

    def play_move(self, move):
        self.last_move_to = move[0]
        self.last_move_from = move[1]
        self.board.deactivate_ghost_pawn(self.game.turn)
        self.game.play_move(move)
        self.game.legal_moves = self.game.get_legal_moves()
        self.game.check_endgame_conditions()
        self.game.kings_in_check() 
        print("Legal moves:", self.game.legal_moves)
        print("MovesList:", self.game.algebric_played_moves)
        print("FEN:", self.board.board_2_FEN())

    def hold_piece(self):
        mouse_pos = self.get_mouse_pos()
        piece = self.board[mouse_pos]
        if piece:
            if piece.color == self.game.turn:
                piece.piece_held = True
                self.piece_held = piece

    def drop_piece(self):
        self.game.legal_moves = self.game.get_legal_moves()
        to = self.get_mouse_pos()
        start = self.piece_held.get_pos()
        if self.piece_held.name == "P":
            if not self.board.get_piece("K", self.game.turn).in_check:
                last_row = 0 if self.piece_held.color else 7
                if to[1] == last_row:
                    self.init_promotion(to, start)
                    return
        move = (start, to, 0)
        if move in self.game.legal_moves:
            self.play_move(move)
        else:
            print("Illegal move, try again")

        self.piece_held.piece_held = False
        self.piece_held = None



    def main(self):
        self.game.legal_moves = self.game.get_legal_moves()
        while self.game.game_running:
            self.screen.fill((0, 0, 0, 255))
            self.draw()
            if self.promoting:
                self.screen.fill(colors.background_promotion)
                self.draw_promotion()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if not self.piece_held:
                            if not self.promoting:
                                self.hold_piece()
                            else:
                                self.choose_promotion()
                                pass
                if event.type == pygame.MOUSEBUTTONUP:
                    if not pygame.mouse.get_pressed()[0]:
                        if self.piece_held:
                            if not self.promoting:
                                self.drop_piece()


            pygame.display.flip()

    def cli_gui_main(self, moves_list):
        print("Moves list", moves_list)
        for move in moves_list:
            move = self.game.uci_2_move(move)
            self.play_move(move)
        self.main()


