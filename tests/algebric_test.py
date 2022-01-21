import sys
sys.path.insert(0,'../')
sys.path.insert(0,'.')

import chess
import board 

# Promotion test

            

castleShortWhite = "e4 e5" 

for test_moves in [castleShortWhite]:

    game = chess.Chess(board.Board())

    def test():
        r = game.play_cli_test_algebric(test_moves.split(" "))
        print(r)
        assert r[:-1] == test_moves


    test()

