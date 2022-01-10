import subprocess

child = subprocess.Popen(['python3', 'chess.py'], stdin=subprocess.PIPE)
child.communicate(bytes('e2e4\ne7e5\ng1f3\nb8c6\nf1b5\ng8f6\ne1g1\nh7h6\nf1e1',"utf-8"))
