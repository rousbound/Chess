import subprocess

child = subprocess.Popen(['python3', 'chess.py'], stdin=subprocess.PIPE)
#child.communicate(bytes('d2d4\nd7d5\nc1g5\ne7e6\nb1c3\nd8g5\nd1d3\nh7h6\ne1c1',
child.communicate(bytes('d2d4\nd7d5\nc1g5\ne7e6\nb1c3\nd8g5\nd1d3\nh7h6\ne2e3\na7a6\ne1c1\nb7b6\nd1e1',
    "utf-8"))
