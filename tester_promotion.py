import subprocess

child = subprocess.Popen(['python3', 'chess.py'], stdin=subprocess.PIPE)
#child.communicate(bytes('d2d4\nd7d5\nc1g5\ne7e6\nb1c3\nd8g5\nd1d3\nh7h6\ne1c1',
#Queen
#child.communicate(bytes('g2g4\nh7h5\ng4h5\nh8h6\nh2h3\nh6f6\nh5h6\na7a6\nh6h7\na6a5\nh7h8q\nb7b5\nh8h6',
#Rook
#child.communicate(bytes('g2g4\nh7h5\ng4h5\nh8h6\nh2h3\nh6f6\nh5h6\na7a6\nh6h7\na6a5\nh7h8r\nb7b5\nh8h6',
#Knight
#child.communicate(bytes('g2g4\nh7h5\ng4h5\nh8h6\nh2h3\nh6f6\nh5h6\na7a6\nh6h7\na6a5\nh7h8n\nb7b5\nh8g6',
#Bishop
child.communicate(bytes('g2g4\nh7h5\ng4h5\nh8h6\nh2h3\nh6f6\nh5h6\na7a6\nh6h7\na6a5\nh7h8b\nb7b5\nh8g7',
    "utf-8"))
