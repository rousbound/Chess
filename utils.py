import re




def mat2uci(l):
    l2 = []
    for el in l:
        s = "abcdefgh"
        a = s[el[0]]
        b = str(abs(el[1]-8))
        l2.append(a+b)
    return l2

def uci2move(uci_move):
    match = re.match(r"([a-h][1-8])([a-h][1-8])([qbnr]?)", uci_move)
    """
    Translates traditional board coordinates of chess into list indices
    """

    start = match.group(1)
    end = match.group(2)
    promotion = match.group(3)
    for coord in [start,end]:
        row = abs(int(coord[1])-8) # Y: Number
        col = coord[0] # X: Letter
        col = "abcdefgh".find(col) # Find Index
        yield (col,row)
    if promotion:
        yield promotion
    else:
        yield 0
