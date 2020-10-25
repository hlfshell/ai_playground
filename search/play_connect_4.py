from connect_four_board import Connect4Board

game = Connect4Board(5,5)

game.print()

player1 = True

while game.winner() is None:
    move = int(input("Move? "))
    game.move('1' if player1 else '2', move)
    player1 = False if player1 else True
    game.print()

if game.winner() == 'Draw':
    print("Draw!")
else:
    print(f"Player {game.winner()} is the winner!")