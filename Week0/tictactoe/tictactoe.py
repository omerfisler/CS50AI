"""
Tic Tac Toe Player
"""

import math
import copy #To use deepcopy in result()

X = "X"
O = "O"
EMPTY = None

max_utility = 1
min_utility = -1


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
    if sum(row.count("X") for row in board) > sum(row.count("O") for row in board):
        return O
    else:
        return X
    

    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_tiles = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possible_tiles.add((i, j))
    return possible_tiles
    
    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError(f"Invalid action: {action}. The action is not allowed on the current board.")
    else:
        board_copy = copy.deepcopy(board)
        board_copy[action[0]][action[1]] = player(board)
        return board_copy
    
    # raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # rows
    for row in board:
        if row[0]==row[1] and row[1] == row[2] and row[0] != EMPTY:
            return row[0]
    # columns
    for column in range(3):
        if board[0][column]==board[1][column] and board[1][column]==board[2][column] and board[0][column] != EMPTY:
            return board[0][column]

    # Check diagonals for winner
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None or not actions(board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)
    if result == X:
        return 1
    elif result == O:
        return -1
    else: # result = None
        return 0

def max_value(board):
    if terminal(board):
        return utility(board), None
    
    best_action = None
    best_value = -math.inf
    for action in actions(board):
        value, _ = min_value(result(board, action)) # tempValue = max(tempValue,min_value(result(board,action)[0]))
        if value > best_value:    #
            best_value = value    #  
            best_action = action  # Compared them in if condition instead of max-min to access "action" easily.
    
    return best_value, best_action

def min_value(board):
    if terminal(board):
        return utility(board), None
    
    best_action = None
    best_value = math.inf
    for action in actions(board):
        value, _ = max_value(result(board, action)) #
        if value < best_value:
            best_value = value
            best_action = action
    
    return best_value, best_action
    
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    _, best_action = max_value(board) if player(board) == X else min_value(board) # The perfect method to adjust to the algorithm shown in the lecture 0.
    return best_action


