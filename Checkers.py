import pygame
import math
import time
import datetime
import os
import copy
from threading import Thread
from Checkers_CPU import CPU
import Checkers_CPU2
from pygame_text import Text
from Basic_UI import Menu
from Game_Viewer import Game_Viewer
from Game_Viewer import Game_Summary

cwd = os.getcwd()

red = (175, 0, 0)
bright_red = (255, 0, 0)
dark_red = (100, 0, 0)
green = (0, 100, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
grey = (130, 130, 130)
dark_grey = (80, 80, 80)

red_moves = [[[[(1, 1), (2, 2)]], [[(1, 0)], [(1, 2), (2, 3)]], [[(1, 1), (2, 0)], [(1, 3), (2, 4)]], [[(1, 2), (2, 1)], [(1, 4), (2, 5)]], [[(1, 3), (2, 2)], [(1, 5), (2, 6)]], [[(1, 4), (2, 3)], [(1, 6), (2, 7)]], [[(1, 5), (2, 4)], [(1, 7)]], [[(1, 6), (2, 5)]]],
[[[(2, 1), (3, 2)]], [[(2, 0)], [(2, 2), (3, 3)]], [[(2, 1), (3, 0)], [(2, 3), (3, 4)]], [[(2, 2), (3, 1)], [(2, 4), (3, 5)]], [[(2, 3), (3, 2)], [(2, 5), (3, 6)]], [[(2, 4), (3, 3)], [(2, 6), (3, 7)]], [[(2, 5), (3, 4)], [(2, 7)]], [[(2, 6), (3, 5)]]],
[[[(3, 1), (4, 2)]], [[(3, 0)], [(3, 2), (4, 3)]], [[(3, 1), (4, 0)], [(3, 3), (4, 4)]], [[(3, 2), (4, 1)], [(3, 4), (4, 5)]], [[(3, 3), (4, 2)], [(3, 5), (4, 6)]], [[(3, 4), (4, 3)], [(3, 6), (4, 7)]], [[(3, 5), (4, 4)], [(3, 7)]], [[(3, 6), (4, 5)]]],
[[[(4, 1), (5, 2)]], [[(4, 0)], [(4, 2), (5, 3)]], [[(4, 1), (5, 0)], [(4, 3), (5, 4)]], [[(4, 2), (5, 1)], [(4, 4), (5, 5)]], [[(4, 3), (5, 2)], [(4, 5), (5, 6)]], [[(4, 4), (5, 3)], [(4, 6), (5, 7)]], [[(4, 5), (5, 4)], [(4, 7)]], [[(4, 6), (5, 5)]]],
[[[(5, 1), (6, 2)]], [[(5, 0)], [(5, 2), (6, 3)]], [[(5, 1), (6, 0)], [(5, 3), (6, 4)]], [[(5, 2), (6, 1)], [(5, 4), (6, 5)]], [[(5, 3), (6, 2)], [(5, 5), (6, 6)]], [[(5, 4), (6, 3)], [(5, 6), (6, 7)]], [[(5, 5), (6, 4)], [(5, 7)]], [[(5, 6), (6, 5)]]],
[[[(6, 1), (7, 2)]], [[(6, 0)], [(6, 2), (7, 3)]], [[(6, 1), (7, 0)], [(6, 3), (7, 4)]], [[(6, 2), (7, 1)], [(6, 4), (7, 5)]], [[(6, 3), (7, 2)], [(6, 5), (7, 6)]], [[(6, 4), (7, 3)], [(6, 6), (7, 7)]], [[(6, 5), (7, 4)], [(6, 7)]], [[(6, 6), (7, 5)]]],
[[[(7, 1)]], [[(7, 0)], [(7, 2)]], [[(7, 1)], [(7, 3)]], [[(7, 2)], [(7, 4)]], [[(7, 3)], [(7, 5)]], [[(7, 4)], [(7, 6)]], [[(7, 5)], [(7, 7)]], [[(7, 6)]]],   
[[], [], [], [], [], [], [], []]]

black_moves = [[[], [], [], [], [], [], [], []],
[[[(0, 1)]], [[(0, 0)], [(0, 2)]], [[(0, 1)], [(0, 3)]], [[(0, 2)], [(0, 4)]], [[(0, 3)], [(0, 5)]], [[(0, 4)], [(0, 6)]], [[(0, 5)], [(0, 7)]], [[(0, 6)]]],   
[[[(1, 1), (0, 2)]], [[(1, 0)], [(1, 2), (0, 3)]], [[(1, 1), (0, 0)], [(1, 3), (0, 4)]], [[(1, 2), (0, 1)], [(1, 4), (0, 5)]], [[(1, 3), (0, 2)], [(1, 5), (0, 6)]], [[(1, 4), (0, 3)], [(1, 6), (0, 7)]], [[(1, 5), (0, 4)], [(1, 7)]], [[(1, 6), (0, 5)]]],
[[[(2, 1), (1, 2)]], [[(2, 0)], [(2, 2), (1, 3)]], [[(2, 1), (1, 0)], [(2, 3), (1, 4)]], [[(2, 2), (1, 1)], [(2, 4), (1, 5)]], [[(2, 3), (1, 2)], [(2, 5), (1, 6)]], [[(2, 4), (1, 3)], [(2, 6), (1, 7)]], [[(2, 5), (1, 4)], [(2, 7)]], [[(2, 6), (1, 5)]]],
[[[(3, 1), (2, 2)]], [[(3, 0)], [(3, 2), (2, 3)]], [[(3, 1), (2, 0)], [(3, 3), (2, 4)]], [[(3, 2), (2, 1)], [(3, 4), (2, 5)]], [[(3, 3), (2, 2)], [(3, 5), (2, 6)]], [[(3, 4), (2, 3)], [(3, 6), (2, 7)]], [[(3, 5), (2, 4)], [(3, 7)]], [[(3, 6), (2, 5)]]],
[[[(4, 1), (3, 2)]], [[(4, 0)], [(4, 2), (3, 3)]], [[(4, 1), (3, 0)], [(4, 3), (3, 4)]], [[(4, 2), (3, 1)], [(4, 4), (3, 5)]], [[(4, 3), (3, 2)], [(4, 5), (3, 6)]], [[(4, 4), (3, 3)], [(4, 6), (3, 7)]], [[(4, 5), (3, 4)], [(4, 7)]], [[(4, 6), (3, 5)]]],
[[[(5, 1), (4, 2)]], [[(5, 0)], [(5, 2), (4, 3)]], [[(5, 1), (4, 0)], [(5, 3), (4, 4)]], [[(5, 2), (4, 1)], [(5, 4), (4, 5)]], [[(5, 3), (4, 2)], [(5, 5), (4, 6)]], [[(5, 4), (4, 3)], [(5, 6), (4, 7)]], [[(5, 5), (4, 4)], [(5, 7)]], [[(5, 6), (4, 5)]]],
[[[(6, 1), (5, 2)]], [[(6, 0)], [(6, 2), (5, 3)]], [[(6, 1), (5, 0)], [(6, 3), (5, 4)]], [[(6, 2), (5, 1)], [(6, 4), (5, 5)]], [[(6, 3), (5, 2)], [(6, 5), (5, 6)]], [[(6, 4), (5, 3)], [(6, 6), (5, 7)]], [[(6, 5), (5, 4)], [(6, 7)]], [[(6, 6), (5, 5)]]]]

king_moves = [[[[(1, 1), (2, 2)]], [[(1, 0)], [(1, 2), (2, 3)]], [[(1, 1), (2, 0)], [(1, 3), (2, 4)]], [[(1, 2), (2, 1)], [(1, 4), (2, 5)]], [[(1, 3), (2, 2)], [(1, 5), (2, 6)]], [[(1, 4), (2, 3)], [(1, 6), (2, 7)]], [[(1, 5), (2, 4)], [(1, 7)]], [[(1, 6), (2, 5)]]],
[[[(0, 1)], [(2, 1), (3, 2)]], [[(0, 0)], [(2, 0)], [(0, 2)], [(2, 2), (3, 3)]], [[(0, 1)], [(2, 1), (3, 0)], [(0, 3)], [(2, 3), (3, 4)]], [[(0, 2)], [(2, 2), (3, 1)], [(0, 4)], [(2, 4), (3, 5)]], [[(0, 3)], [(2, 3), (3, 2)], [(0, 5)], [(2, 5), (3, 6)]], [[(0, 4)], [(2, 4), (3, 3)], [(0, 6)], [(2, 6), (3, 7)]], [[(0, 5)], [(2, 5), (3, 4)], [(0, 7)], [(2, 7)]], [[(0, 6)], [(2, 6), (3, 5)]]],
[[[(1, 1), (0, 2)], [(3, 1), (4, 2)]], [[(1, 0)], [(3, 0)], [(1, 2), (0, 3)], [(3, 2), (4, 3)]], [[(1, 1), (0, 0)], [(3, 1), (4, 0)], [(1, 3), (0, 4)], [(3, 3), (4, 4)]], [[(1, 2), (0, 1)], [(3, 2), (4, 1)], [(1, 4), (0, 5)], [(3, 4), (4, 5)]], [[(1, 3), (0, 2)], [(3, 3), (4, 2)], [(1, 5), (0, 6)], [(3, 5), (4, 6)]], [[(1, 4), (0, 3)], [(3, 4), (4, 3)], [(1, 6), (0, 7)], [(3, 6), (4, 7)]], [[(1, 5), (0, 4)], [(3, 5), (4, 4)], [(1, 7)], [(3, 7)]], [[(1, 6), (0, 5)], [(3, 6), (4, 5)]]],
[[[(2, 1), (1, 2)], [(4, 1), (5, 2)]], [[(2, 0)], [(4, 0)], [(2, 2), (1, 3)], [(4, 2), (5, 3)]], [[(2, 1), (1, 0)], [(4, 1), (5, 0)], [(2, 3), (1, 4)], [(4, 3), (5, 4)]], [[(2, 2), (1, 1)], [(4, 2), (5, 1)], [(2, 4), (1, 5)], [(4, 4), (5, 5)]], [[(2, 3), (1, 2)], [(4, 3), (5, 2)], [(2, 5), (1, 6)], [(4, 5), (5, 6)]], [[(2, 4), (1, 3)], [(4, 4), (5, 3)], [(2, 6), (1, 7)], [(4, 6), (5, 7)]], [[(2, 5), (1, 4)], [(4, 5), (5, 4)], [(2, 7)], [(4, 7)]], [[(2, 6), (1, 5)], [(4, 6), (5, 5)]]],
[[[(3, 1), (2, 2)], [(5, 1), (6, 2)]], [[(3, 0)], [(5, 0)], [(3, 2), (2, 3)], [(5, 2), (6, 3)]], [[(3, 1), (2, 0)], [(5, 1), (6, 0)], [(3, 3), (2, 4)], [(5, 3), (6, 4)]], [[(3, 2), (2, 1)], [(5, 2), (6, 1)], [(3, 4), (2, 5)], [(5, 4), (6, 5)]], [[(3, 3), (2, 2)], [(5, 3), (6, 2)], [(3, 5), (2, 6)], [(5, 5), (6, 6)]], [[(3, 4), (2, 3)], [(5, 4), (6, 3)], [(3, 6), (2, 7)], [(5, 6), (6, 7)]], [[(3, 5), (2, 4)], [(5, 5), (6, 4)], [(3, 7)], [(5, 7)]], [[(3, 6), (2, 5)], [(5, 6), (6, 5)]]],
[[[(4, 1), (3, 2)], [(6, 1), (7, 2)]], [[(4, 0)], [(6, 0)], [(4, 2), (3, 3)], [(6, 2), (7, 3)]], [[(4, 1), (3, 0)], [(6, 1), (7, 0)], [(4, 3), (3, 4)], [(6, 3), (7, 4)]], [[(4, 2), (3, 1)], [(6, 2), (7, 1)], [(4, 4), (3, 5)], [(6, 4), (7, 5)]], [[(4, 3), (3, 2)], [(6, 3), (7, 2)], [(4, 5), (3, 6)], [(6, 5), (7, 6)]], [[(4, 4), (3, 3)], [(6, 4), (7, 3)], [(4, 6), (3, 7)], [(6, 6), (7, 7)]], [[(4, 5), (3, 4)], [(6, 5), (7, 4)], [(4, 7)], [(6, 7)]], [[(4, 6), (3, 5)], [(6, 6), (7, 5)]]],
[[[(5, 1), (4, 2)], [(7, 1)]], [[(5, 0)], [(7, 0)], [(5, 2), (4, 3)], [(7, 2)]], [[(5, 1), (4, 0)], [(7, 1)], [(5, 3), (4, 4)], [(7, 3)]], [[(5, 2), (4, 1)], [(7, 2)], [(5, 4), (4, 5)], [(7, 4)]], [[(5, 3), (4, 2)], [(7, 3)], [(5, 5), (4, 6)], [(7, 5)]], [[(5, 4), (4, 3)], [(7, 4)], [(5, 6), (4, 7)], [(7, 6)]], [[(5, 5), (4, 4)], [(7, 5)], [(5, 7)], [(7, 7)]], [[(5, 6), (4, 5)], [(7, 6)]]],
[[[(6, 1), (5, 2)]], [[(6, 0)], [(6, 2), (5, 3)]], [[(6, 1), (5, 0)], [(6, 3), (5, 4)]], [[(6, 2), (5, 1)], [(6, 4), (5, 5)]], [[(6, 3), (5, 2)], [(6, 5), (5, 6)]], [[(6, 4), (5, 3)], [(6, 6), (5, 7)]], [[(6, 5), (5, 4)], [(6, 7)]], [[(6, 6), (5, 5)]]]]

#move format: [start, end, taken]
class Piece:

    def __init__(self, board, pos: tuple[int, int], color: int) -> None:
        self.board = board
        self.pos = pos
        self.color = color
        if self.color:
            self.rgb = black
            self.color_str = 'black'
            self.direction = -1
            self.squares = black_moves
            self.constant_squares = black_moves
            self.king_row = 0
        else:
            self.rgb = dark_red
            self.color_str = 'red'
            self.direction = 1
            self.squares = red_moves
            self.constant_squares = red_moves
            self.king_row = 7

        self.value = 1
        self.is_king = False
        self.move_count = 0
        self.king_move = -1
        self.valid_moves = []

    def draw(self):
        pos = (self.pos[1] + .5) * self.board.interface.square_size, (7.5 - self.pos[0]) * self.board.interface.square_size
        pygame.draw.circle(self.board.interface.screen, self.rgb, pos, self.board.interface.piece_radius)
        if self.is_king:
            pygame.draw.circle(self.board.interface.screen, white, pos, self.board.interface.piece_radius//3)

    def set_valid_moves(self):
        self.valid_moves = []
        pairs = self.squares[self.pos[0]][self.pos[1]]
        for pair in pairs:
            i = len(pair)
            if i:
                y1, x1 = square1 = pair[0]
                taken = self.board.matrix[y1][x1]
                if taken and (i > 1) and (taken.color != self.color):
                    y2, x2 = square2 = pair[1]
                    if not self.board.matrix[y2][x2]:
                        self.board.takes.append([self.pos, square2, taken])
                elif not taken:
                    self.valid_moves.append([self.pos, square1, taken])

    def king(self):
        self.squares = king_moves
        self.is_king = True
        self.king_move = self.move_count
        self.value = 1.25

    def unking(self):
        self.squares = self.constant_squares
        self.is_king = False
        self.king_move = -1
        self.value = 1

    def copy(self):
        new = Piece(self.board, self.pos, self.color)
        new.is_king = self.is_king
        new.king_move = self.king_move
        new.move_count = self.move_count
        new.squares = self.squares
        new.value = self.value

        return new

    def __str__(self):
        return f'{self.color_str} piece at {self.pos[1]}, {self.pos[0]}'

    def __repr__(self) -> str:
        return self.__str__()

class Board:

    def __init__(self, interface):
        self.interface = interface

        self.valid_moves = []
        self.moves = []
        self.turn = 0
        self.game_over = False
        self.takes = []

        self.init_matrix()
        self.init_pieces()

    def init_matrix(self):
        self.matrix = []
        for y in range(8):
            self.matrix.append([])
            for x in range(8):
                self.matrix[y].append(0)

    def init_pieces(self):
        self.red_pieces = []
        self.black_pieces = []

        for y in range(8):
            for x in range(8):
                if (y < 3):
                    color = 0
                elif (y > 4):
                    color = 1
                else:
                    continue
                if (y%2) == 0:
                    if (x%2) == 0:
                        piece = Piece(self, (y, x), color)
                    else:
                        continue
                else:
                    if (x%2) != 0:
                        piece = Piece(self, (y, x), color)
                    else:
                        continue
                if piece.color:
                    self.black_pieces.append(piece)
                else:
                    self.red_pieces.append(piece)
                self.matrix[y][x] = piece
        self.set_valid_moves()

    def move(self, move):
        start, end, taken = move
        piece = self.matrix[start[0]][start[1]]

        self.matrix[end[0]][end[1]] = piece
        self.matrix[start[0]][start[1]] = 0
        piece.pos = end
        piece.move_count += 1

        if (end[0] == piece.king_row) and not piece.is_king:
            piece.king()

        if taken:
            self.matrix[taken.pos[0]][taken.pos[1]] = 0
            self.get_piece_group(taken.color).remove(taken)
            self.takes = []
            piece.set_valid_moves()
            if self.takes:
                self.turn -= 1

        self.turn += 1
        self.moves.append(move)
        self.set_valid_moves()
        self.game_over = self.is_game_over()

    def undo(self):
        start, end, taken = self.moves[-1]

        piece = self.matrix[end[0]][end[1]]
        self.matrix[start[0]][start[1]] = piece
        piece.pos = start
        piece.move_count -= 1
        self.matrix[end[0]][end[1]] = 0

        if piece.move_count < piece.king_move:
            piece.unking()

        if taken:
            self.matrix[taken.pos[0]][taken.pos[1]] = taken
            self.get_piece_group(taken.color).append(taken)

            if (self.turn%2) == piece.color:
                self.takes = []
                piece.set_valid_moves()
                if self.takes:
                    self.turn += 1

        self.turn -= 1
        self.set_valid_moves()
        self.moves.pop()
        self.game_over = False

    def set_valid_moves(self):
        self.takes = []
        self.valid_moves = []

        for piece in self.get_piece_group(self.turn%2):
            piece.set_valid_moves()
            for move in piece.valid_moves:
                self.valid_moves.append(move)

        if self.takes:
            self.valid_moves = self.takes

    def is_game_over(self):
        if not self.valid_moves:
            if not self.red_pieces:
                return 'black'
            if not self.black_pieces:
                return 'red'
            if self.turn%2:
                return 'red'
            else:
                return 'black'
        return False

    def get_all_pieces(self):
        return self.red_pieces + self.black_pieces

    def get_piece_group(self, group: int):
        if group:
            return self.black_pieces
        return self.red_pieces

    def get_turn(self):
        return self.turn%2

    def square_in_board(self, square: tuple[int, int]):
        x, y = square
        return (-1 < x < 8) and (-1 < y < 8)

    def copy(self):
        new = Board(self.interface)
        for move in self.moves:
            start, end, taken = move
            if taken:
                m = start, end, new.matrix[taken.pos[0]][taken.pos[1]]
            else:
                m = move
            new.move(m)

        return new

class Checkers:

    def __init__(self, fullscreen: bool = True, display: tuple[int, int] = (800, 450)) -> None:
        self.display = self.width, self.height = display
        self.fullscreen = fullscreen
        self.last_game = None
        self.init_display()
        self.init_text()

    def init_display(self):
        pygame.init()
        if self.fullscreen:
            self.display = self.width, self.height = pygame.display.get_desktop_sizes()[0]
        self.screen = pygame.display.set_mode(self.display)
        if self.fullscreen:
            pygame.display.toggle_fullscreen()

        self.square_size = min(self.display)//8
        self.piece_radius = self.square_size//3

        self.in_start_screen = True
        self.in_cpu_screen = False
        self.in_end_screen = False
        self.in_analysis_board = False

        self.background = pygame.image.load(f'wood.jpg').convert()
        self.background = pygame.transform.scale(self.background, self.display)

    def init_game(self):
        self.board = Board(self)
        self.selected = None
        self.cpu_game = False
        self.two_player = False
        self.searching = False

        if self.colors.selected_button.label == 'Red':
            color = 'black'
        elif self.colors.selected_button.label == 'Black':
            color = 'red'
        elif self.colors.selected_button.label == 'CPU Game':
            color = 'red'
            self.cpu_game = True
        else:
            color = 'red'
            self.two_player = True

        self.cpu1 = CPU(round(self.red_slider.value), color)
        self.cpu2 = CPU(round(self.black_slider.value), self.cpu1.opp_color_str)

        self.undone = False

        self.cpu_eval = 0
        self.min_depth = 4
        self.max_depth = 6
        if self.two_player:
            self.max_depth += 1
        self.thread1 = Thread(target=self.background_eval, daemon=True)
        self.thread1.start()
        
        self.parser = None
        self.best_move = self.board.valid_moves[0]
        self.show_hint = False

    def init_text(self):
        self.font = pygame.font.Font(None, self.height//5)
        self.medium_font = pygame.font.Font(None, self.square_size//2)
        self.small_font = pygame.font.Font(None, self.square_size//4)
        self.center_text = Text('space to start', self.font, (self.width//2, self.height//2))
        self.eval_text = Text('0', self.small_font, (self.square_size*8 + self.square_size//4, self.height//2))

        self.menu = Menu((self.width*.1, self.height*.1), (self.width*.8, self.height*.8), self.height//20)
        self.cpu_slider = self.menu.add_slider(10, 1, 0, 'CPU Difficulty')
        self.colors = self.menu.add_button_group(['Red', 'Black', 'CPU Game', '2 Player'], 4)
        self.start_button = self.menu.add_button('START')

        self.menu2 = Menu((self.width*.1, self.height*.1), (self.width*.8, self.height*.8), self.height//20)
        self.red_slider = self.menu2.add_slider(10, 1, 0, 'Red Search Depth')
        self.black_slider = self.menu2.add_slider(10, 1, 0, 'Black Search Depth')

    def start_menu(self):
        self.screen.blit(self.background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        self.menu.update(self.screen)
        self.in_start_screen = not self.start_button.selected
        pygame.display.flip()

    def cpu_menu(self):
        self.screen.blit(self.background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.in_cpu_screen = False
        self.menu2.update(self.screen)
        self.center_text.draw(self.screen)
        pygame.display.flip()

    def end_screen(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_board()
        self.draw_pieces()
        self.center_text.draw(self.screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                self.in_end_screen = False
                if event.key == pygame.K_a:
                    self.in_analysis_board = True

        pygame.display.flip()

    def init_analysis_board(self):
        games = os.listdir(f'{cwd}\demos')
        l = []
        for game in reversed(games):
            l.append(f'{self.timestamp_to_time(game.removesuffix("txt"))[0:6]}...')
        
        analysis_menu = Menu((0, self.height*.2), self.display)
        slider = analysis_menu.add_slider(12, 5, descriptor='ANALYSIS DEPTH')
        button = analysis_menu.add_button('ANALYZE')
        group = analysis_menu.add_button_group(l)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.blit(self.background, (0, 0))
            analysis_menu.update(self.screen)
            if button.selected:
                break
            pygame.display.flip()

        index = group.buttons.index(group.selected_button)
        selected = f'{games[-(index + 1)]}'

        depth = round(slider.value)
        thread2 = Thread(target=self.show_progress, daemon=True)
        self.parser = Game_Viewer(Board, selected, depth)
        thread2.start()

        self.parser.get_analysis()
        self.board = Board(self)
        self.move_set = self.parser.analysis.board.moves

        side_width = self.width - (self.square_size*8.5)
        side_middle = self.width - side_width*.5
        timestamp = self.timestamp_to_time(self.parser.filename.removesuffix('.txt'))

        self.cpu_eval = 0
        self.label_text = Text('', self.medium_font, (side_middle, self.height * .9))
        self.summary = Game_Summary(self.parser.analysis, (side_middle - side_width*.5, self.height*.05), (side_width, self.height*.8), self.parser.gameinfo, timestamp)
        
    def timestamp_to_time(self, timestamp: str):
        date, time = timestamp.split('_')
        year, month, day = date.split('-')
        hour, minute, second, millisecond = time.split('-')

        result = f'{month}/{day}/{year}, {hour}:{minute}'
        return result

    def analysis_board(self):
        index = len(self.board.moves)
        self.show_hint = pygame.key.get_pressed()[pygame.K_h]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if index < len(self.parser.analysis.analysis):
                        move = self.move_set[len(self.board.moves)]
                        if move[-1]:
                            move = move[0], move[1], self.board.matrix[move[-1].pos[0]][move[-1].pos[1]]
                        self.board.move(move)

                elif event.key == pygame.K_LEFT:
                    if self.board.moves:
                        self.board.undo()
                
                elif event.key == pygame.K_ESCAPE:
                    self.in_analysis_board = False

                elif event.key == pygame.K_a:
                    self.init_analysis_board()

        if index < len(self.parser.analysis.analysis):
            self.cpu_eval = round(self.parser.analysis.analysis[index][2], 1)
            self.best_move = self.parser.analysis.analysis[index][1]
            s = ''
            if index > 0:
                for label in self.parser.analysis.analysis[index - 1][-1]:
                    s += f'{label.replace("_", " ")}, '
                s = s.removesuffix(', ')

            self.label_text.set_text(s)

        self.screen.blit(self.background, (0, 0))
        self.draw_board()
        self.draw_eval_bar()
        self.show_last_move()
        self.show_best_move()
        if self.selected:
            self.draw_valid_moves(self.selected)
        self.draw_pieces()

        self.summary.draw(self.screen)
        self.label_text.draw(self.screen)
        pygame.display.flip()

    def show_progress(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.blit(self.background, (0, 0))

            # self.board = self.parser.analysis.board
            # self.parser.analysis.board.interface = self
            # self.draw_board()
            # self.draw_pieces()

            self.center_text.set_text(f'Analyzing Game {int(self.parser.analysis.progress*100)}%')
            self.center_text.draw(self.screen)
            pygame.display.flip()
            if self.parser.analysis.progress >= 1:
                break

    def draw_board(self):
        for y in range(8):
            for x in range(8):
                if (y % 2) == 0:
                    if (x % 2) == 0:
                        color = green
                    else:
                        color = grey
                else:
                    if (x % 2) == 0:
                        color = grey
                    else:
                        color = green
                pos = x * self.square_size, (7 - y) * self.square_size
                rect = pygame.rect.Rect(pos[0], pos[1], self.square_size, self.square_size)

                pygame.draw.rect(self.screen, color, rect)

    def highlight_squares(self, squares, color = red):
        for square in squares:
            pos = self.to_pixel_pos(square)
            pygame.draw.rect(self.screen, color, pygame.Rect(pos[0], pos[1], self.square_size, self.square_size))

    def show_last_move(self):
        if self.board.moves:
            start, end, taken = self.board.moves[-1]
            squares = [start, end]
            self.highlight_squares(squares)

    def show_best_move(self):
        if self.show_hint:
            self.highlight_squares([self.best_move[0], self.best_move[1]], blue)

    def draw_pieces(self):
        for piece in self.board.get_all_pieces():
            if (piece != self.selected) or not pygame.mouse.get_pressed()[0]:
                piece.draw()

        if (self.selected) and (pygame.mouse.get_pressed()[0]):
                pos = pygame.mouse.get_pos()
                pygame.draw.circle(self.screen, self.selected.rgb, pos, self.piece_radius)
                if self.selected.is_king:
                    pygame.draw.circle(self.screen, white, pos, self.piece_radius//3)

    def draw_valid_moves(self, piece: Piece):
        moves = piece.valid_moves
        if self.board.takes:
            moves = []
            for take in self.board.takes:
                if take[0] == piece.pos:
                    moves.append(take)

        for move in moves:
            pygame.draw.circle(self.screen, bright_red, self.to_pixel_pos((move[1][0] - .5, move[1][1] + .5)), self.piece_radius//2)

    def draw_eval_bar(self):
        x = self.square_size*8
        middle = (self.height//2) - (self.cpu_eval / 14)*self.height
        bar_width = self.square_size/2

        rect1 = pygame.rect.Rect(x, 0, bar_width, middle)
        rect2 = pygame.rect.Rect(x, middle, bar_width, self.height - middle + 10)
        pygame.draw.rect(self.screen, black, rect1)
        pygame.draw.rect(self.screen, dark_red, rect2)

        if self.cpu_eval < 0:
            y = self.square_size//4
        else:
            y = self.height - self.square_size//4

        if abs(self.cpu_eval) > 100:
            text = f'M{int(1000 - abs(self.cpu_eval/self.cpu1.multiplier)) + 1}'
        else:
            text = f'{abs(self.cpu_eval)}'

        self.eval_text.set_text(text)
        self.eval_text.set_center((self.square_size*8 + self.square_size//4, y))
        self.eval_text.draw(self.screen)

    def update_display(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_board()
        self.draw_eval_bar()
        self.show_last_move()
        self.show_best_move()
        if self.selected:
            self.draw_valid_moves(self.selected)
        self.draw_pieces()
        pygame.display.flip()

    def update(self):
        self.update_display()
        turn = self.board.get_turn()

        pressed = pygame.key.get_pressed()
        self.show_hint = pressed[pygame.K_h]

        if (turn == self.cpu2.color) and self.cpu_game:
            move, value = self.cpu2.find_best_move(self.board.copy())
            if move[-1]:
                move = move[0], move[1], self.board.matrix[move[-1].pos[0]][move[-1].pos[1]]
            self.board.move(move)

        if (turn != self.cpu1.color) or self.undone or self.two_player:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            
                if (event.type == pygame.MOUSEBUTTONDOWN) and not self.cpu_game:
                    click = pygame.mouse.get_pos()
                    square = self.to_game_pos(click)
                    if self.board.square_in_board(square):
                        piece = self.board.matrix[square[0]][square[1]]
                        if self.selected:
                            moves = self.selected.valid_moves
                            if self.board.takes:
                                moves = self.board.takes
                            moved = False
                            for move in moves:
                                if (square == tuple(move[1])) and (self.selected.pos == move[0]):
                                    self.board.move(move)
                                    moved = True
                                    self.undone = False
                            
                            if square == self.selected.pos:
                                self.selected = None
                            elif (not moved) and piece:
                                if piece.color == self.selected.color:
                                    self.selected = piece
                            else:
                                self.selected = None

                        else:
                            if piece and (piece.color == turn):
                                self.selected = piece

                elif event.type == pygame.MOUSEBUTTONUP:
                    click = pygame.mouse.get_pos()
                    square = self.to_game_pos(click)
                    if self.board.square_in_board(square):
                        piece = self.board.matrix[square[0]][square[1]]
                        if self.selected:
                            moves = self.selected.valid_moves
                            if self.board.takes:
                                moves = self.board.takes
                            moved = False
                            for move in moves:
                                if (square == tuple(move[1])) and (self.selected.pos == move[0]):
                                    self.board.move(move)
                                    moved = True
                                    self.selected = None
                                    self.undone = False

                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE) and (self.board.moves):
                        self.board.undo()
                        self.undone = True
                        self.selected = None

        elif (turn == self.cpu1.color) and not self.two_player:
            move, value = self.cpu1.find_best_move(self.board.copy())
            if move[-1]:
                move = move[0], move[1], self.board.matrix[move[-1].pos[0]][move[-1].pos[1]]
            self.board.move(move)

    def to_game_pos(self, pos: tuple[int, int]):
        x, y = pos
        x = math.floor(x/self.square_size)
        y = math.floor(y/self.square_size)
        y = 7 - y
        return y, x

    def to_pixel_pos(self, pos: tuple[int, int]):
        y, x = pos
        y = (7 - y) * self.square_size
        x = x * self.square_size
        return x, y

    def reset(self):
        self.init_text()
        self.in_start_screen = True

    def save_game(self):
        filename = f'{str(datetime.datetime.now()).replace(" ", "_").replace(":", "-").replace(".", "-")}.txt'
        file = open(f'{cwd}\demos\{filename}', 'x')
        for move in self.board.moves:
            if move[-1]:
                file.write(f'{move[0]}: {move[1]}: {move[2].pos};')
            else:
                file.write(f'{move[0]}: {move[1]}: {move[1]};')
        file.write('\n')

        if self.cpu_game:
            gameinfo = f'Red Cpu Depth {self.cpu1.depth} vs Black Cpu Depth {self.cpu2.depth}'
        elif self.two_player:
            gameinfo = f'Red Player vs Black Player'
        else:
            if self.cpu1.color:
                gameinfo = f'Red Player vs Black Cpu Depth {self.cpu1.depth}'
            else:
                gameinfo = f'Red Cpu Depth {self.cpu1.depth} vs Black Player'
        file.write(gameinfo)
        file.close()
        self.last_game = filename

    def background_eval(self):
        depth = self.min_depth
        eval_cpu = CPU(self.min_depth)
        board = self.board.copy()
        while not self.board.game_over:
            if self.board.turn != board.turn:
                depth = self.min_depth
                board = self.board.copy()

            if (depth <= self.max_depth):
                eval_cpu.depth = depth
                if board.get_turn():
                    eval_cpu.set_color('black')
                else:
                    eval_cpu.set_color('red')

                move, val, = eval_cpu.find_best_move(board, False, False, False)
                self.best_move = move
                if eval_cpu.color:
                    val *= -1
                self.cpu_eval = val
                depth += 1
                self.draw_eval_bar()
                pygame.display.update(pygame.Rect(self.square_size*8, 0, self.square_size/2, self.height))

    def gameloop(self):
        while True:
            while self.in_start_screen:
                self.start_menu()

            self.in_cpu_screen = self.colors.buttons[-2].selected
            self.red_slider.set_value(self.cpu_slider.value)
            self.black_slider.set_value(self.cpu_slider.value)

            while self.in_cpu_screen:
                self.cpu_menu()

            self.init_game()
            while not self.board.game_over:
                self.update()

            self.save_game()
            self.center_text.set_text(f'{self.board.game_over} wins')
            self.in_end_screen = True

            while self.in_end_screen:
                self.end_screen()

            if self.in_analysis_board:
                self.init_analysis_board()
            while self.in_analysis_board:
                self.analysis_board()

            self.reset()