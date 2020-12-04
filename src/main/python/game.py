# Currently we considering creating a new Game object for each game, i.e., no re-using
from board import Board

class IllegalMove(Exception):
    pass

class Game():
    # Colors
    WHITE=1
    TIE=0
    BLACK=-1

    def __init__(self, rows, columns, max_moves):
        self.current_player = Game.WHITE # White begins
        self.rows = rows
        self.columns = columns
        self.board = Board(rows, columns)
        self.max_moves = max_moves
        self.next_move = 0

    # Return TRUE if final move 
    def make_move(self, row, col):
        if (self.board.get_cell(row, col) != 0 or
           row < 0 or row >= self.rows or
           col < 0 or col >= self.columns):
            raise IllegalMove

        self.board.set_cell(row, col, self.current_player)
        self.next_move += 1
        self.current_player = -self.current_player
        return self.next_move == self.max_moves

    def valid_move(self, row, col):
        if (self.board.get_cell(row, col) == 0):
            return True
        else:
            return False

    def get_score(self, row, col):
        return self.board.get_score(row, col)

    def get_winner(self):
        score = self.board.get_final_score()
        if (score < 0):
            return Game.BLACK
        elif (score > 0):
            return Game.WHITE
        else:
            return Game.TIE

    def next_player(self):
        return self.current_player

    def get_status(self, row, col):
        return (self.board.get_cell(row, col), self.get_score(row, col))
