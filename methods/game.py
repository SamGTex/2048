import numpy as np

# ----- console -----
# request for user input: wasd
def input_request():
    while True:
        control = input('Your move: ').upper()
        if control == 'W' or control == 'A' or control == 'S' or control == 'D':
            return control
        print('Ungültige Eingabe!\n Steuerung:')
        print('  W')
        print('A S D')


# ----- game -----  
def create_initial_board():
    display = np.zeros((4,4), dtype=int) #int 64
    return display

# create number 2 (90%) and 4 (10%) in a random empty field
def generate_2_4(display):
    pos_empty_fields_row, pos_empty_fields_col = np.where(display==False)

    rnd_pos = np.random.randint(0, pos_empty_fields_row.shape[0])

    pos_row_two = pos_empty_fields_row[rnd_pos]
    pos_col_two = pos_empty_fields_col[rnd_pos]

    # 10% propability to get a 4
    if np.random.rand() > 0.1:
        display[pos_row_two, pos_col_two] = 2
    else:
        display[pos_row_two, pos_col_two] = 4

    return display


# sum pairs and move if next field is empty
def apply_action(A):
    
    k = 3
    A_result = np.zeros(4, dtype=int)
    for i in range(4):
        if A[3-i] != 0:
            A_result[k] = A[3-i]
            k -= 1
    A = A_result


    if A[0] == A[1] and A[2] == A[3]:
        A[3] *= 2
        A[2] = 2*A[1]
        A[1] = 0
        A[0] = 0

    elif A[2] == A[3]:
        A[3] *= 2
        A[2] = A[1]
        A[1] = A[0]
        A[0] = 0

    elif A[1] == A[2]:
        A[2] *= 2
        A[1] = A[0]
        A[0] = 0

    elif A[0] == A[1]:
        A[1] *= 2
        A[0] = 0

    return A

def update_grid(display, control):
    if control.upper() == 'A':
        for row in range(4):
            A = display[row,:]
            A = A[::-1]
            A_moved = apply_action(A)
            display[row,:] = A_moved[::-1]

    elif control.upper() == 'D':
        for row in range(4):
            A = display[row,:]
            A_moved = apply_action(A)
            display[row,:] = A_moved

    elif control.upper() == 'W':
        for col in range(4):

            A = display[:,col]
            A = A[::-1]
            A_moved = apply_action(A)
            display[:,col] = A_moved[::-1]

    elif control.upper() == 'S':
        for col in range(4):
            A = display[:,col]
            A_moved = apply_action(A)
            display[:,col] = A_moved
    else:
        raise('ERROR: invalid argument for input')
    
    return display

# check if game is over
def check_game_over(display):
    if np.any(display==0):
        return False
    else:
        return True
    
# check if game is won
def check_game_won(display):
    if np.any(display==2048):
        return True
    return False