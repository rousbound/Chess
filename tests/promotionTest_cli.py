import subprocess
import os

path = os.path.abspath(".")
cmd = "python3 chess.py -clitest" + " "

moves = "g2g4 h7h5 g4h5 g7g6  h5h6  h8h7  f2f3  h7g7  h6h7  f7f6  h7h8q  e7e6  h8h6"

cmd += moves
print(cmd)

child = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True)
child.communicate()
# #child.communicate(bytes('d2d4\nd7d5\nc1g5\ne7e6\nb1c3\nd8g5\nd1d3\nh7h6\ne1c1',
# child.communicate(bytes('g2g4\nh7h5\ng4h5\ng7g6\nh5h6\nh8h7\nf2f3\nh7g7\nh6h7\nf7f6\nh7h8q\ne7e6\nh8h6', "utf-8"))
