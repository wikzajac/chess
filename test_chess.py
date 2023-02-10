import pytest
from chess import Board

# to start: python -m pytest test_chess.py

def test_piece_converts():
    assert Board.Piece.convert_to_numeric('a1') == [1, 1]
    assert Board.Piece.convert_to_alpha([2, 8]) == 'b8'
    assert Board.Piece.convert_to_alpha(Board.Piece.convert_to_numeric('a1')) == 'a1'

def test_sum_coordinates():
    assert Board.Piece.sum_coordinates([4, 4], [-2, 1]) == [2, 5]

