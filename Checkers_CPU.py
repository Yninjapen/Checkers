import numpy
import time
square_map = [[1, 1, 1, 1, 1, 1, 1, 1],
              [1, 0, 0, 0, 0, 0, 0, 1],
              [2, 0, 0, 0, 0, 0, 0, 2],
              [2, 0, 0, 0, 0, 0, 0, 2],
              [3, 0, 0, 0, 0, 0, 0, 3],
              [3, 0, 0, 0, 0, 0, 0, 3],
              [4, 0, 0, 0, 0, 0, 0, 4],
              [5, 3, 2, 2, 2, 2, 3, 5]]

class CPU:

    def __init__(self, search_depth: int = 1, color: str = 'red'):
        self.depth = search_depth
        self.color_str = color
        if color == 'red':
            self.color = 0
            self.opponent = 1
            self.opp_color_str = 'black'
        else:
            self.color = 1
            self.opponent = 0
            self.opp_color_str = 'red'

        self.piece_weight = .65 #.6
        self.move_weight = .2 #.2
        self.pos_weight = .05 #.1
        self.range_weight = .1 #.1

        self.piece_variation = .2 #.2
        self.move_variation = .05 #.1
        self.pos_variation = .3 #.2
        self.range_variation = .1 #.1

    def set_color(self, color: str):
        self.color_str = color
        if color == 'red':
            self.color = 0
            self.opponent = 1
            self.opp_color_str = 'black'
        else:
            self.color = 1
            self.opponent = 0
            self.opp_color_str = 'red'

    def evaluate(self, board):
        result = board.game_over
        if result:
            if result == self.color_str:
                return 1000
            if result == self.opp_color_str:
                return -1000
            else:
                return 0

        pieces = board.get_piece_group(self.color)
        opp_pieces = board.get_piece_group(self.opponent)
        piece_count = (len(pieces) + len(opp_pieces))
        game_development = (piece_count - 12)/12
        piece_val = 0
        opp_piece_val = 0
        move_val = 0
        opp_move_val = 0
        pos_val = 0
        opp_pos_val = 0

        player_columns = set()
        opp_columns = set()

        for piece in pieces:
            piece_val += piece.value
            move_val += len(piece.valid_moves)
            pos_val += square_map[(piece.pos[0]+self.color)*piece.direction][piece.pos[1]]*game_development
            player_columns.add(piece.pos[1])

        for piece in opp_pieces:
            opp_piece_val += piece.value
            opp_move_val += len(piece.valid_moves)
            opp_pos_val += square_map[(piece.pos[0]+self.opponent)*piece.direction][piece.pos[1]]*game_development
            opp_columns.add(piece.pos[1])
 
        p_diff = player_columns - opp_columns
        opp_diff = opp_columns - player_columns
        return ((piece_val - opp_piece_val)/12)*(self.piece_weight + self.piece_variation*((24 - piece_count)/24)) + ((move_val - opp_move_val)/10)*(self.move_weight - self.move_variation*abs(game_development)) + ((pos_val/piece_val) - (opp_pos_val/opp_piece_val)) * self.pos_weight + ((len(p_diff) - len(opp_diff))/3) * (self.range_weight - self.range_variation*max(game_development, 0))
    
    def minimax(self, board, depth: int, alpha, beta):
        score = self.evaluate(board)

        if score == 1000:
            return score - (self.depth - depth)
        if score == -1000:
            return score + (self.depth - depth)
        if board.game_over:
            return 0
        
        if depth == 0:
            return score

        if (board.turn%2) == self.color:
            bestVal = -10000
            valid_moves = board.valid_moves
            for move in valid_moves:
                board.move(move)
                bestVal = max(bestVal, self.minimax(board, depth - 1, alpha, beta))
                alpha = max(alpha, bestVal)
                board.undo()

                if beta <= alpha:
                    break
            return bestVal
        
        else:
            bestVal = 10000
            valid_moves = board.valid_moves
            for move in valid_moves:
                board.move(move)
                bestVal = min(bestVal, self.minimax(board, depth - 1, alpha, beta))
                beta = min(beta, bestVal)
                board.undo()

                if beta <= alpha:
                    break
            return bestVal
    
    def find_best_move(self, board, wait: bool = True, return_all: bool = False, feedback = True):
        if feedback:
            print('calculating best move...')
        start = time.time()
        bestVal = -10000
        bestMove = -1
        valid_moves = board.valid_moves

        ordered_moves = []
        alpha = -10000
        beta = 10000
        for move in valid_moves:
            board.move(move)
            moveVal = self.minimax(board, self.depth, alpha, beta)

            if moveVal > bestVal:
                bestVal = moveVal
                bestMove = move

            if ordered_moves:# creates list of moves in order of how good they are
                inserted = False
                for i in range(len(ordered_moves)):
                    m, v = ordered_moves[i]
                    if (moveVal*20) > v:
                        ordered_moves.insert(i, (move, moveVal*20))
                        inserted = True
                        break
                if not inserted:
                    ordered_moves.append((move, moveVal*20))
            else:
                ordered_moves.append((move, moveVal*20))

            alpha = max(alpha, bestVal)

            board.undo()
        
        end = time.time()
        elapsed = end - start
        if feedback:
            print(f'best move for {self.color_str} is {bestMove}, with a value of {round(bestVal*20, 1)}')
            print(f'time elapsed:', numpy.round(elapsed, 1), 'seconds')

        if (elapsed < 1) and wait:
            time.sleep(1)
        if return_all:
            return ordered_moves
        return bestMove, round(bestVal*20, 1)