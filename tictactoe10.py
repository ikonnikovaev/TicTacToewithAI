import random

def opposite(ch):
    if (ch == "X"):
        return "O"
    else:
        return "X"

def print_field(field):
    print("---------")
    for row in field:
        print("| " + " ".join(row) + " |")
    print("---------")
    
def find_free_cells(field):
    free_cells = []
    for r in range(3):
        for c in range(3):
            if (field[r][c] == " "):
                free_cells.append((r, c))
    return free_cells

def check_full_row(field, r, ch):
    for c in range(3):
        if (field[r][c] != ch):
            return False
    return True

def check_full_column(field, c, ch):
    for r in range(3):
        if (field[r][c] != ch):
            return False
    return True

def check_full_main_diag(field, ch):
    for i in range(3):
        if (field[i][i] != ch):
            return False
    return True

def check_full_aux_diag(field, ch):
    for i in range(3):
        if (field[i][2 - i] != ch):
            return False
    return True


def check_danger_row(field, r, ch):
    if (field[r][0] == ch):
        if (field[r][1] == ch) and (field[r][2] == " "):
            return 2
        elif (field[r][1] == " ") and (field[r][2] == ch):
            return 1
    elif (field[r][0] == " ") and (field[r][1] == ch) and (field[r][2] == ch):
        return 0
    return -1


def check_danger_column(field, c, ch):
    if (field[0][c] == ch):
        if (field[1][c] == ch) and (field[2][c] == " "):
            return 2
        elif (field[1][c] == " ") and (field[2][c] == ch):
            return 1
    elif (field[0][c] == " ") and (field[1][c] == ch) and (field[2][c] == ch):
        return 0
    return -1

def check_danger_main_diag(field, ch):
    if (field[0][0] == ch) and (field[1][1] == ch) and (field[2][2] == " "):
        return 2
    elif (field[0][0] == ch) and (field[1][1] == " ") and (field[2][2] == ch):
        return 1
    elif (field[0][0] == " ") and (field[1][1] == ch) and (field[2][2] == ch):
        return 0
    return -1
    
    
def check_danger_aux_diag(field, ch):
    if (field[0][2] == ch) and (field[1][1] == ch) and (field[2][0] == " "):
        return 2
    elif (field[0][2] == ch) and (field[1][1] == " ") and (field[2][0] == ch):
        return 1
    elif (field[0][2] == " ") and (field[1][1] == ch) and (field[2][0] == ch):
        return 0
    return -1
    
    
def check_win(field, ch):
    for r in range(3):
        if (check_full_row(field, r, ch)):
            return True
    for c in range(3):
        if (check_full_column(field, c, ch)):
            return True
    if (check_full_main_diag(field, ch)) or (check_full_aux_diag(field, ch)):
        return True
    return False


def read_human_move(field):
    correct_coordinates = False
    while not (correct_coordinates):
        try:
            c, r = map(int, input("Enter the coordinates: ").split())
        except ValueError:
            print("You should enter numbers!")

        r = 3 - r
        c = c - 1
        
        if (r < 0) or (r > 2) or (c < 0) or (c > 2):
            print("Coordinates should be from 1 to 3!")
            continue
        elif (field[r][c] != " "):
            print("This cell is occupied! Choose another one!")
            continue
        
        correct_coordinates = True
        return (r, c)

def choose_winning_move(field, ch):
    for r in range(3):
        c = check_danger_row(field, r, ch)
        if (c != -1):
            return (r, c)
    for c in range(3):
        r = check_danger_column(field, c, ch) 
        if (r != -1):
            return (r, c)
    r = check_danger_main_diag(field, ch)
    if (r != -1):
        return(r, r)
    r = check_danger_aux_diag(field, ch)
    if (r != -1):
        return(r, 2 - r)

    return (-1, -1)


def choose_computer_move_easy(field):    
    return random.choice(find_free_cells(field))

def choose_computer_move_medium(field, ch):

    ch_opp = opposite(ch)
   
    (r, c) = choose_winning_move(field, ch)
    if ((r, c) != (-1, -1)):
        return (r, c)
    
    (r, c) = choose_winning_move(field, ch_opp)
    if ((r, c) != (-1, -1)):
        return (r, c)

    return choose_computer_move_easy(field)

def eval(field):
     if check_win(field, "X"):
         return 10
     elif check_win(field, "O"):
         return -10
     else:
         return 0
         
def minimax(field, ch, depth):
    score = eval(field)
    if (abs(score) == 10):
        return score
    elif len(find_free_cells(field)) == 0:
        return 0
    else:
        best = -1000
        if (ch == "O"):
            best = 1000
            
        for (r, c) in find_free_cells(field):
            field[r][c] = ch
            if (ch == "X"):
                best = max(best, minimax(field, opposite(ch), depth + 1))
            else:
                best = min(best, minimax(field, opposite(ch), depth + 1))
            field[r][c] = " "
            
        return best
        
        
def choose_computer_move_hard(field, ch):
    
    best_move = (-1, -1)
    best = -1000
    if (ch == "O"):
        best = 1000
        
    for (r, c) in find_free_cells(field):
        field[r][c] = ch
        move_eval = minimax(field, opposite(ch), 0)
        field[r][c] = " "
        if (ch == "X") and (move_eval > best):
            best = move_eval
            best_move = (r, c)
        elif (ch == "O") and (move_eval < best):
            best = move_eval
            best_move = (r, c)
        
    return best_move
     
    #(r, c) =  choose_computer_move_medium(field, ch) 
    #return (r, c)
    
def make_move(field, ch, human = False, level = 0):
    r, c = 0, 0
    if (human):
        r, c = read_human_move(field)
    else:
        if (level == 0):
            print('Making move level "easy"')
            r, c = choose_computer_move_easy(field)
        elif (level == 1):
            print('Making move level "medium"')
            r, c = choose_computer_move_medium(field, ch)
        elif (level == 2):
            print('Making move level "hard"')
            r, c = choose_computer_move_hard(field, ch)
        
    field[r][c] = ch
    print_field(field)


def check_result(field):
    game_finished = False

    n_x = 0
    n_o = 0
    x_wins = False
    o_wins = False
    empty_cells = False

    for row in field:
        for cell in row:
            if (cell == " "):
                empty_cells = True
            elif (cell == "X"):
                n_x += 1
            elif (cell == "O"):
                n_o += 1

    if check_win(field, "X"):
        x_wins = True
    if check_win(field, "O"):
        o_wins = True   
      

    if (x_wins and o_wins) or (abs(n_x - n_o) > 1):
        game_finished = True
        print("Impossible")
    elif (x_wins):
        game_finished = True
        print("X wins")
    elif (o_wins):
        game_finished = True
        print("O wins")
    elif (empty_cells):
        pass
        #print("Game not finished")
    else:
        game_finished = True
        print("Draw")

    return game_finished


def play(x_human, o_human, x_level, o_level):
    field = []
    for i in range(3):
        #row = list(user_input[3 * i + 1 : 3 * i + 4])
        field.append([" "] * 3)

    print_field(field)

    k = 0
    while not (check_result(field)):
        if (k % 2 == 0):
            make_move(field, "X", x_human, x_level)
        else:
            make_move(field, "O", o_human, o_level)
        k += 1
     
    
#main body of the program
exit = False
while (not exit):
    x_human, o_human = False, False
    x_level, o_level = 0, 0
    parameters = input("Input command: ").split()
    
    if (parameters[0] == "exit"):
        break
    if (parameters[0] != "start") or (len(parameters) < 3):
        print("Bad parameters!")
        continue
    if (parameters[1] == "user"):
        x_human = True
    elif (parameters[1] == "easy"):
        x_human = False
        x_level = 0
    elif (parameters[1] == "medium"):
        x_human = False
        x_level = 1
    elif (parameters[1] == "hard"):
        x_human = False
        x_level = 2
    else:
        print("Bad parameters!")
        continue
    if (parameters[2] == "user"):
        o_human = True
    elif (parameters[2] == "easy"):
        o_human = False
        o_level = 0
    elif (parameters[2] == "medium"):
        o_human = False
        o_level = 1
    elif (parameters[2] == "hard"):
        o_human = False
        o_level = 2
    else:
        print("Bad parameters!")
        continue
        
    play(x_human, o_human, x_level, o_level)





