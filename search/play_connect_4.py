from connect_four_board import Connect4Board
from random_connect_four import RandomBot

game = Connect4Board(5,5)

player1 = True

random_bot = RandomBot(game, '2')
while game.winner() is None:
    if player1:
        game.print()
        move = int(input("Move? "))
        game.move('1', move)
    else:
        random_bot.move()
    player1 = False if player1 else True
    game.store_im()
if not player1:
    game.print()

if game.winner() == 'Draw':
    print("Draw!")
else:
    print(f"Player {game.winner()} is the winner!")

game.write_gif('out/random_bot.gif')