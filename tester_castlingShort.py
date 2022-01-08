import subprocess

child = subprocess.Popen(['python3', 'chess.py'], stdin=subprocess.PIPE)
child.communicate(bytes('e2e4\ne7e5\ng1f3\nd7d5\nf1c4\nd5c4\nb2b3\nc4b3\na2b3\nc8d7\nh2h3\nd7b5\ne1g1',
    "utf-8"))
