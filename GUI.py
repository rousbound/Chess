import pygame
from PIL import ImageColor
from pygame.locals import *
import sys

import utils
import time

class GUI():

    def __init__(self, board, width, height, game, playable=True):
        pygame.init()

        self.fps = 60
        self.cell = width//8
        self.game = game
        self.playable = playable

        self.screen = pygame.display.set_mode((width, height))

        self.board = board
        self.spritesheet = pygame.image.load("res/pieces.png").convert_alpha()
        self.capture = pygame.image.load("res/capture.png").convert_alpha()
        self.check = pygame.image.load("res/Check.png").convert_alpha()
        self.lastMoveFrom = None
        self.lastMoveTo = None

        self.piecesDict = {
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
        self.pieceHeld = None
        self.xoffset = -1
        self.yoffset = -2
        self.getSpriteSheet()

    def getPieceSpriteCoordinates(self, piece):
        pieceColor = "W" if piece.color else "B"
        piece_index = self.piecesDict[pieceColor+piece.name]
        return self.spriteSheetPieceCoordinates[piece_index]

    def getSpriteSheet(self):
        cols = 6
        rows = 2
        cell_count = cols * rows

        rect = self.spritesheet.get_rect()
        w = cell_width = rect.width // cols
        h = cell_height = rect.height // rows

        self.spriteSheetPieceCoordinates = list([(i % cols * w, i // cols * h, w, h) for i in range(cell_count)])



    def draw(self):
        for i in range(8):
            for j in range(8):
                squareBright = ImageColor.getrgb("#f0d9b5")
                squareDark = ImageColor.getrgb("#b58863")
                if (i,j) == self.lastMoveFrom or (i,j) == self.lastMoveTo:
                    squareDark = ImageColor.getrgb("#aba23b")
                    squareBright = ImageColor.getrgb("#cdd26b")
                if self.pieceHeld:
                    mouse_index_x = pygame.mouse.get_pos()[0]//self.cell
                    mouse_index_y = pygame.mouse.get_pos()[1]//self.cell
                if (i + j) % 2 == 0:
                    squareColor = squareBright
                else:
                    squareColor = squareDark

                pygame.draw.rect(self.screen,squareColor,(i*self.cell,j*self.cell,self.cell,self.cell))

                piece = self.board.board[i][j]
                if piece:
                    pieceColor = "W" if piece.color else "B"
                    piece_index = self.piecesDict[pieceColor+piece.name]
                    if not piece.pieceHeld:
                        x = (i*self.cell) + self.xoffset
                        y = (j*self.cell) + self.yoffset
                        if piece.name == "K" and piece.inCheck:
                            self.screen.blit(self.check, (x,y))
                        self.screen.blit(self.spritesheet, (x,y), self.spriteSheetPieceCoordinates[piece_index])

        if self.pieceHeld:
            piece_moves = self.pieceHeld.get_valid_moves(self.board)
            for to in piece_moves:
                start = (self.pieceHeld.x, self.pieceHeld.y)
                uci_move = "".join(utils.mat2uci([start, to]))
                if uci_move in self.legalMoves:
                    color = ImageColor.getrgb("#718a53")
                    if self.board.board[to[0]][to[1]]:
                        x = ((to[0])*self.cell) 
                        y = ((to[1])*self.cell)
                        if self.pieceHeld:
                            mouse_index_x = pygame.mouse.get_pos()[0]//self.cell
                            mouse_index_y = pygame.mouse.get_pos()[1]//self.cell
                            if (to[0],to[1]) == (mouse_index_x, mouse_index_y):
                                if (to[0] + to[1]) % 2 == 0:
                                    squareColor = ImageColor.getrgb("#829769")
                                else:
                                    squareColor = ImageColor.getrgb("#84794e")
                                pygame.draw.rect(self.screen,squareColor,(to[0]*self.cell,to[1]*self.cell,self.cell,self.cell))
                                piece_capturing = self.board.board[to[0]][to[1]]
                                if piece_capturing:
                                    coord = self.getPieceSpriteCoordinates(piece_capturing)
                                    print("coord piece capturing:", coord)
                                    print("coord piece capturing2:", piece_capturing.get_pos())
                                    x = (piece_capturing.get_pos()[0]*80) + self.xoffset
                                    y = (piece_capturing.get_pos()[1]*80) + self.yoffset
                                    self.screen.blit(self.spritesheet, (x,y), coord)
                            else:
                                if (to[0] + to[1]) % 2 == 0:
                                    squareColor = ImageColor.getrgb("#f0d9b5")
                                else:
                                    squareColor = ImageColor.getrgb("#b58863")
                                pygame.draw.rect(self.screen,squareColor,(to[0]*self.cell,to[1]*self.cell,self.cell,self.cell))
                                piece_capturing = self.board.board[to[0]][to[1]]
                                coord = self.getPieceSpriteCoordinates(piece_capturing)
                                print("coord piece capturing:", coord)
                                print("coord piece capturing2:", piece_capturing.get_pos())
                                x_piece = (piece_capturing.get_pos()[0]*80) + self.xoffset
                                y_piece = (piece_capturing.get_pos()[1]*80) + self.yoffset
                                self.screen.blit(self.spritesheet, (x_piece,y_piece), coord)
                                self.screen.blit(self.capture, (x,y))
                        
                    else:
                        x = ((to[0]+1)*self.cell) 
                        y = ((to[1]+1)*self.cell)
                        x -= 40
                        y -= 40
                        if self.pieceHeld:
                            mouse_index_x = pygame.mouse.get_pos()[0]//self.cell
                            mouse_index_y = pygame.mouse.get_pos()[1]//self.cell
                            if (to[0],to[1]) == (mouse_index_x, mouse_index_y):
                                if (to[0] + to[1]) % 2 == 0:
                                    squareColor = ImageColor.getrgb("#829769")
                                else:
                                    squareColor = ImageColor.getrgb("#84794e")
                                pygame.draw.rect(self.screen,squareColor,(to[0]*self.cell,to[1]*self.cell,self.cell,self.cell))
                            else:
                                pygame.draw.circle(self.screen, color, (x,y) , 11, width=0)
            mousepos = pygame.mouse.get_pos()
            x = mousepos[0] - 40
            y = mousepos[1] - 40
            coord = self.getPieceSpriteCoordinates(self.pieceHeld)
            self.screen.blit(self.spritesheet, (x,y), coord)





    def get_piece(self):


        self.legalMoves = self.game.getLegalMoves()
        mousepos = pygame.mouse.get_pos()
        i = mousepos[0] // 80
        j = mousepos[1] // 80
        piece = self.board.board[i][j]
        if piece:
            if piece.color == self.game.turn:
                piece.pieceHeld = True
                self.pieceHeld = piece

    def drop_piece(self):

        if self.pieceHeld:
            mousepos = pygame.mouse.get_pos()
            i = mousepos[0] // 80
            j = mousepos[1] // 80
            to = (i,j)
            start = (self.pieceHeld.x, self.pieceHeld.y)
            self.legalMoves = self.game.getLegalMoves()
            uci_move = "".join(utils.mat2uci([start,to]))
            if uci_move in self.legalMoves:
                self.game.legalMoves = self.game.getLegalMoves()
                index_start, index_to, promotion = utils.splitUci2indices(uci_move)
                self.lastMoveTo = index_to
                self.lastMoveFrom = index_start
                self.game.move(uci_move, index_start, index_to, promotion)
                self.game.kingInCheck(self.game.turn)
                print("Current player to play:", self.game.turn)
                self.board.print_board()
            else:
                print("Illegal move, try again")

            self.pieceHeld.pieceHeld = False
            self.pieceHeld = None


    def main(self):
        self.legalMoves = self.game.getLegalMoves()
        while self.game.gameRunning:
            self.screen.fill((0, 0, 0))
            self.draw()


            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if not self.pieceHeld:
                            self.get_piece()
                if event.type == pygame.MOUSEBUTTONUP:
                    if not pygame.mouse.get_pressed()[0]:
                        self.drop_piece()


            pygame.display.flip()
            # fpsClock.tick(fps)

    def mainUnplayable(self, tick):
        time.sleep(tick)
        self.screen.fill((0, 0, 0))
        self.draw()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if not self.pieceHeld:
                        self.get_piece()
            if event.type == pygame.MOUSEBUTTONUP:
                if not pygame.mouse.get_pressed()[0]:
                    self.drop_piece()
        pygame.display.flip()
