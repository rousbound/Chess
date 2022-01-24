
Introduction
------------

python-chess is a chess library for Python, with move generation,
move validation, and support for common formats. This is the Scholar's mate in
python-chess:

.. code:: python

    >>> from mychess import *

    >>> game = Chess()
    White's turn to move!
     *********************************
    8| r | n | b | q | k | b | n | r |
    7| p | p | p | p | p | p | p | p |
    6|   |   |   |   |   |   |   |   |
    5|   |   |   |   |   |   |   |   |
    4|   |   |   |   |   |   |   |   |
    3|   |   |   |   |   |   |   |   |
    2| P | P | P | P | P | P | P | P |
    1| R | N | B | Q | K | B | N | R |
       a   b   c   d   e   f   g   h
    *********************************
    
    # Make moves 
    >>> board.legal_moves  
    a2a4 a2a3 b2b4 b2b3 b1c3 b1a3 c2c4 c2c3 d2d4 d2d3 e2e4 e2e3 f2f4 f2f3 g2g4 g2g3 g1h3 g1f3 h2h4 h2h3
    
    >>> game.push_uci("e2e4")
    
    Black's turn to move!
    *********************************
    8| r | n | b | q | k | b | n | r |
    7| p | p | p | p | p | p | p | p |
    6|   |   |   |   |   |   |   |   |
    5|   |   |   |   |   |   |   |   |
    4|   |   |   |   | P |   |   |   |
    3|   |   |   |   |   |   |   |   |
    2| P | P | P | P |   | P | P | P |
    1| R | N | B | Q | K | B | N | R |
       a   b   c   d   e   f   g   h
    *********************************

    >>> game = Chess("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 0")
    White's turn to move!
    *********************************
    8| r |   |   |   | k |   |   | r |
    7| p |   | p | p | q | p | b |   |
    6| b | n |   |   | p | n | p |   |
    5|   |   |   | P | N |   |   |   |
    4|   | p |   |   | P |   |   |   |
    3|   |   | N |   |   | Q |   | p |
    2| P | P | P | B | B | P | P | P |
    1| R |   |   |   | K |   |   | R |
       a   b   c   d   e   f   g   h
    *********************************
    >>> game.uci_moves()
    a2a4 a2a3 a1b1 a1c1 a1d1 b2b3 c3a4 c3d1 c3b1 c3b5 d5d6 d5e6 d2c1 d2f4 d2e3 d2g5 d2h6 e5g4 e5
    e5c4 e5c6 e5f7 e5d3 e5d7 e2b5 e2f1 e2c4 e2d1 e2a6 e2d3 e1f1 e1d1 e1c1 e1g1 f3g4 f3h5 f3e3 f3
    f3g3 f3h3 f3f4 f3f5 f3f6 g2g4 g2g3 g2h3 h1g1 h1f1
    >>> game.push_uci("a2a4")
    Black's turn to move!
    *********************************
    8| r |   |   |   | k |   |   | r |
    7| p |   | p | p | q | p | b |   |
    6| b | n |   |   | p | n | p |   |
    5|   |   |   | P | N |   |   |   |
    4| P | p |   |   | P |   |   |   |
    3|   |   | N |   |   | Q |   | p |
    2|   | P | P | B | B | P | P | P |
    1| R |   |   |   | K |   |   | R |
       a   b   c   d   e   f   g   h
    *********************************
    >>> game.push_uci("a2a4")
    Illegal or impossible move
    Black's turn to move!
    *********************************
    8| r |   |   |   | k |   |   | r |
    7| p |   | p | p | q | p | b |   |
    6| b | n |   |   | p | n | p |   |
    5|   |   |   | P | N |   |   |   |
    4| P | p |   |   | P |   |   |   |
    3|   |   | N |   |   | Q |   | p |
    2|   | P | P | B | B | P | P | P |
    1| R |   |   |   | K |   |   | R |
       a   b   c   d   e   f   g   h
    *********************************





`Documentation <https://github.com/rousbound/Chess/blob/refactor_jonatas/docs/meta/doc.pdf/>`__
--------------------------------------------------------------------

Features
--------

* Make moves.

  .. code:: python

      game.push_uci("e2e4")

* Load from FEN and save to FEN

  >>> game = Chess("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 0")
    White's turn to move!
    *********************************
    8| r |   |   |   | k |   |   | r |
    7| p |   | p | p | q | p | b |   |
    6| b | n |   |   | p | n | p |   |
    5|   |   |   | P | N |   |   |   |
    4|   | p |   |   | P |   |   |   |
    3|   |   | N |   |   | Q |   | p |
    2| P | P | P | B | B | P | P | P |
    1| R |   |   |   | K |   |   | R |
       a   b   c   d   e   f   g   h
    *********************************
    >>> game.push_uci("a2a4")
    >>> game.board.board_2_FEN()
    'r3k2r/p1ppqpb1/bn2pnp1/3PN3/Pp2P3/2N2Q1p/1PPBBPPP/R3K2R b KQkq a3 0 0'
  
* Opening position in GUI
    
    >>> game.play_gui()
    .. image:: https://github.com/rousbound/Chess/blob/refactor_jonatas/res/example_position.png
