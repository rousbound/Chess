
def translate(n):
    s = "abcdefgh"
    return s[int(n+1)]

def translateMoves(xstart,ystart,xend,yend):
    move = str(translate(xstart))+str(ystart-1)+str(translate(xend))+str(yend-1)
    return move

def mat2algebric(l):
    l2 = []
    for el in l:
        s = "abcdefgh"
        a = s[int(el[0])]
        b = str(abs(el[1]-8))
        l2.append(a+b)
    return l2
