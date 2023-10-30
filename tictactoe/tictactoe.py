"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


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
                o_count +=1
    
    if x_count > o_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    res = set()
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == EMPTY:
                res.add((i, j))
    return res



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception
    copy_board = copy.deepcopy(board)
    copy_board[action[0]][action[1]] = player(board)
    return copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if len(set(row)) == 1:
            return row[0]
    if board[0][0] == board[1][1] and board[0][0] == board[2][2]:
        return board[0][0]
    if board[0][2] == board[1][1] and board[0][2] == board[2][0]:
        return board[0][2]
    if board[0][0] == board[1][0] and board[0][0] == board[2][0]:
        return board[0][0]
    if board[0][1] == board[1][1] and board[0][1] == board[2][1]:
        return board[0][1]
    if board[0][2] == board[1][2] and board[0][2] == board[2][2]:
        return board[0][2]

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
   
    return len(actions(board)) == 0 or winner(board) != None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
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
    actions_and_values = {}
    for action in actions(board):
        actions_and_values[min_max(result(board, action))] = action

    if player(board) == X:
        return actions_and_values[max(actions_and_values)]
    else:
        return actions_and_values[min(actions_and_values)]
    
def min_max(board):
    if terminal(board):
        return utility(board)
    
    if player(board) == X:
        v = -100
        for action in actions(board):
            v = max(v, min_max(result(board, action)))
    else:
        v = 100
        for action in actions(board):
            v = min(v, min_max(result(board, action)))
    return v
