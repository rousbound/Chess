import sys
from PIL import ImageColor
 
import pygame
import board
from pygame.locals import *
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 640, 640
screen = pygame.display.set_mode((width, height))

board = board.Board()

piecesDict = {
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
spritesheet = pygame.image.load("res/pieces.png").convert_alpha()

cols = 6
rows = 2
cell_count = cols * rows

rect = spritesheet.get_rect()
w = cell_width = rect.width // cols
h = cell_height = rect.height // rows

cells = list([(i % cols * w, i // cols * h, w, h) for i in range(cell_count)])

# def draw(self, surface, piece_name, coords):
    # piece_index = self.pieces[piece_name]
    # surface.blit(self.spritesheet, coords, self.cells[piece_index])

xoffset = -1
yoffset = -2
pieceHeld = None

def draw():
    cell = 80
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 1:
                # squareColor = (0,0,0)
                squareColor = ImageColor.getrgb("#f0d9b5")

            else:
                squareColor = (255,255,255)
                squareColor = ImageColor.getrgb("#b58863")
            pygame.draw.rect(screen,squareColor,(i*cell,j*cell,cell,cell))

            piece = board.board[i][j]
            if piece:
                pieceColor = "W" if piece.color else "B"
                piece_index = piecesDict[pieceColor+piece.name]
                if not piece.pieceHeld:
                    x = (i*cell) + xoffset
                    y = (j*cell) + yoffset
                    screen.blit(spritesheet, (x,y), cells[piece_index])
    if pieceHeld:
        mousepos = pygame.mouse.get_pos()
        pieceColor = "W" if pieceHeld.color else "B"
        piece_index = piecesDict[pieceColor+pieceHeld.name]
        x = mousepos[0] - 40
        y = mousepos[1] - 40
        screen.blit(spritesheet, (x,y), cells[piece_index])

    
def get_piece():
  global pieceHeld

  mousepos = pygame.mouse.get_pos()
  i = mousepos[0] // 80
  j = mousepos[1] // 80
  piece = board.board[i][j]
  if piece:
      piece.pieceHeld = True
      pieceHeld = piece
      print(piece.name)

def drop_piece():
  global pieceHeld

  if pieceHeld:
      mousepos = pygame.mouse.get_pos()
      i = mousepos[0] // 80
      j = mousepos[1] // 80
      pieceCaptured = board.board[i][j]
      if pieceCaptured:
          color1 = "W" if pieceHeld.color else "B"
          color2 = "W" if pieceCaptured.color else "B"
          if pieceCaptured.color != pieceHeld.color:
              print(f"{pieceHeld.name}{color1} captures {pieceCaptured}{color2}")
              pieceHeld.move((i,j), board)
          else:
              print("Illegal move")
      else:
          pieceHeld.move((i,j), board)


      pieceHeld.pieceHeld = False
      pieceHeld = None

 
# Game loop.
while True:
  screen.fill((0, 0, 0))
  draw()

  
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
      get_piece()
    if event.type == pygame.MOUSEBUTTONUP:
      drop_piece()
    
        
  
  # Update.
  
  # Draw.
  
  pygame.display.flip()
  fpsClock.tick(fps)
