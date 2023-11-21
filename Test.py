import math
from Checkers import Board
from Checkers import Piece

count = 0
def to_board_pos(num):
    row = math.floor(num/8)
    col = num%8
    return row, col

for p1 in range(0, 64, 2):
    for k1 in True, False:
        for c1 in 0, 1:
            for p2 in range(0, 64, 2):
                for k2 in True, False:
                    for c2 in 0, 1:
                        for p3 in range(0, 64, 2):
                            for k3 in True, False:
                                for c3 in 0, 1:
                                    valid = True
                                    if ((p1 == p2) or (p1 == p3) or (p2 == p3)):
                                        valid = False
                                    if ((c1 == c2) and (c2 == c3)):
                                        valid = False
                                    for piece in (p1, k1, c1), (p2, k2, c2), (p3, k3, c3):
                                        if ((math.floor(piece[0]/8)) == (7 - piece[2]*7)) and (piece[1]):
                                            valid = False

                                    if valid:
                                        count += 1
print(count)