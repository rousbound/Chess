import subprocess

child = subprocess.Popen(['python3', 'chess.py', '-cligui'], stdin=subprocess.PIPE)
#child.communicate(bytes('d2d4\nd7d5\nc1g5\ne7e6\nb1c3\nd8g5\nd1d3\nh7h6\ne1c1',
child.communicate(bytes('e2e4\na7a6\ne4e5\nf7f5\ne5f6\n', "utf-8"))
