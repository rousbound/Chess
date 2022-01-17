import pygame
from pygame.locals import *
import sys
import copy

import utils
import time
import colors

class GUI():

    def __init__(self, board, width, height, game, playable=True):
        pygame.init()

        self.cell : int = width//8
        self.game : object = game
        self.playable : bool = playable

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

    def get_piece(self):
        self.game.legal_moves = self.game.get_legal_moves()
        mouse_pos = self.get_mouse_pos()
        piece = self.board[mouse_pos]
        if piece:
            if piece.color == self.game.turn:
                piece.piece_held = True
                self.piece_held = piece

    def get_promotion(self, to, color):
        while self.promoting:
            behind = 1 if color else -1
            queen = piece.Queen(color, to[0], to[1])
            knight = piece.Knight(color, to[0], to[1]-behind)
            rook = piece.Rook(color, to[0], to[1]-(2*behind), first_move=False)
            bishop = piece.Bishop(color, to[0], to[1]-(3*behind))
            for piece in [queen, knight, rook, bishop]:
                self.draw_piece(piece)


    def drop_piece(self):
        to = self.get_mouse_pos()
        start = self.piece_held.get_pos()
        # if self.piece_held.name == "P":
            # last_row = 0 if self.piece_held.color else 7
            # if to[1] == last_row:
                # self.promoting = True
                # self.get_promotion(to, self.piece_held.color)
        move = (start, to, 0)
        if move in self.game.legal_moves:
            self.last_move_to = to
            self.last_move_from = start
            self.check_promotion(move)
            self.game.play_move(move)
            self.game.kings_in_check() # To activate king's check visual indicator
            self.game.legal_moves = self.game.get_legal_moves()
            print("Legal moves:", self.game.algebric_legal_moves)
            self.game.check_endgame_conditions()
            self.board.deactivate_ghost_pawn(self.game.turn)
            print("MovesList:", self.game.algebric_played_moves)
        else:
            print("Illegal move, try again")

        self.piece_held.piece_held = False
        self.piece_held = None



    def main(self):
        while self.game.game_running:
            self.screen.fill((0, 0, 0))
            self.draw()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if not self.piece_held:
                            self.get_piece()
                if event.type == pygame.MOUSEBUTTONUP:
                    if not pygame.mouse.get_pressed()[0]:
                        if self.piece_held:
                            self.drop_piece()


            pygame.display.flip()

