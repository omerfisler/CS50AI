
from tictactoe import result
X = "X"
O = "O"
EMPTY = None

board = [[X, X, EMPTY],
        [EMPTY, O, EMPTY],
        [EMPTY, X, O]]

action=(0,2)

print(result(board,action))