from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QMainWindow, QMessageBox, QAction, qApp, QDialogButtonBox, QLineEdit, QSizePolicy, QLabel
from PyQt5.QtGui import QIcon, QFont, QDrag, QPixmap, QPainter
from PyQt5.QtCore import pyqtSlot, QMimeData
from PyQt5.QtCore import Qt
from PyQt5 import QtSvg

from player import *
from board import Board
from squares import BoardSquare, BarracksSquare
from game import Game

import sys

class MainWindow(QMainWindow):
    def __init__(self, ctx):
        super(MainWindow, self).__init__()
        self.ctx = ctx

class ChangeBoardDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(ChangeBoardDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Change Board Size")

        self.width_input = QLineEdit()
        self.height_input = QLineEdit()

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.width_input)
        self.layout.addWidget(self.height_input)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


##
## Main Application
##

class AppContext(ApplicationContext):
    @cached_property
    def main_window(self):
        return MainWindow(self)

    def __init__(self):
        super().__init__()
        self.main_window.title = 'CoverChess'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 800

        # Default values
        self.rows = 4
        self.columns = 4
        self.max_moves = 2*2
        self.white_human = False
        self.black_human = True

        self.squares = []
        self.barracks = []

        # Images for the pieces
        self.piece_set = [0] * BoardSquare.PIECES
        self.piece_set[BoardSquare.WHITE_SQUARE] = self.get_resource('images/solid_white.svg')
        self.piece_set[BoardSquare.BLACK_SQUARE] = self.get_resource('images/solid_black.svg')
        self.piece_set[BoardSquare.GREEN_SQUARE] = self.get_resource('images/solid_green.svg')
        self.piece_set[BoardSquare.RED_SQUARE] = self.get_resource('images/solid_red.svg')
        self.piece_set[BoardSquare.WHITE_ROOK] = self.get_resource('images/white_rook.svg')
        self.piece_set[BoardSquare.BLACK_ROOK] = self.get_resource('images/black_rook.svg')

        self.initUI()
        self.new_game()

    def initBoardLayout(self):
        self.wid = QWidget()
        boardLayout = QGridLayout()
        self.grid = boardLayout

        for r in range(self.rows):
            for c in range(self.columns):
                boardLayout.addWidget(self.squares[r][c], r,c)

        self.barracks = []
        barracksLayout = QGridLayout()
        for c in range(self.columns):
            widget = QtSvg.QSvgWidget(self.get_resource('images/white_rook.svg'))
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            bsq = BarracksSquare(self.piece_set, BoardSquare.WHITE_ROOK, self.gendrag(c))
            self.barracks.append(bsq)
            barracksLayout.addWidget(bsq, 0, c)

        layout = QVBoxLayout()

        layout.addLayout(boardLayout)
        layout.addLayout(barracksLayout)

        self.wid.setLayout(layout)
        self.main_window.setCentralWidget(self.wid)


    def initUI(self):
        self.main_window.setWindowTitle(self.main_window.title)
        self.main_window.setGeometry(self.left, self.top, self.width, self.height)

        quitAction = QAction("&Quit", self.main_window)
        quitAction.setShortcut('Ctrl+Q')
        quitAction.triggered.connect(qApp.quit)

        whiteAction = QAction("&White", self.main_window)
        whiteAction.setShortcut('Ctrl+W')
        whiteAction.triggered.connect(lambda _ : self.set_player_color(True))
        whiteAction.setCheckable(True)

        blackAction = QAction("&Black", self.main_window)
        blackAction.setShortcut('Ctrl+B')
        blackAction.triggered.connect(lambda _ : self.set_player_color(False))
        blackAction.setCheckable(True)

        self.whiteAction = whiteAction
        self.blackAction = blackAction

        changeBoardAction = QAction("Change Board &Size", self.main_window)
        changeBoardAction.setShortcut('Ctrl+S')
        changeBoardAction.triggered.connect(self.change_board_dialog)

        menubar = self.main_window.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(quitAction)

        settingsMenu = menubar.addMenu('&Settings')
        playerColorMenu = settingsMenu.addMenu('Player Color')
        playerColorMenu.addAction(whiteAction)
        playerColorMenu.addAction(blackAction)

        if self.white_human:
            whiteAction.setChecked(True)
        if self.black_human:
            blackAction.setChecked(True)

        settingsMenu.addAction(changeBoardAction)

    def update_graphics(self):
        for r in range(self.rows):
            for c in range(self.columns):
                (piece, score) = self.game.get_status(r, c)
                if (piece == 1):
                    piece = BoardSquare.WHITE_ROOK
                if (piece == -1):
                    piece = BoardSquare.BLACK_ROOK
                self.squares[r][c].setStatus(piece, score)
                # self.squares[r][c].setScore(self.game.get_score(r, c))

        self.grid.update()



    # Restart the game
    # - Resize board and create squares
    # - Reset game
    # - Update graphics
    def new_game(self):
        # We have to destroy old board if existing
        for bs in self.squares:
            for b in bs:
                b.deleteLater()

        self.squares = []
        for r in range(self.rows):
            # self.squares.append([BoardSquare(self.piece_set, 0, self.gen_clickhandler(r, c)) for c in range(self.columns)])
            self.squares.append([BoardSquare(self.piece_set, 0, self.gen_clickhandler(r, c)) for c in range(self.columns)])

        self.game = Game(self.rows, self.columns, self.max_moves)
        self.initBoardLayout()
        self.update_graphics()


    def do_move(self, row, col):
        gameOver = self.game.make_move(row, col)
        self.update_graphics()
        if (gameOver):
            self.game_over()

        # Computer move?
        self.check_computer_move()

    def handle_click(self, row, col, src):
        if (self.game.valid_move(row, col)):
            self.barracks[src].used()
            self.do_move(row, col)


    # TODO: Move to AI file
    def minmax_move(self):
        (row, col) = minmax(self.game.board, self.game.next_player() == Game.BLACK, 2)
        self.do_move(row, col)

    # def random_move(self):
    #     moves = []
    #     for r in range(self.rows):
    #         for c in range(self.columns):
    #             if self.board.get_cell(r, c) == 0:
    #                 moves.append((r, c))
    #     (r, c) = random.choice(moves)
    #     self.do_move(r, c)

    def game_over(self):
        winner = self.game.get_winner()
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        if winner == Game.WHITE:
            title = "White wins!"
        elif winner == Game.BLACK:
            title = "Black wins!"
        else:
            title = "Tie!"

        msgBox.setText(title)
        msgBox.setWindowTitle(title)
        msgBox.exec()
        self.new_game()


    def gen_clickhandler(self, row, col):
        return lambda src : self.handle_click(row, col, src)

    def gendrag(self, idx):
        return lambda _ : self.drag_test(idx)

    def drag_test(self, idx):
        drag = QDrag(self.main_window)
        mimeData = QMimeData()
        mimeData.setText(str(idx))
        drag.setMimeData(mimeData)
        pixmap = QPixmap(150, 150)
        painter = QPainter(pixmap)
        painter.drawPixmap(self.barracks[idx].rect(), self.barracks[idx].grab())
        painter.end()
        drag.setPixmap(pixmap)
        drag.exec_()


    def change_board_dialog(self):
        dlg = ChangeBoardDialog(self.main_window)
        dlg.width_input.setText(str(self.board.cols))
        dlg.height_input.setText(str(self.board.rows))
        if dlg.exec_():
            newHeight = dlg.height_input.text()
            newWidth = dlg.width_input.text()
            if newHeight.isnumeric() and newWidth.isnumeric() and 0 < int(newHeight) and 0 < int(newWidth):
                self.rows = int(newHeight)
                self.columns = int(newWidth)
                self.initBoard()
                self.initBoardLayout()
                self.reset()
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText("Invalid board width/height!")
                msgBox.setWindowTitle("Error")
                msgBox.exec()

    def set_player_color(self, white):
        if (white):
            if (self.white_human):
                self.white_human = False
                self.whiteAction.setChecked(False)
            else:
                self.white_human = True
                self.whiteAction.setChecked(True)
        else:
            if (self.black_human):
                self.black_human = False
                self.blackAction.setChecked(False)
            else:
                self.black_human = True
                self.blackAction.setChecked(True)
        self.check_computer_move()

    def check_computer_move(self):
        if (self.game.next_player() == Game.WHITE and not self.white_human) or (self.game.next_player() == Game.BLACK and not self.black_human):
            self.minmax_move()

    def run(self):
        self.main_window.show()
        self.check_computer_move()
        return self.app.exec_()

if __name__ == '__main__':
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
