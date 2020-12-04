from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QMainWindow, QMessageBox, QAction, qApp, QDialogButtonBox, QLineEdit, QSizePolicy, QLabel
from PyQt5.QtGui import QIcon, QFont, QDrag, QPixmap, QPainter
from PyQt5.QtCore import pyqtSlot, QMimeData
from PyQt5.QtCore import Qt
from PyQt5 import QtSvg

# TODO: Use inheritance to merge equivalent things

class BoardSquare(QtSvg.QSvgWidget):
    WHITE_SQUARE = 0
    BLACK_SQUARE = 1
    GREEN_SQUARE = 2
    RED_SQUARE = 3
    WHITE_ROOK = 4
    BLACK_ROOK = 5
    PIECES = 6

    def __init__(self, images, background, action):
        super(QWidget, self).__init__(images[background])
        self.images = images
        self.action = action
        # self.mouseReleaseEvent=click

        self.background = background
        self.piece = background
        self.highlighted = False

        self.label = QLabel(self)
        self.label.setText("   ")
        self.label.move(10, 10)
        self.label.setFont(QFont('Arial', 48))

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        event.accept()
        self.tmpPiece = self.piece
        self.setPiece(self.GREEN_SQUARE)

    def dragLeaveEvent(self, event):
        self.piece = self.tmpPiece
        self.setPiece(self.piece)
        event.accept()

    def dropEvent(self, event):
        event.accept()
        # TODO: Figure out how to get rid of the 0
        src = int(event.mimeData().text())
        self.action(src)

    def reset(self):
        self.piece = self.background
        self.load(self.images[self.background])
        self.label.setText("")

    def setPiece(self, piece):
        self.piece = piece
        if piece > 1:
            self.label.setText("")
        self.load(self.images[piece])

    def setStatus(self, piece, score):
        self.setPiece(piece)
        self.setScore(score)

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




class BarracksSquare(QtSvg.QSvgWidget):
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
        self.click = click
        self.mousePressEvent=click

        self.background = background
        self.piece = background
        self.highlighted = False

        self.label = QLabel(self)
        self.label.setText("   ")
        self.label.move(10, 10)
        self.label.setFont(QFont('Arial', 48))

        self.setAcceptDrops(True)

    # def dragEnterEvent(self, event):
    #     event.accept()
    #     self.tmpPiece = self.piece
    #     self.setPiece(self.GREEN_SQUARE)

    # def dragLeaveEvent(self, event):
    #     self.piece = self.tmpPiece
    #     self.setPiece(self.piece)
    #     event.accept()

    # def dropEvent(self, event):
    #     event.accept()
    #     self.click(0)

    def used(self):
        self.setPiece(0)
        self.mouseReleaseEvent=()

    def reset(self):
        self.piece = self.background
        self.load(self.images[self.background])
        self.label.setText("")

    def setPiece(self, piece):
        self.piece = piece
        if piece > 1:
            self.label.setText("")
        self.load(self.images[piece])

    def setStatus(self, piece, score):
        self.setPiece(piece)
        self.setScore(score)

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

