from connect_four_board import Connect4Board
from random_connect_four import RandomBot
from min_max_connect_four import MinMaxBot

game = Connect4Board(6,7)

player1 = True
bot = MinMaxBot(game, '2')
# bot = RandomBot(game, '2')
turn = 1
while game.winner() is None:
    print(f"==== Turn {turn} ====")
    game.print()
    if player1:
        move = int(input("Move? "))
        game.move('1', move)
    else:
        bot.move()
    player1 = False if player1 else True
    game.store_im()
    turn += 1
game.print()

if game.winner() == 'draw':
    print("Draw!")
else:
    print(f"Player {game.winner()} is the winner!")
    game.print()
game.write_gif('out/random_bot.gif')