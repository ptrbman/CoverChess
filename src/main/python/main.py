from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QMainWindow, QMessageBox, QAction, qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtSvg

from player import *
from board import Board
import sys, random

PLAYER_WHITE = False

class MainWindow(QMainWindow):
    def __init__(self, ctx):
        super(MainWindow, self).__init__()
        self.ctx = ctx 

class AppContext(ApplicationContext):

    @cached_property
    def main_window(self):
        return MainWindow(self)

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


        self.turns = 0
        self.board = Board(self.rows, self.cols)
        self.buttons = []
        self.pieces = []
        self.next_white = True

        for r in range(self.rows):
            self.pieces.append([0 for _ in range(self.cols)])
            self.buttons.append([QPushButton("0") for _ in range(self.cols)])

        self.initUI()


    def do_move(self, row, col):
        self.turns += 1
        if (self.next_white):
            self.next_white = False
            self.board.set_cell(row, col, -1)
            svgWidget = QtSvg.QSvgWidget(self.get_resource('images/white_rook.svg'))
        else:
            self.next_white = True
            self.board.set_cell(row, col, 1)
            svgWidget = QtSvg.QSvgWidget(self.get_resource('images/black_rook.svg'))

        self.pieces[row][col] = svgWidget
        svgWidget.setGeometry(250,250,250,250)
        self.buttons[row][col].setVisible(False)
        self.grid.addWidget(svgWidget, row, col)
        self.updateScores()
        self.grid.update()

        if (self.turns == self.max_turns):
            self.game_over()

        if ((PLAYER_WHITE and not self.next_white) or(not PLAYER_WHITE and self.next_white)):
            self.minmax_move()


    def handle_click(self, row, col):
        self.do_move(row, col)

    def minmax_move(self):
        (row, col) = minmax(self.board, not PLAYER_WHITE, 2)
        self.do_move(row, col)

    def random_move(self):
        moves = []
        for r in range(self.rows):
            for c in range(self.cols):
                if (self.board.get_cell(r, c) == 0):
                    moves.append((r, c))
        (r, c) = random.choice(moves)
        self.do_move(r, c)

    def game_over(self):
        score = self.board.get_final_score()
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        if (score > 0):
            title = "Black wins!"
        elif (score < 0):
            title = "White wins!"
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
                if (self.pieces[r][c] != 0):
                    self.pieces[r][c].setVisible(False)
                    self.buttons[r][c].setVisible(True)
        self.updateScores()
        self.grid.update()
        self.turns = 0
        self.next_white = True


    def updateScores(self):
        for r in range(self.rows):
            for c in range(self.cols):
                score = self.board.get_score(r, c)
                button = self.buttons[r][c]
                button.setText(str(score))
                if (score < 0):
                    button.setStyleSheet("background-color: green")
                elif (score > 0):
                    button.setStyleSheet("background-color: red")
                else:
                    button.setStyleSheet("background-color: gray")



    def gen_clickhandler(self, row, col):
        return lambda _ : self.handle_click(row, col)

    def initUI(self):
        self.main_window.setWindowTitle(self.main_window.title)
        self.main_window.setGeometry(self.left, self.top, self.width, self.height)

        wid = QWidget()
        layout = QGridLayout()
        self.grid = layout

        for r in range(0,self.rows):
            for c in range(0,self.cols):
                button = self.buttons[r][c]
                button.setFixedHeight(250)
                button.clicked.connect(self.gen_clickhandler(r, c))
                layout.addWidget(button, r,c)

        wid.setLayout(layout)
        self.main_window.setCentralWidget(wid)

        quitAction = QAction("&Quit", self.main_window)
        quitAction.setShortcut('Ctrl+Q')
        quitAction.triggered.connect(qApp.quit)

        menubar = self.main_window.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(quitAction)


    def run(self):
        self.main_window.show()
        if (not PLAYER_WHITE):
            self.minmax_move()
        return self.app.exec_()

if __name__ == '__main__':
    appctxt = AppContext(4,4,3)
    exit_code = appctxt.run()
    sys.exit(exit_code)
