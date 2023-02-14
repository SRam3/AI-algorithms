"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], 
            [EMPTY, EMPTY, EMPTY], 
            [EMPTY, EMPTY, EMPTY]
            ]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0

    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1
            else:
                pass

    if x_count > o_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid action")

    i, j = action
    board_copy = deepcopy(board)
    board_copy[i][j] = player(board)
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in range(len(board)):
        if len(set(board[row])) == 1 and board[row][0] != EMPTY:
            return board[row][0]

    # Check columns
    for col in range(len(board[0])):
        column = []
        for row in range(len(board)):
            column.append(board[row][col])
        if len(set(column)) == 1 and column[0] != EMPTY:
            return column[0]

    # Check diagonals
    diagonal1 = []
    diagonal2 = []
    for i in range(len(board)):
        diagonal1.append(board[i][i])
        diagonal2.append(board[i][len(board) - i - 1])

    if len(set(diagonal1)) == 1 and diagonal1[0] != EMPTY:
        return diagonal1[0]
    elif len(set(diagonal2)) == 1 and diagonal2[0] != EMPTY:
        return diagonal2[0]

    # No winner
    if not any(None in row for row in board):
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None or not any(None in row for row in board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    elif player(board) == X:
        action, _ = max_value(board)
        return action
    else:
        action, _ = min_value(board)
        return action


def max_value(board):
    """
    Returns the optimal action for the maximizing player
    """
    v = -math.inf
    best_action = None
    if terminal(board):
        return best_action, utility(board)
    for action in actions(board):
        _, val = min_value(result(board, action))
        if val > v:
            v = val
            best_action = action
    return best_action, v


def min_value(board):
    """
    Returns the optimal action for the minimizing player
    """
    v = math.inf
    best_action = None
    if terminal(board):
        return best_action, utility(board)
    for action in actions(board):
        _, val = max_value(result(board, action))
        if val < v:
            v = val
            best_action = action
    return best_action, v
