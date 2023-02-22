import pytest
from chess import Chess, Piece


# to start: python -m pytest test_chess.py

def test_piece_converts():
    assert Piece.convert_to_numeric('a1') == [1, 1]
    assert Piece.convert_to_alpha([2, 8]) == 'b8'
    assert Piece.convert_to_alpha(Piece.convert_to_numeric('a1')) == 'a1'

def test_sum_coordinates():
    assert Piece.sum_coordinates([4, 4], [-2, 1]) == [2, 5]

def test_is_it_in_board():
    assert Piece.is_it_in_board([1, 1]) == True
    assert Piece.is_it_in_board([8, 8]) == True
    assert Piece.is_it_in_board([9, 8]) == False

def test_piece_ability():
    # Create chess board with start position
    board = Chess.setup(Chess.board_init())

    # Check posible moves and takens for pawn in a2
    assert board['a2'].ability('a2', board) == (['a3', 'a4'], [])
    
    # Check posible moves and takens for knight in g8
    assert board['g8'].ability('g8', board) == (['h6', 'f6'], [])
