class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = []
        self.scores = []
        for _ in range(rows):
            self.board.append([0 for _ in range(cols)])
            self.scores.append([0 for _ in range(cols)])

    def rook(self, row, col, value):
        # Upwards
        free = True
        for r in range(row-1, -1, -1):
            if (self.board[r][col] != 0):
                free = False

            if (free):
                self.scores[r][col] += value

        free = True
        # Downwards
        for r in range(row+1, self.rows):
            if (self.board[r][col] != 0):
                free = False

            if (free):
                self.scores[r][col] += value

        free = True
        # Leftwards
        for c in range(col-1, -1, -1):
            if (self.board[row][c] != 0):
                free = False

            if (free):
                self.scores[row][c] += value

        free = True
        # Rightwards
        for c in range(col+1, self.cols):
            if (self.board[row][c] != 0):
                free = False
            if (free):
                self.scores[row][c] += value




    def update_scores(self):
         for r in range(self.rows):
            for c in range(self.cols):
                self.scores[r][c] = 0
         for r in range(self.rows):
            for c in range(self.cols):
                if (self.board[r][c] == 1):
                    self.rook(r, c, 1)
                elif (self.board[r][c] == -1):
                    self.rook(r, c, -1)

    def get_final_score(self):
        sum = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if (self.scores[r][c] > 0):
                    sum += 1
                elif (self.scores[r][c] < 0):
                    sum -= 1
        return sum

    def get_score(self, row, col):
        return self.scores[row][col]

    def get_cell(self, row, col):
        return self.board[row][col]

    def set_cell(self, row, col, value):
        if (row < 0 or row >= self.rows or col < 0 or col >= self.cols):
            raise Exception("set_cell out of bounds")

        self.board[row][col] = value
        self.update_scores()


    def get_moves(self):
        moves = []
        for r in range(self.rows):
            for c in range(self.cols):
                if (self.board[r][c] == 0):
                    moves.append((r, c))
        return moves


    def reset(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.board[r][c] = 0
                self.scores[r][c] = 0

    def print(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (self.board[r][c] == 0):
                    char = '.'
                if (self.board[r][c] == 1):
                    char = 'b'
                if (self.board[r][c] == -1):
                    char = 'w'

                print(char, end = '')
            print()
