"""
utils.py -- Module made for storing move conversion functions used across all modules
Author: Geraldo Luiz Pereira
www.github.com/rousbound

There are basically three types of move representation:

Algebraic, for example: Nc3, e4, exf4, exf4=Q, O-O-O

UCI, for example: f1b3, e2e4, e7e5, e1g1

And "move", which is the internal representation of a move in the program),
Where the number stands for indexes in the board matrix.
For example: ((4,4),(4,6),%) or ((4,7),(4,8),"q")
"""
import re

def move_2_algebric(board, move, selected_piece, captured_piece, castling):
    """
    Translates a tuple-move to algebric format.
    Ex: ((4,4),(4,6),%) -> e4
        ((4,4),(5,5),%) -> exf5

    It needs board context to understand whether or not it was a capture, promotion, etc.

    """

    start = move[0]
    to = move[1]
    promotion = move[2]
    if castling:
        return castling
    algebric_to = mat_2_uci(to)
    capture = "x" if captured_piece else ""
    if selected_piece.name == "P":
        if capture == "x":
            piece_name = 'abcdefgh'[start[0]]
        else:
            piece_name = ""
    else:
        piece_name = selected_piece.name

    specifier = ""
    if selected_piece.name != "K":
        specifier = board.has_same_target(start, selected_piece, selected_piece.color)

    promotion = "" if promotion == "%" else "=" + promotion.upper()
    return piece_name + specifier + capture + algebric_to + promotion

def move_2_uci(move):
    """
    Translate move to uci format
    Ex: ((4,4),(5,5),%) -> e4f5
    """
    return (mat_2_uci(move[0]),mat_2_uci(move[1]))

def mat_2_uci(square):
    """
    Translates a coordinate in the board matrix to uci format.
    Ex: (4,4) -> e4
        (5,5) -> f5

    """
    a = "abcdefgh"[square[0]]
    b = str(abs(square[1]-8))
    return a + b

def uci_2_move(uci_move):
    """
    1. Check move grammar and
    2. Translates uci notation as 'e2e4' into our move index notation as '((4,4)(4,6),%)'

    """
    match = re.match(r"([a-h][1-8])([a-h][1-8])([qbnr]?)", uci_move)
    if not match:
        print(uci_move + " is not in the format '[a-h][1-8][a-h][1-8]([qbnr])'")
        return None

    start = match.group(1)
    end = match.group(2)
    promotion = match.group(3)

    move = []
    for coord in [start,end]:
        row = abs(int(coord[1])-8) # Y: Number
        col = coord[0] # X: Letter
        col = "abcdefgh".find(col) # Find Index
        move.append((col,row))
    if promotion:
        move.append(promotion)
    else:
        move.append("%")

    return tuple(move)
