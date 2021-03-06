"""
This module creates a PyQt application to show the Ludo Board.
"""

# Python stdlib
import sys
import signal

# PyQt Imports
from PyQt5 import QtGui as QtG
from PyQt5 import QtCore as QtC

from PyQt5 import QtWidgets as QtW
# Our Code
from board_view import BoardView
from game import LudoGame


class LudoView(QtW.QGraphicsView):

    def __init__(self, player_id, game_mode, qparent):
        QtW.QGraphicsView.__init__(self)

        # Window's dimensions
        self.setGeometry(QtC.QRect(500, 100, 904, 904))

        # Add the board
        self.board = BoardView()
        self.setScene(self.board)

        self.game = ThreadedGame(player_id, game_mode)
        self.game.update_board.connect(self.board.paint)
        self.game.update_turn.connect(self.board.showTurn)
        self.game.update_status.connect(qparent.updateStatusBar)

        self.board.paint(self.game.coins)

    def keyPressEvent(self, e):
        if e.key() == QtC.Qt.Key_Escape:
            self.close()


class ThreadedGame(LudoGame, QtC.QThread):

    update_board = QtC.pyqtSignal(object)
    update_turn = QtC.pyqtSignal(object)

    update_status = QtC.pyqtSignal(object, object)

    def __init__(self, player_id, game_mode):
        LudoGame.__init__(self, player_id, game_mode)
        QtC.QThread.__init__(self)

        self.update_board.emit(self.coins)

class LudoWindow(QtW.QMainWindow):

    def __init__(self, player_id, game_mode):
        QtW.QMainWindow.__init__(self)

        self.setGeometry(QtC.QRect(500, 100, 940, 960))
        self.setFixedSize(self.size())

        self.statusBar = QtW.QStatusBar()
        self.setStatusBar(self.statusBar)

        self.view = LudoView(player_id, game_mode, self)

        hbox = QtW.QHBoxLayout()
        hbox.addWidget(self.view)

        mainWidget = QtW.QWidget()
        mainWidget.setLayout(hbox)

        self.setWindowTitle('Ludo')
        
        self.setCentralWidget(mainWidget)
        
        self.show()

    def updateStatusBar(self, player, moves):
        msg = "%s played: %s" % (player.color.title(), ", ".join(moves))
        self.statusBar.showMessage(msg)

def run_gui(player_id, game_mode, start=True):

    # Close on Ctrl + C from terminal
    # https://stackoverflow.com/a/5160720
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QtW.QApplication(sys.argv)

    ludo = LudoWindow(player_id, game_mode)

    if start:
        ludo.view.game.start()

    sys.exit(app.exec_())

if __name__ == '__main__':
    run_gui(0, 0, start=False)
