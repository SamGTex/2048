import methods.game as game
import numpy as np

if __name__ == '__main__':
    # create 4x4 display
    display = np.zeros((4,4), dtype=int) #int 64

    # information for user
    print('-------------------------')
    print('Welcome to 2048!\n')
    print('Control:')
    print('  W')
    print('A S D\n')
    print('Quit: CTR + C\n')
    print('Lets go and good luck!')
    print('-------------------------')
    display = game.generate_2_4(display)

    while True:
        # generate a new 2 or 4
        display = game.generate_2_4(display)

        # show state
        print(display)

        # get input
        control = game.input_request()

        # update grid
        display = game.update_grid(display, control)

        # check if game is over
        if game.check_game_over(display):
            print('Game Over!')
            break
        
        # check if game is won
        if game.check_game_won(display):
            print('You won!')
            break