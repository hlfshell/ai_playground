from connect_four_board import Connect4Board
from a_star import OrderedQueue
from random import choice

class MinMaxBot():

    def __init__(self, board : Connect4Board, player : str, depth : int = 4):
        self.board = board
        self.player = player
        self.depth = depth

    def move(self):
        move, score = self.minmax(depth = 0)
        self.board.move(self.player, move)

    # Given an x/y coordinate, see if in any direction (2 in each)
    # how many ways does 3 in a row get achieved (assuming that position
    # was also set to the same value
    def threes_counter(self, row, col):
        threes = 0

        topmost = row - 2 if row - 2 >= 0 else 0
        leftmost = col - 2 if col - 2 >= 0 else 0
        bottommost = row + 2 if row + 2 < self.rows else self.rows - 1
        rightmost = col + 2 if col + 2 >= self.cols else self.cols - 1

        # Horizontal left endcap OOX
        if col - leftmost == 2:
            a = self.board.values[row][leftmost]
            b = self.board.values[row][col - 1]
            c = self.board.values[row][col]
            if a == b and b == c:
                threes += 1

        # Horizontal mid OXO
        if leftmost != col and rightmost != col:
            a = self.board.values[row][col - 1]
            b = self.board.values[row][col]
            c = self.board.values[row][col + 1]
            if a == b and b == c:
                threes += 1

        # Horizontal right XOO
        if rightmost - col == 2:
            a = self.board.values[row][col]
            b = self.board.values[row][col + 1]
            c = self.board.values[row][rightmost]
            if a == b and b == c:
                threes += 1

        

        return threes

            


    def minmax(self, state : Connect4Board = None, max : bool = True, depth : int = 0, move : int = None) -> (int, int):
        # state is only blank on the first
        # call, so use our real state
        if state is None:
            state = self.board

        # the current player is the bot if max
        # the opponent if min
        player = self.player if max else '2' if self.player == '1' else '1'

        # if we've reached our max depth or hit an end state
        # let's return our score
        winner = state.winner()
        if depth == self.depth or winner is not None:
            if winner == 'draw':
                return move, 0 - depth
            elif winner == self.player:
                return move, 20 - depth
            elif winner is not None:
                return move, -(20 - depth)
            else:
                return move, 0 - self.depth

        moveset = OrderedQueue(reverse=max)

        for move in state.possible_moves():
            clone = state.clone()
            clone.images=[] # This is just to save memory
            clone.move(self.player if max else '1' if self.player != '1' else '2', move)
            _, score = self.minmax(clone, max = not max, depth = depth+1, move = move)
            moveset.append(move, score)

        move_score = moveset.pop()
        best_moves = [move_score[0]]
        best_score = move_score[1]
        
        while True:
            move_score = moveset.pop()
            if move_score is None:
                break
            if move_score[1] == best_score:
                best_moves.append(move_score[0])
        next_move = choice(best_moves)

        return next_move, best_score
                

