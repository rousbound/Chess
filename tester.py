import subprocess
import sys

child = subprocess.Popen(['python3', 'chess.py', '-p'], stdin=subprocess.PIPE)
#child.communicate(bytes('d2d4\nd7d5\nc1g5\ne7e6\nb1c3\nd8g5\nd1d3\nh7h6\ne1c1',

string = sys.argv[1:]
command = "\n".join(string)
print(string)
print(command)
child.communicate(bytes(command, "utf-8"))
