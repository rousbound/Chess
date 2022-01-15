import pygame
from pygame.locals import *
import sys

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

    def draw(self):
        for i in range(8):
            for j in range(8):
                # Original Colors
                square_bright = colors.square_bright
                square_dark = colors.square_dark
                # If square was involved in last move, change colors
                if (i,j) == self.last_move_from or (i,j) == self.last_move_to:
                    square_dark = colors.last_move_square_dark
                    square_bright = colors.last_move_square_bright

                # Alternate square colors based on i,j
                if (i + j) % 2 == 0:
                    square_color = square_bright
                else:
                    square_color = square_dark

                pygame.draw.rect(self.screen,square_color,(i*self.cell,j*self.cell,self.cell,self.cell))

                piece = self.board[i, j]
                if piece:
                    coord = self.get_piece_sprite_coordinates(piece)
                    if not piece.piece_held:
                        piece_pixel_pos = self.get_piece_pixel_pos(piece)
                        if piece.name == "K" and piece.in_check:
                            self.screen.blit(self.in_check_visual_indicator, piece_pixel_pos)
                        self.screen.blit(self.spritesheet, piece_pixel_pos, coord)

        if self.piece_held:
            piece_moves = self.piece_held.get_valid_moves(self.board)
            for move in piece_moves:
                if move in self.game.legal_moves:
                    to = move[1]
                    if self.board[to]:
                        x = ((to[0])*self.cell) 
                        y = ((to[1])*self.cell)
                        if self.piece_held:
                            if to == self.get_mouse_pos():
                                if (to[0] + to[1]) % 2 == 0:
                                    square_color = colors.capturing_square_bright
                                else:
                                    square_color = colors.capturing_square_dark
                                pygame.draw.rect(self.screen,square_color,(to[0]*self.cell,to[1]*self.cell,self.cell,self.cell))
                                piece_capturing = self.board[to]
                                if piece_capturing:
                                    coord = self.get_piece_sprite_coordinates(piece_capturing)
                                    piece_pixel_pos = self.get_piece_pixel_pos(piece_capturing)
                                    self.screen.blit(self.spritesheet, piece_pixel_pos, coord)
                            else:
                                if (to[0] + to[1]) % 2 == 0:
                                    square_color = colors.square_bright
                                else:
                                    square_color = colors.square_dark
                                pygame.draw.rect(self.screen,square_color,(to[0]*self.cell,to[1]*self.cell,self.cell,self.cell))
                                piece_capturing = self.board[to]
                                coord = self.get_piece_sprite_coordinates(piece_capturing)
                                piece_pixel_pos = self.get_piece_pixel_pos(piece_capturing)
                                self.screen.blit(self.spritesheet, piece_pixel_pos, coord)
                                self.screen.blit(self.capture_visual_indicator, (x,y))
                        
                    else:
                        if self.piece_held:
                            mouse_pos = self.get_mouse_pos()
                            if (to[0],to[1]) == mouse_pos:
                                if (to[0] + to[1]) % 2 == 0:
                                    square_color = colors.capturing_square_bright
                                else:
                                    square_color = colors.capturing_square_dark
                                pygame.draw.rect(self.screen,square_color,(to[0]*self.cell,to[1]*self.cell,self.cell,self.cell))
                            else:
                                x = ((to[0]+1)*self.cell) 
                                y = ((to[1]+1)*self.cell)
                                x -= 40
                                y -= 40
                                pygame.draw.circle(self.screen, colors.circle_color, (x,y) , 11, width=0)
            mouse_pixel_pos = pygame.mouse.get_pos()
            x = mouse_pixel_pos[0] - 40
            y = mouse_pixel_pos[1] - 40
            coord = self.get_piece_sprite_coordinates(self.piece_held)
            self.screen.blit(self.spritesheet, (x,y), coord)





    def get_piece(self):
        self.game.legal_moves = self.game.get_legal_moves()
        i,j = self.get_mouse_pos()
        piece = self.board[i,j]
        if piece:
            print("Piece held:", piece.get_pos())
            if piece.color == self.game.turn:
                piece.piece_held = True
                self.piece_held = piece

    def drop_piece(self):
        print("Drop piece")

        if self.piece_held:
            to = self.get_mouse_pos()
            start = self.piece_held.get_pos()
            move = (start, to, 0)
            if move in self.game.legal_moves:
                self.last_move_to = to
                self.last_move_from = start
                self.game.play_move(move)
                self.game.kings_in_check() # To activate king's check visual indicator
                self.game.legal_moves = self.game.get_legal_moves()
                print("Legal moves:", self.game.legal_moves)
                self.game.check_endgame_conditions()
                self.board.deactivate_ghost_pawn(self.game.turn)
            else:
                print("Illegal move, try again")

            self.piece_held.piece_held = False
            self.piece_held = None


    def main(self):
        # self.game.legalMoves = self.game.getLegalMoves()
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
                        self.drop_piece()


            pygame.display.flip()
            # fpsClock.tick(fps)

    def main_unplayable(self, tick):
        time.sleep(tick)
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
                    self.drop_piece()
        pygame.display.flip()
