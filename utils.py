
def mat2uci(l):
    l2 = []
    for el in l:
        s = "abcdefgh"
        a = s[el[0]]
        b = str(abs(el[1]-8))
        l2.append(a+b)
    return l2

def uci2indices(start, end):
    """
    Translates traditional board coordinates of chess into list indices
    """
    list_indices = []
    for coord in [start,end]:
        row = abs(int(coord[1])-8) # Y: Number
        col = coord[0] # X: Letter
        col = "abcdefgh".find(col) # Find Index
        list_indices.append((col,row))
    return list_indices
