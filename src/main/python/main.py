
##
## Either fix barracks or remove it
## Make sure the reset works
##
## Next step: separate to server/client even here
##

from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QMainWindow, QMessageBox, QAction, qApp, QDialogButtonBox, QLineEdit, QSizePolicy, QLabel
from PyQt5.QtGui import QIcon, QFont, QDrag
from PyQt5.QtCore import pyqtSlot, QMimeData
from PyQt5.QtCore import Qt
from PyQt5 import QtSvg

from player import *
from board import Board

import sys

class BoardSquare(QtSvg.QSvgWidget):
    WHITE_SQUARE = 0
    BLACK_SQUARE = 1
    GREEN_SQUARE = 2
    RED_SQUARE = 3
    WHITE_ROOK = 4
    BLACK_ROOK = 5
    PIECES = 6

    def __init__(self, images, background, click):
        super(QWidget, self).__init__(images[background])
        self.images = images
        self.mouseReleaseEvent=click

        self.background = background
        self.piece = background

        self.label = QLabel(self)
        self.label.setText("   ")
        self.label.move(10, 10)
        self.label.setFont(QFont('Arial', 48))


    def reset(self):
        self.piece = self.background
        self.load(self.images[self.background])
        self.label.setText("")

    def setPiece(self, piece):
        self.piece = piece
        if piece > 1:
            self.label.setText("")
        self.load(self.images[piece])

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, w):
        return w

    def setScore(self, score):
        if self.piece < 4:
            if (score < 0):
                p = BoardSquare.RED_SQUARE
            elif (score > 0):
                p = BoardSquare.GREEN_SQUARE
            else:
                p = self.background

            self.piece = p
            self.load(self.images[p])
            self.label.setText(str(score))
            self.adjustSize()

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


class AppContext(ApplicationContext):
    @cached_property
    def main_window(self):
        return MainWindow(self)

    def initBoard(self):
        # We have to destroy old board if existing
        for bs in self.squares:
            for b in bs:
                b.deleteLater()

        self.board = Board(self.rows, self.cols)
        self.squares = []

        for r in range(self.rows):
            self.squares.append([BoardSquare(self.piece_set, 0, self.gen_clickhandler(r, c)) for c in range(self.cols)])

    def __init__(self, rows, cols, max_turns):
        super().__init__()
        self.main_window.title = 'CoverChess'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 800

        self.rows = rows
        self.cols = cols
        self.max_turns = max_turns*2
        self.squares = []
        self.turns = 0
        self.next_white = True
        self.player_white = True

        self.piece_set = [0] * BoardSquare.PIECES
        self.piece_set[BoardSquare.WHITE_SQUARE] = self.get_resource('images/solid_white.svg')
        self.piece_set[BoardSquare.BLACK_SQUARE] = self.get_resource('images/solid_black.svg')
        self.piece_set[BoardSquare.GREEN_SQUARE] = self.get_resource('images/solid_green.svg')
        self.piece_set[BoardSquare.RED_SQUARE] = self.get_resource('images/solid_red.svg')
        self.piece_set[BoardSquare.WHITE_ROOK] = self.get_resource('images/white_rook.svg')
        self.piece_set[BoardSquare.BLACK_ROOK] = self.get_resource('images/black_rook.svg')

        self.initBoard()
        self.initUI()
        self.initBoardLayout()


    def do_move(self, row, col):
        self.turns += 1
        if self.next_white:
            self.next_white = False
            self.board.set_cell(row, col, 1)
            self.squares[row][col].setPiece(BoardSquare.WHITE_ROOK)
        else:
            self.next_white = True
            self.board.set_cell(row, col, -1)
            self.squares[row][col].setPiece(BoardSquare.BLACK_ROOK)

        self.updateScores()
        self.grid.update()

        if self.turns == self.max_turns:
            self.game_over()

        if (self.player_white and not self.next_white) or (not self.player_white and self.next_white):
            self.minmax_move()


    def handle_click(self, row, col):
        if (self.board.get_cell(row, col) == 0):
            self.do_move(row, col)

    def minmax_move(self):
        (row, col) = minmax(self.board, self.player_white, 2)
        self.do_move(row, col)

    def random_move(self):
        moves = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board.get_cell(r, c) == 0:
                    moves.append((r, c))
        (r, c) = random.choice(moves)
        self.do_move(r, c)

    def game_over(self):
        score = self.board.get_final_score()
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        if score > 0:
            title = "White wins!"
        elif score < 0:
            title = "Black wins!"
        else:
            title = "Tie!"

        msgBox.setText(title + "\nFinal score: " + str(score))
        msgBox.setWindowTitle(title)
        msgBox.exec()
        self.reset()

    def reset(self):
        self.board.reset()
        for r in range(self.rows):
            for c in range(self.cols):
                self.squares[r][c].reset()
        self.updateScores()
        self.grid.update()
        self.turns = 0
        self.next_white = True


    def updateScores(self):
        for r in range(self.rows):
            for c in range(self.cols):
                score = self.board.get_score(r, c)
                self.squares[r][c].setScore(score)


    def gen_clickhandler(self, row, col):
        return lambda _ : self.handle_click(row, col)

    def initBoardLayout(self):
        self.wid = QWidget()
        boardLayout = QGridLayout()
        self.grid = boardLayout

        for r in range(self.rows):
            for c in range(self.cols):
                boardLayout.addWidget(self.squares[r][c], r,c)

        # barracksLayout = QGridLayout()
        # for c in range(self.cols):
        #     widget = QtSvg.QSvgWidget(self.get_resource('images/white_rook.svg'))
        #     widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #     barracksLayout.addWidget(widget, 0, c)

        layout = QVBoxLayout()

        layout.addLayout(boardLayout)
        # layout.addLayout(barracksLayout)

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

        if self.player_white:
            whiteAction.setChecked(True)
        else:
            blackAction.setChecked(True)

        settingsMenu.addAction(changeBoardAction)

    def change_board_dialog(self):
        dlg = ChangeBoardDialog(self.main_window)
        dlg.width_input.setText(str(self.board.cols))
        dlg.height_input.setText(str(self.board.rows))
        if dlg.exec_():
            newHeight = dlg.height_input.text()
            newWidth = dlg.width_input.text()
            if newHeight.isnumeric() and newWidth.isnumeric() and 0 < int(newHeight) and 0 < int(newWidth):
                self.rows = int(newHeight)
                self.cols = int(newWidth)
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
        self.player_white = white
        self.whiteAction.setChecked(white)
        self.blackAction.setChecked(not white)
        self.check_computer_move()

    def check_computer_move(self):
        if self.player_white != self.next_white:
            self.minmax_move()

    def run(self):
        self.main_window.show()
        self.check_computer_move()
        return self.app.exec_()

if __name__ == '__main__':
    appctxt = AppContext(4,4,3)
    exit_code = appctxt.run()
    sys.exit(exit_code)
