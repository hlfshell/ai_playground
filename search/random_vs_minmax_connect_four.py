from connect_four_board import Connect4Board
from random_connect_four import RandomBot
from min_max_connect_four import MinMaxBot

random_wins = 0
minmax_wins = 0
draws = 0

images = []

for round in range(0, 100):
    game = Connect4Board(6,7)
    random = RandomBot(game, '1')
    minmax = MinMaxBot(game, '2', depth = 4)

    player1 = True
    turn = 1
    while game.winner() is None:
        if player1:
            random.move()
        else:
            minmax.move()
        player1 = False if player1 else True

        game.store_im()

    winner = game.winner()
    if game.winner() is not None:
        if winner == 'draw':
            print(f"Round {round+1} ends in a draw")
            draws += 1
        elif winner == '1':
            print(f"Round {round+1} is won by random bot")
            random_wins += 1
        else:
            print(f"Round {round+1} is won by minmax bot")
            minmax_wins += 1

    # Save game progress as images
    images = images + game.images
    # Hang on the "end" image for five frames
    for i in range(1, 5):
        images.append(game.images[-1])

print(f"Draws: {draws} | Random Wins: {random_wins} | Minmax Wins: {minmax_wins}")
    
images[0].save("./out/random_vs_minmax.gif", save_all=True, append_images=images, duration=100, loop=0)