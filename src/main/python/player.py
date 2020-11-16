import random
import copy

#
#
# PLAYERS
#
#


def random_player(board):
    return random.choice(board.get_moves())

def mmaux(board, next_white, max_moves, move_count):
    moves = board.get_moves()

    if (max_moves == move_count) or (not moves):
        return (board.get_final_score(), (-1,-1))

    best_score = ""
    best_move = ""

    for m in board.get_moves():
        newboard = copy.deepcopy(board)
        (r, c) = m
        if (next_white):
            newboard.set_cell(r, c, -1)
        else:
            newboard.set_cell(r, c, 1)

        (score, _) = mmaux(newboard, not next_white, max_moves, move_count+1)

        if (best_score == ""):
            best_score = score
            best_move = m
        else:
            if (next_white): # we want to minimize
                if (score < best_score):
                    best_score = score
                    best_move = m
            else: # we want to maximize
                if (score > best_score):
                    best_score = score
                    best_move = m

    return (best_score, best_move)


def minmax(board, next_white, max_moves):
    assert(max_moves > 0)
    (best_score, best_move) = mmaux(board, next_white, max_moves, 0)
    return best_move

def minmaxwhite(board):
    return minmax(board, True, 3)

def minmaxblack(board):
    return minmax(board, False, 3)

