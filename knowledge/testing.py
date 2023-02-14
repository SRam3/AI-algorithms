from minesweeper import *


user = Minesweeper()

def create_empty_board():
    board = []
    for i in range(user.height):
        row = []
        for j in range(user.width):
            row.append(False)
        board.append(row)
    return board
         
def board_mines():
    mines = set()
    user_board = create_empty_board()
    while len(mines) != len(user.mines):
        i = random.randrange(user.height)
        j = random.randrange(user.width)
        if not user_board[i][j]:
            mines.add((i, j))
            user_board[i][j] = True
    return user_board

def print_board_mines():
    board = board_mines()
    for i in range(user.height):
        print("--" * user.width + "-")
        for j in range(user.width):
            if board[i][j]:
                print("|X", end="")
            else:
                print("| ", end="")
        print("|")
    print("--" * user.width + "-")

    
def is_mine(cell):
    i, j = cell
    return board_mines()[i][j]

def nearby_mines(cell):
    count = 0
    for i in range(cell[0] - 1, cell[0] + 2):
        for j in range(cell[1] -1, cell[1] + 2):
            if (i, j) == cell:
                continue
            if 0 <= i < user.height and 0 <= j < user.width:
                if is_mine((i, j)):
                    count += 1
    return count
    
def mines_and_nearby():
    """Prints a text-based representation of nearby mines"""
    for i in range(user.height):
        print("--" * user.width + "-")
        for j in range(user.width):
            print("|{}".format(nearby_mines((i, j))), end="")
        print("|")
    print("--" * user.width + "-")





mines_and_nearby()

