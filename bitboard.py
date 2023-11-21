import numpy as np
from enum import IntEnum

class Rank(IntEnum):
    ONE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7

class File(IntEnum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7

class Square:
    def __init__(self, index):
        self.index = np.uint8(index)

class Move(object):
    def __init__(self, src, dest, promo=None):
        """
        src is Square representing source square
        dst is Square representing destination square
        promo is Piece representing promotion
        """
        self.src = src
        self.dest = dest
        self.promo = promo

class Board:
    def __init__(self):
        self.red_pieces = np.uint32(0)
        self.black_pieces = np.uint32(0)
        self.combined_all = np.uint32(0)
        self.kings = np.uint32(0)
        self.color = 0 # Color to move

        print(bin(self.combined_all))

board = Board()