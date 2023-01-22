from copy import deepcopy

def is_win(board):
    WINS = [
        ((0, 0), (0, 1), (0, 2)),
        ((1, 0), (1, 1), (1, 2)),
        ((2, 0), (2, 1), (2, 2)),

        ((0, 0), (1, 0), (2, 0)),
        ((0, 1), (1, 1), (2, 1)),
        ((0, 2), (1, 2), (2, 2)),

        ((0, 0), (1, 1), (2, 2)),
        ((2, 0), (1, 1), (0, 2))
    ]

    for a1, a2, a3 in WINS:
        if board[a1[0]][a1[1]] == board[a2[0]][a2[1]] == board[a3[0]][a3[1]] != " ":
            return [1] if board[a1[0]][a1[1]] == "O" else [-1]
    
    for i in board:
        if " " in i:
            break
    else:
        return [0]
    
    return False
        

def minimax(position, depth, is_O):

    res = is_win(position)

    if depth == 0 or res:
        return res

    valid_pos = [(i, j) for i in range(3) for j in range(3) if position[i][j] == " "]

    if is_O:
        max_eval = [-10]
        evals = []

        for i, j in valid_pos:
            new_pos = deepcopy(position)
            new_pos[i][j] = "O"

            evals.append([minimax(new_pos, depth-1, False)[0], i, j, depth])
        
        for eval in evals:
            if max_eval < eval:
                max_eval = eval
            elif max_eval == eval and max_eval[3] < eval[3]:
                max_eval = eval

        return max_eval

    else:
        min_eval = [10]
        evals = []

        for i, j in valid_pos:
            new_pos = deepcopy(position)
            new_pos[i][j] = "X"
            evals.append([minimax(new_pos, depth-1, True)[0], i, j, depth])
        
        for eval in evals:
            if min_eval > eval:
                min_eval = eval
            elif min_eval == eval and min_eval[3] < eval[3]:
                min_eval = eval

        return min_eval

board = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
    ]

turn = True               #true turn → O turn || false → X turn

minimax(board, 100, turn) #evaluation of current position || 1: O, 0: DRAW, -1: X
