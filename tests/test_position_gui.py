"""
Opening certain positions directly on GUI by using a FEN

"""
from mychess import Chess
from board import Board
from main import *


def play_position_in_gui(position):
    chess = Chess(fen=position)
    chess.play_gui()

def test_gui_position_1():
    position_1 = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 0"
    play_position_in_gui(position_1)

def test_gui_position_2():
    position_2 = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 0"
    play_position_in_gui(position_2)

def test_gui_position_3():
    position_3 = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 0"
    play_position_in_gui(position_3)

def test_gui_position_4():
    position_4 = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 0"
    play_position_in_gui(position_4)

def test_gui_position_5():
    position_5 = "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10"
    play_position_in_gui(position_5)
