import logging

from PySide2.QtCore import Signal, Slot, QObject
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QPlainTextEdit, QPushButton, QWidget, QLineEdit, QLabel

from gui.components.player import PlayerWidget

logger = logging.getLogger(__name__)


class TabPlayers(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self._server = None
        self.player_widgets = []

        layout = QHBoxLayout(self)

        left = QWidget()
        self.left_layout = QVBoxLayout(left)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.addWidget(QLabel("Dummy"))

        layout.addWidget(left)
        layout.addWidget(right)


    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, server):
        if server == self._server or not server:
            return
        elif self._server:
            for pw in self.player_widgets:
                pw.deleteLater()
            self.player_widgets = []
            # Disconnect signals, cleanup

        self._server = server

        for player in server.players:
            pw = PlayerWidget(player)
            self.left_layout.addWidget(pw)
            self.player_widgets.append(pw)
