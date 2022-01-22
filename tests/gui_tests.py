import sys
sys.path.insert(0,'../')
sys.path.insert(0,'.')

from mychess.chess import Chess
from mychess.board import Board

# Promotion test

promotion = ["g2g4 h7h5 g4h5 g7g6 h5h6 f8g7 h6g7 f7f6 g7h8q e7e6 h8g8", "rnbqk1Q1/pppp4/4ppp1/8/8/8/PPPPPP1P/RNBQKBNR b KQq - 0 6"]
            

castleKingSide = ["e2e4 e7e5 g1f3 g8f6 f1c4 f8c5 e1g1 e8g8", "rnbq1rk1/pppp1ppp/5n2/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQ1RK1 w - - 6 5"]

castleQueenSide = ["d2d4 d7d5 c1f4 c8f5 b1c3 b8c6 d1d2 d8d7 e1c1 e8c8", "2kr1bnr/pppqpppp/2n5/3p1b2/3P1B2/2N5/PPPQPPPP/2KR1BNR w - - 8 6"]
        
enPasseant = ["e2e4 a7a6 e4e5 d7d5 e5d6", "rnbqkbnr/1pp1pppp/p2P4/8/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 3"]

doubleSpecifier = ["g2g4 h7h5 g4h5 g7g6 h5g6 f8g7 g6f7 e8f8 e2e3 e7e6 f7g8r f8e7 g8g7 e7e8 g1f3 d7d6 h1g1 d6d5 h2h4 e6e5 h4h5 c7c6 h5h6 e8f8 h6h7 f8e8 g1h1 c8d7 c2c3 d8e7 b2b3 d7e6 c3c4 e8d7 b3b4 c6c5 g7e7 d7c6 e3e4 h8g8 h7g8r b7b6 g8h8 a7a6 e7h7", "rn5R/7R/ppk1b3/2ppp3/1PP1P3/5N2/P2P1P2/RNBQKB1R b Q - 1 23"]

# kingHunt = ["g2g4 h7h5 g4h5 g7g6 h5g6 f8g7 g6f7 e8f8 e2e3 e7e6 f7g8r f8e7 g8g7 e7e8 g1f3 d7d6 h1g1 d6d5 h2h4 e6e5 h4h5 c7c6 h5h6 e8f8 h6h7 f8e8 g1h1 c8d7 c2c3 d8e7 b2b3 d7e6 c3c4 e8d7 b3b4 c6c5 g7e7 d7c6 e3e4 h8g8 h7g8r b7b6 g8h8 a7a6 e7h7", "rn5R/7R/ppk1b3/2ppp3/1PP1P3/5N2/P2P1P2/RNBQKB1R b Q - 1 23"]

tests = [promotion, castleKingSide, castleQueenSide, enPasseant, doubleSpecifier]

for test in tests[:1]:

    game = Chess(Board())

    FEN = game.play_gui_test(test[0].split(" "))
    print("Baseline:",test[1])
    print("Test result:", FEN)
    assert FEN == test[1]
