
Introduction
------------

python-chess is a chess library for Python, with move generation,
move validation, and support for common formats. This is the Scholar's mate in
python-chess:

.. code:: python

    >>> import chess

    >>> board = chess.Board()

    >>> board.legal_moves  # doctest: +ELLIPSIS
    <LegalMoveGenerator at ... (Nh3, Nf3, Nc3, Na3, h3, g3, f3, e3, d3, c3, ...)>
    >>> chess.Move.from_uci("a8a1") in board.legal_moves
    False

    >>> board.push_san("e4")
    Move.from_uci('e2e4')
    >>> board.push_san("e5")
    Move.from_uci('e7e5')
    >>> board.push_san("Qh5")
    Move.from_uci('d1h5')
    >>> board.push_san("Nc6")
    Move.from_uci('b8c6')
    >>> board.push_san("Bc4")
    Move.from_uci('f1c4')
    >>> board.push_san("Nf6")
    Move.from_uci('g8f6')
    >>> board.push_san("Qxf7")
    Move.from_uci('h5f7')

    >>> board.is_checkmate()
    True

    >>> board
    Board('r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4')

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


 
