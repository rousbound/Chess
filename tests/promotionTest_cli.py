import sys
sys.path.insert(0,'../')

import mychess.chess as chess
import mychess.board as board

# Promotion test

promotion = "g2g4 h7h5 g4h5 g7g6 h5h6 h8h7 f2f3 h7g7 h6h7 f7f6 h7h8q e7e6 h8h6"

castleLongWhite = "d2d4 d7d5 b1c3 b8c6 c1f4 c8f5 d1d2 d8d7 e1c1 e8c8"

castleShortWhite = "e2e4 e7e5 g1f3 b8c6 f1b5 g8f6 e1g1 f8b4 c2c3 e8g8"


for test_moves in [promotion, castleLongWhite, castleShortWhite]:

    game = chess.Chess(board.Board())

    def test():
        r = game.play_cli_test(test_moves.split(" "))
        assert r[:-1] == test_moves
