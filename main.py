"""
This module provides the main entry point to the Ludo Application.

This is what should be run from the CLI: python main.py
"""

# Python stdlib
import sys
import signal

# PyQt Imports
from PyQt5 import QtCore as QtC

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGraphicsView

# Our Code
from board_view import BoardView
from game import LudoGame


class LudoApp(QGraphicsView):

    def __init__(self):
        QGraphicsView.__init__(self)

        # Window's dimensions
        self.setGeometry(QtC.QRect(500, 100, 904, 904))

        # Prevent Window Resize
        self.setFixedSize(self.size())

        # Add the board
        self.board = BoardView()
        self.setScene(self.board)

        self.game = ThreadedGame()
        self.game.update_board.connect(self.board.paint)

        self.board.paint(self.game.coins)

    def keyPressEvent(self, e):
        if e.key() == QtC.Qt.Key_Escape:
            self.close()


class ThreadedGame(LudoGame, QtC.QThread):

    update_board = QtC.pyqtSignal(object)

    def __init__(self):
        LudoGame.__init__(self)
        QtC.QThread.__init__(self)

        self.update_board.emit(self.coins)

if __name__ == '__main__':

    # Close on Ctrl + C from terminal
    # https://stackoverflow.com/a/5160720
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)

    ludo = LudoApp()

    ludo.show()

    ludo.game.start()

    sys.exit(app.exec_())
