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
        self.capture = pygame.image.load("res/capture2.png").convert_alpha()
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
        self.squareBright = ImageColor.getrgb("#f0d9b5")
        self.squareDark = ImageColor.getrgb("#b58863")
        self.lastMoveSquareDark = ImageColor.getrgb("#aba23b")
        self.lastMoveSquareBright = ImageColor.getrgb("#cdd26b")
        self.capturingSquareBright = ImageColor.getrgb("#829769")
        self.capturingSquareDark = ImageColor.getrgb("#84794e")
        self.circleColor = ImageColor.getrgb("#718a53")

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


    def getMousePos(self):
        x = pygame.mouse.get_pos()[0]//self.cell
        y = pygame.mouse.get_pos()[1]//self.cell
        return (x,y)

    def getPiecePixelPos(self, piece):
        x = (piece.get_pos()[0]*self.cell) + self.xoffset
        y = (piece.get_pos()[1]*self.cell) + self.yoffset
        return (x,y)

    def draw(self):
        for i in range(8):
            for j in range(8):
                # Original Colors
                squareBright = self.squareBright
                squareDark = self.squareDark
                # If square was involved in last move, change colors
                if (i,j) == self.lastMoveFrom or (i,j) == self.lastMoveTo:
                    squareDark = self.lastMoveSquareDark
                    squareBright = self.lastMoveSquareBright

                # Alternate square colors based on i,j
                if (i + j) % 2 == 0:
                    squareColor = squareBright
                else:
                    squareColor = squareDark

                pygame.draw.rect(self.screen,squareColor,(i*self.cell,j*self.cell,self.cell,self.cell))

                piece = self.board.board[i][j]
                if piece:
                    coord = self.getPieceSpriteCoordinates(piece)
                    if not piece.pieceHeld:
                        piece_pixel_pos = self.getPiecePixelPos(piece)
                        if piece.name == "K" and piece.inCheck:
                            self.screen.blit(self.check, piece_pixel_pos)
                        self.screen.blit(self.spritesheet, piece_pixel_pos, coord)

        if self.pieceHeld:
            piece_moves = self.pieceHeld.get_valid_moves(self.board)
            for to in piece_moves:
                start = self.pieceHeld.get_pos()
                uci_move = "".join(utils.mat2uci([start, to]))
                if uci_move in self.game.legalMoves:
                    if self.board.board[to[0]][to[1]]:
                        x = ((to[0])*self.cell) 
                        y = ((to[1])*self.cell)
                        if self.pieceHeld:
                            if (to[0],to[1]) == self.getMousePos():
                                if (to[0] + to[1]) % 2 == 0:
                                    squareColor = self.capturingSquareBright
                                else:
                                    squareColor = self.capturingSquareDark
                                pygame.draw.rect(self.screen,squareColor,(to[0]*self.cell,to[1]*self.cell,self.cell,self.cell))
                                piece_capturing = self.board.board[to[0]][to[1]]
                                if piece_capturing:
                                    coord = self.getPieceSpriteCoordinates(piece_capturing)
                                    piece_pixel_pos = self.getPiecePixelPos(piece_capturing)
                                    self.screen.blit(self.spritesheet, piece_pixel_pos, coord)
                            else:
                                if (to[0] + to[1]) % 2 == 0:
                                    squareColor = self.squareBright
                                else:
                                    squareColor = self.squareDark
                                pygame.draw.rect(self.screen,squareColor,(to[0]*self.cell,to[1]*self.cell,self.cell,self.cell))
                                piece_capturing = self.board.board[to[0]][to[1]]
                                coord = self.getPieceSpriteCoordinates(piece_capturing)
                                piece_pixel_pos = self.getPiecePixelPos(piece_capturing)
                                self.screen.blit(self.spritesheet, piece_pixel_pos, coord)
                                self.screen.blit(self.capture, (x,y))
                        
                    else:
                        if self.pieceHeld:
                            mouse_pos = self.getMousePos()
                            if (to[0],to[1]) == mouse_pos:
                                if (to[0] + to[1]) % 2 == 0:
                                    squareColor = self.capturingSquareBright
                                else:
                                    squareColor = self.capturingSquareDark
                                pygame.draw.rect(self.screen,squareColor,(to[0]*self.cell,to[1]*self.cell,self.cell,self.cell))
                            else:
                                x = ((to[0]+1)*self.cell) 
                                y = ((to[1]+1)*self.cell)
                                x -= 40
                                y -= 40
                                pygame.draw.circle(self.screen, self.circleColor, (x,y) , 11, width=0)
            mouse_pixel_pos = pygame.mouse.get_pos()
            x = mouse_pixel_pos[0] - 40
            y = mouse_pixel_pos[1] - 40
            coord = self.getPieceSpriteCoordinates(self.pieceHeld)
            self.screen.blit(self.spritesheet, (x,y), coord)





    def get_piece(self):


        self.game.legalMoves = self.game.getLegalMoves()
        i,j = self.getMousePos()
        piece = self.board.board[i][j]
        if piece:
            if piece.color == self.game.turn:
                piece.pieceHeld = True
                self.pieceHeld = piece

    def drop_piece(self):

        if self.pieceHeld:
            to = self.getMousePos()
            start = (self.pieceHeld.x, self.pieceHeld.y)
            uci_move = "".join(utils.mat2uci([start,to]))
            if uci_move in self.game.legalMoves:
                index_start, index_to, promotion = utils.splitUci2indices(uci_move)
                self.lastMoveTo = index_to
                self.lastMoveFrom = index_start
                self.game.move(uci_move, index_start, index_to, promotion)
                print("Current player to play:", self.game.turn)
                self.game.kingsInCheck()
                self.game.legalMoves = self.game.getLegalMoves()
                print("Legal Moves:", self.game.legalMoves)
                print("Ghost Pawn:", self.board.getGhostPawn(not self.game.turn))
                self.board.deactivateGhostPawn(self.game.turn)
                self.board.print_board()
            else:
                print("Illegal move, try again")

            self.pieceHeld.pieceHeld = False
            self.pieceHeld = None


    def main(self):
        self.game.legalMoves = self.game.getLegalMoves()
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
