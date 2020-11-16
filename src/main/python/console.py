from board import Board
from player import *


MAX_MOVES = 3*2


def play_game(white_player, black_player, verbose):
    next_white = True
    cur_move = 0
    board = Board(4, 4)
    board.set_cell(1,1,-1)

    if (verbose):
        board.print()
    while (cur_move < MAX_MOVES):
        if (next_white):
            (r, c) = white_player(board)
            board.set_cell(r, c, -1)
            next_white = False
        else:
            (r, c) = black_player(board)
            board.set_cell(r, c, 1)
            next_white = True

        cur_move += 1
        if (verbose):
            print("\n")
            board.print()

    score = board.get_final_score()
    if (score > 0):
        title = "black wins!"
    elif (score < 0):
        title = "white wins!"
    else:
        title = "tie!"
    if (verbose):
        print(title + " (" + str(score) + ")")

    return score



def gen_minmax(white, depth):
    return lambda b : minmax(b, white, depth)

if __name__ == '__main__':
    print("CoverChess Console ")
    sum = 0
    total_games = 50
    for i in range(total_games):
        if (i%10 == 0):
            print(str(i) + "/" + str(total_games))
        score = play_game(gen_minmax(True, 2), gen_minmax(False, 2), False)
        sum += score

    print(str(sum/total_games))





