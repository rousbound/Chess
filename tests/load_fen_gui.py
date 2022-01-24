import sys
sys.path.insert(0,'../')
sys.path.insert(0,'.')

from mychess.chess import Chess
from mychess.board import Board
from mychess.main import *

# Promotion test

position_1 = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 0"
position_2 = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 0"

chess = Chess(Board(FEN = position_2))

play_gui(chess)

