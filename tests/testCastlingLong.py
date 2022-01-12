import subprocess

child = subprocess.Popen(['python3', 'chess.py', '-cligui'], stdin=subprocess.PIPE)
#child.communicate(bytes('d2d4\nd7d5\nc1g5\ne7e6\nb1c3\nd8g5\nd1d3\nh7h6\ne1c1',
print("CastleShortWhite")
child.communicate(bytes('d2d4\nd7d5\nb1c3\nb8c6\nc1f4\nc8f5\nd1d2\nd8d7\ne1c1\ne8c8\n', "utf-8"))
