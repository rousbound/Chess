import subprocess

cmd = "python3 chess.py -cli"
child = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True)
#child.communicate(bytes('d2d4\nd7d5\nc1g5\ne7e6\nb1c3\nd8g5\nd1d3\nh7h6\ne1c1',
child.communicate(bytes('e2e4\ne7e5\ng1f3\nb8c6\nf1b5\ng8f6\ne1g1\nf8b4\nc2c3\ne8g8\n', "utf-8"))
