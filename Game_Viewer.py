import pygame
import os
import math
from Checkers_CPU import CPU
from pygame_text import Text

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

class Analysis:

    def __init__(self, game: list, depth: int, b):
        self.game = game
        self.depth = depth

        self.red_acc_val = 0
        self.black_acc_val = 0

        self.red_total_moves = 0
        self.black_total_moves = 0

        self.red_missed_wins = 0
        self.black_missed_wins = 0

        self.red_best_moves = 0
        self.black_best_moves = 0

        self.red_brilliants = 0
        self.black_brilliants = 0

        self.red_blunders = 0
        self.black_blunders = 0

        self.red_mistakes = 0
        self.black_mistakes = 0

        self.progress = 0

        self.b = b
        self.board = self.b(self)
        self.cpu = CPU(self.depth)

    def analzye_move(self, move, board):
        self.cpu = CPU(self.depth)
        labels = []
        turn = board.get_turn()
        if turn:
            color = 'black'
            self.black_total_moves += 1
        else:
            color = 'red'
            self.red_total_moves += 1
        self.cpu.set_color(color)

        m = move
        l = self.cpu.find_best_move(board, False, True, False)

        self.cpu.depth = math.ceil(self.cpu.depth/2)
        half_search = self.cpu.find_best_move(board, False, True, False)
        half_best, half_val = half_search[0]

        bestMove, bestVal = l[0]
        worstMove, worstVal = l[-1]
        if len(l) > 1:
            nextbestVal = l[1][1]
        else:
            nextbestVal = None

        for i in range(len(l)):
            if l[i][0] == list(m):
                index = i
                moveVal = l[i][1]
                break

        r = bestVal - worstVal
        if r != 0:
            acc_val = (moveVal - worstVal)/r
        else:
            acc_val = 1

        if acc_val < .5:
            labels.append('inaccuracy')

        if turn:
            self.black_acc_val += acc_val
        else:
            self.red_acc_val += acc_val

        if ((bestMove[0], bestMove[1]) == (move[0], move[1])) and (len(l) > 1):
            labels.append('best_move')
            if turn:
                self.black_best_moves += 1
            else:
                self.red_best_moves += 1
            if ((moveVal - nextbestVal >= 1) and (moveVal + 1 > 0) and (moveVal - half_val >= 1)):
                labels.append('brilliant')
                if turn:
                    self.black_brilliants += 1
                else:
                    self.red_brilliants += 1
        else:
            if (bestVal > 100) and (moveVal < 100):
                labels.append('missed_win')
                if turn:
                    self.black_missed_wins += 1
                else:
                    self.red_missed_wins += 1
            if (bestVal - moveVal >= 1):
                labels.append('blunder')
                if turn:
                    self.black_blunders += 1
                else:
                    self.red_blunders += 1

            if (bestVal - moveVal >= .5):
                labels.append('mistake')
                if turn:
                    self.black_mistakes += 1
                else:
                    self.red_mistakes += 1

        if self.cpu.color:
            moveVal *= -1
        return (move, bestMove, moveVal, labels)

    def analyze_game(self):
        self.board = self.b(self)

        result = []

        self.red_acc_val = 0
        self.black_acc_val = 0

        self.red_total_moves = 0
        self.black_total_moves = 0

        self.red_missed_wins = 0
        self.black_missed_wins = 0

        self.red_best_moves = 0
        self.black_best_moves = 0

        self.red_brilliants = 0
        self.black_brilliants = 0

        self.red_blunders = 0
        self.black_blunders = 0

        self.red_mistakes = 0
        self.black_mistakes = 0

        for i, move in enumerate(self.game):
            m = move[0], move[1], self.board.matrix[move[2][0]][move[2][1]]
            a, bestMove, moveVal, labels = self.analzye_move(m, self.board)

            if bestMove[-1]:
                bestMove = bestMove[0], bestMove[1], (bestMove[2].pos[0], bestMove[2].pos[1])
            else:
                bestMove = bestMove[0], bestMove[1], bestMove[1]

            result.append((move, bestMove, moveVal, labels))
            self.board.move(m)
            self.progress = i/(len(self.game) - 1)

        self.red_acc_val = round(100*self.red_acc_val/self.red_total_moves, 1)
        self.black_acc_val = round(100*self.black_acc_val/self.black_total_moves, 1)

        self.analysis = result
        return self.analysis

    def get_end_state_board(self):
        self.board = self.b(self)
        for data in self.analysis:
            start, end, taken = move = data[0]
            move = start, end, self.board.matrix[taken[0]][taken[1]]
            self.board.move(move)
        return self.board

    def __str__(self) -> str:
        s1 = f'RED:\n   ACCURACY: {self.red_acc_val}%\n   BEST MOVES: {self.red_best_moves}\n   BRILLIANT MOVES: {self.red_brilliants}\n   MISTAKES: {self.red_mistakes}\n   BLUNDERS: {self.red_blunders}\n   MISSED WINS: {self.red_missed_wins}\n'
        s2 = f'BLACK:\n   ACCURACY: {self.black_acc_val}%\n   BEST MOVES: {self.black_best_moves}\n   BRILLIANT MOVES: {self.black_brilliants}\n   MISTAKES: {self.black_mistakes}\n   BLUNDERS: {self.black_blunders}\n   MISSED WINS: {self.black_missed_wins}'
        return s1 + s2

class Game_Viewer:
    def __init__(self, b, filename: str, depth: int = 5) -> None:
        self.filename = filename
        self.depth = depth
        self.moves = self.unpack_game()
        self.b = b
        self.analysis = Analysis(self.moves, depth, b)

    def get_analysis(self):
        pre_analyzed = os.listdir(f'{cwd}\game_analysis')
        analyzed = False
        for filename in pre_analyzed:
            name = f'{filename.removesuffix("_analysis.txt")}.txt'
            if name == self.filename:
                analyzed = True
                break
        
        if analyzed:
            self.analysis = self.unpack_analysis(filename)
            if self.analysis.depth < self.depth:
                self.analysis.depth = self.depth
                self.analysis.analyze_game()
                self.save_analysis(self.analysis)
            self.analysis.progress = 1
        else:
            self.analysis.analyze_game()
            self.save_analysis(self.analysis)
        return self.analysis

    def unpack_game(self):
        self.game_file = open(f'{cwd}\\demos\\{self.filename}', 'r')
        moves = self.game_file.readline()
        self.gameinfo = self.game_file.readline()
        self.game_file.close()

        moves.strip('\n')
        moves = moves.strip().split(';')
        moves.pop()
        result = []
        for move in moves:
            l = []
            for pos in move.strip().split(':'):
                x1, y1 = pos.split(',')
                x1 = int(x1.strip()[-1])
                y1 = int(y1.strip()[0])
                l.append((x1, y1))
            result.append(l)

        return result

    def unpack_analysis(self, filename: str):
        file = open(f'{cwd}\game_analysis\{filename}', 'r')
        stat_line = file.readline().removesuffix('\n').strip()
        original_file = file.readline().removesuffix('\n').strip()
        depth = int(file.readline().removesuffix('\n').strip())

        moves = []
        for line in file.readlines():
            move, bestMove, val, labels = line.split(';')
            l = []
            for c in move:
                if c.isnumeric():
                    l.append(int(c))
            
            m = (l[0], l[1]), (l[2], l[3]), (l[4], l[5])
            
            l = []
            for c in bestMove:
                if c.isnumeric():
                    l.append(int(c))
            
            b = (l[0], l[1]), (l[2], l[3]), (l[4], l[5])

            value = float(val.strip())
            labels = labels.replace('[', '').replace(']', '').strip().split(',')
            l = []
            for label in labels:
                l.append(label.replace("'", '').strip())
            labels = l
            moves.append((m, b, value, labels))

        file.close()

        red_stats, black_stats = stat_line.split(';')
        red_stats = red_stats.strip().split(',')
        black_stats = black_stats.strip().split(',')

        result = Analysis(self.moves, self.analysis.depth, self.b)
        result.analysis = moves
        result.depth = depth

        result.red_total_moves = int(red_stats[0])
        result.red_acc_val = float(red_stats[1])
        result.red_best_moves = int(red_stats[2])
        result.red_brilliants = int(red_stats[3])
        result.red_mistakes = int(red_stats[4])
        result.red_blunders = int(red_stats[5])
        result.red_missed_wins = int(red_stats[6])

        result.black_total_moves = int(black_stats[0])
        result.black_acc_val = float(black_stats[1])
        result.black_best_moves = int(black_stats[2])
        result.black_brilliants = int(black_stats[3])
        result.black_mistakes = int(black_stats[4])
        result.black_blunders = int(black_stats[5])
        result.black_missed_wins = int(black_stats[6])

        result.get_end_state_board()
        return result

    def save_analysis(self, analysis: Analysis):
        file = open(f'{cwd}\game_analysis\{self.filename.removesuffix(".txt")}_analysis.txt', 'w')

        red_stat_str = f'{analysis.red_total_moves},{analysis.red_acc_val},{analysis.red_best_moves},{analysis.red_brilliants},{analysis.red_mistakes},{analysis.red_blunders},{analysis.red_missed_wins}'
        black_stat_str = f'{analysis.black_total_moves},{analysis.black_acc_val},{analysis.black_best_moves},{analysis.black_brilliants},{analysis.black_mistakes},{analysis.black_blunders},{analysis.black_missed_wins}'

        file.write(f'{red_stat_str};{black_stat_str}\n')
        file.write(f'{self.filename}\n')
        file.write(f'{analysis.depth}\n')
        for move in self.analysis.analysis:
            file.write(f'{move[0]};{move[1]};{move[2]};{move[3]}\n')

        file.close()

class Game_Summary:

    def __init__(self, analysis: Analysis, position: tuple[int, int], dimensions: tuple[int, int], game_info: str = '', game_timestamp: str = '') -> None:
        self.analysis = analysis
        self.position = self.x, self.y = position
        self.display = self.width, self.height = dimensions
        self.game_info = game_info
        self.timestamp = game_timestamp
        self.init_text()
        self.init_rects()

    def init_text(self):
        self.center = self.center_x, self.center_y = self.x + self.width//2, self.y + self.height//2
        self.increment = self.height // 10
        self.mid_left_x = self.x + self.width//4
        self.mid_right_x = self.x + self.width*.75

        self.big_font = pygame.font.Font(None, int(self.height//10))
        self.font = pygame.font.Font(None, int(self.height//18))
        self.small_font = pygame.font.Font(None, int(self.height//20))

        self.top_text = Text('GAME SUMMARY', self.big_font, (self.center_x, self.y + self.increment))
        self.matchup_text = Text(self.game_info, self.small_font, (self.center_x, self.y + self.increment*9))
        self.time_text = Text(self.timestamp, self.small_font, (self.center_x, self.y + self.increment * 9.5))

        self.red_acc_text = Text(f'{self.analysis.red_acc_val}% Acc', self.font, (self.mid_left_x,self.y + self.increment*3))
        self.red_best_text = Text(f'{self.analysis.red_best_moves} Best Moves', self.font, (self.mid_left_x, self.y + self.increment*4))
        self.red_brilliant_text = Text(f'{self.analysis.red_brilliants} Brilliant Moves', self.font, (self.mid_left_x, self.y + self.increment * 5))
        self.red_mistake_text = Text(f'{self.analysis.red_mistakes} Mistakes', self.font, (self.mid_left_x, self.y + self.increment * 6))
        self.red_blunder_text = Text(f'{self.analysis.red_blunders} Blunders', self.font, (self.mid_left_x, self.y + self.increment * 7))
        self.red_missed_win_text = Text(f'{self.analysis.red_missed_wins} Missed Wins', self.font, (self.mid_left_x, self.y + self.increment * 8))

        self.black_acc_text = Text(f'{self.analysis.black_acc_val}% Acc', self.font, (self.mid_right_x,self.y + self.increment*3))
        self.black_best_text = Text(f'{self.analysis.black_best_moves} Best Moves', self.font, (self.mid_right_x, self.y + self.increment*4))
        self.black_brilliant_text = Text(f'{self.analysis.black_brilliants} Brilliant Moves', self.font, (self.mid_right_x, self.y + self.increment * 5))
        self.black_mistake_text = Text(f'{self.analysis.black_mistakes} Mistakes', self.font, (self.mid_right_x, self.y + self.increment * 6))
        self.black_blunder_text = Text(f'{self.analysis.black_blunders} Blunders', self.font, (self.mid_right_x, self.y + self.increment * 7))
        self.black_missed_win_text = Text(f'{self.analysis.black_missed_wins} Missed Wins', self.font, (self.mid_right_x, self.y + self.increment * 8))

        self.all_text = [self.top_text, self.matchup_text, self.time_text, self.red_acc_text, self.red_best_text, self.red_brilliant_text,
                        self.red_mistake_text, self.red_blunder_text, self.red_missed_win_text, self.black_acc_text, self.black_best_text,
                        self.black_brilliant_text, self.black_mistake_text, self.black_blunder_text, self.black_missed_win_text]

    def init_rects(self):
        self.red_rect = pygame.Rect(self.x, self.y, self.width//2, self.increment*8.5)
        self.black_rect = pygame.Rect(self.center_x, self.y, self.width//2, self.increment*8.5)
        self.big_rect = pygame.Rect(self.x, self.y, self.width, self.increment*8.5)

        self.bg_color = green

    def draw_rects(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.big_rect)
        pygame.draw.rect(screen, red, self.red_rect)
        pygame.draw.rect(screen, black, self.black_rect)

    def draw_text(self, screen):
        for text in self.all_text:
            text.draw(screen)

    def draw(self, screen):
        self.draw_rects(screen)
        self.draw_text(screen)