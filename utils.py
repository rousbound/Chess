import re

def move_2_algebric(board, move, selected_piece, captured_piece, castling):
    start = move[0]
    to = move[1]
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
    
    return piece_name + specifier + capture + algebric_to

def mat_2_uci(el):
    a = "abcdefgh"[el[0]]
    b = str(abs(el[1]-8))
    return a + b

def uci_2_move(uci_move):
    """
    1. Check move grammar and
    2. Translates uci notation as 'e2e4' into our move index notation as '((4,4)(4,6),0)'

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
