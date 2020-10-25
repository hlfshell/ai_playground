from connect_four_board import Connect4Board
from random import choice

class RandomBot():

    def __init__(self, board : Connect4Board, player : str):
        self.board = board
        self.player = player

    def move(self):
        move = choice(self.board.possible_moves())
        self.board.move(self.player, move)