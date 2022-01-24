
Introduction
------------

python-chess is a chess library for Python, with move generation,
move validation, and support for common formats. This is the Scholar's mate in
python-chess:

.. code:: python

    >>> from mychess import *

    >>> game = Chess()

    >>> board.legal_moves  # doctest: +ELLIPSIS
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


Installing
----------

Download and install the latest release:

::

    pip install chess


`Documentation <https://python-chess.readthedocs.io/en/latest/>`__
--------------------------------------------------------------------

Features
--------

* Make and unmake moves.

  .. code:: python

      >>> Nf3 = chess.Move.from_uci("g1f3")
      >>> board.push(Nf3)  # Make the move

      >>> board.pop()  # Unmake the last move
      Move.from_uci('g1f3')

* Show a simple ASCII board.

  .. code:: python

      >>> board = chess.Board("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")
      >>> print(board)
      r . b q k b . r
      p p p p . Q p p
      . . n . . n . .
      . . . . p . . .
      . . B . P . . .
      . . . . . . . .
      P P P P . P P P
      R N B . K . N R

* Detects checkmates, stalemates and draws by insufficient material.

  .. code:: python

      >>> board.is_stalemate()
      False
      >>> board.is_insufficient_material()
      False
      >>> board.outcome()
      Outcome(termination=<Termination.CHECKMATE: 1>, winner=True)

* Detects repetitions. Has a half-move clock.

  .. code:: python

      >>> board.can_claim_threefold_repetition()
      False
      >>> board.halfmove_clock
      0
      >>> board.can_claim_fifty_moves()
      False
      >>> board.can_claim_draw()
      False

* Detects checks and attacks.

  .. code:: python

      >>> board.is_check()
      True
      >>> board.is_attacked_by(chess.WHITE, chess.E8)
      True

      >>> attackers = board.attackers(chess.WHITE, chess.F3)
      >>> attackers
      SquareSet(0x0000_0000_0000_4040)
      >>> chess.G2 in attackers
      True
      >>> print(attackers)
      . . . . . . . .
      . . . . . . . .
      . . . . . . . .
      . . . . . . . .
      . . . . . . . .
      . . . . . . . .
      . . . . . . 1 .
      . . . . . . 1 .

* Parses and creates SAN representation of moves.

  .. code:: python

      >>> board = chess.Board()
      >>> board.san(chess.Move(chess.E2, chess.E4))
      'e4'
      >>> board.parse_san('Nf3')
      Move.from_uci('g1f3')
      >>> board.variation_san([chess.Move.from_uci(m) for m in ["e2e4", "e7e5", "g1f3"]])
      '1. e4 e5 2. Nf3'

* Parses and creates FENs, extended FENs and Shredder FENs.

  .. code:: python

      >>> board.fen()
      'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
      >>> board.shredder_fen()
      'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w HAha - 0 1'
      >>> board = chess.Board("8/8/8/2k5/4K3/8/8/8 w - - 4 45")
      >>> board.piece_at(chess.C5)
      Piece.from_symbol('k')


 
