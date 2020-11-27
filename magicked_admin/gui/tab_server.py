import logging

from PySide2.QtCore import Signal, Slot, QObject, QUrl, QMargins
from PySide2.QtWidgets import QVBoxLayout, QPlainTextEdit, QPushButton, QWidget, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout, QGroupBox, QFormLayout
from PySide2.QtGui import QPixmap, Qt, QFont, QDesktopServices, QPainter
from PySide2.QtCharts import QtCharts
import time

from utils import find_data_file
from database.queries.graphs import players_time, kills_time, noise_filter
from gui.graphs.server import PlayersGraph, KillsGraph
from gui.components.widgets import LabelButton
from web_admin.constants import GAME_TYPE_DISPLAY, DIFF_DISPLAY, LEN_DISPLAY
from server.match import Match
from server.player import Player

logger = logging.getLogger(__name__)


class TabServer(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self._server = None

        layout_columns = QHBoxLayout(self)

        left = QWidget()
        layout_left = QVBoxLayout(left)
        layout_columns.addWidget(left)

        self.form = QGroupBox()
        form_layout = QFormLayout(self.form)

        self.address = QLabel()
        self.username = QLabel()
        self.players_capacity = QLabel()
        self.wave = QLabel()

        self.game_type = LabelButton("", "Change")
        self.difficulty = LabelButton("", "Change")
        self.length = LabelButton("", "Change")
        self.map = LabelButton("", "Change")

        form_layout.addRow(QLabel("Address:"), self.address)
        form_layout.addRow(QLabel("Username:"), self.username)
        form_layout.addRow(QLabel("Players:"), self.players_capacity)
        form_layout.addRow(QLabel("Wave:"), self.wave)
        form_layout.addRow(QLabel("Game mode:"), self.game_type)
        form_layout.addRow(QLabel("Difficulty:"), self.difficulty)
        form_layout.addRow(QLabel("Length:"), self.length)
        form_layout.addRow(QLabel("Map:"), self.map)

        layout_left.addWidget(self.form)
        layout_left.addWidget(QPushButton("Delete"))

        # TODO: Hide right col when window is small
        right = QWidget()
        layout_right = QVBoxLayout(right)
        self.players_graph = PlayersGraph()
        layout_right.addWidget(self.players_graph)
        # layout_right.addWidget(KillsGraph(self, server))
        layout_columns.addWidget(right)

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, server):
        if server == self._server or not server:
            return
        elif self._server:
            self._server.signals.player_join.disconnect(self.players_changed)
            self._server.signals.player_quit.disconnect(self.players_changed)
            self._server.signals.match_start.disconnect(self.match_changed)

        self._server = server

        self.form.setTitle(server.name)
        self.address.setText(self.server.web_admin.web_interface.address)
        self.username.setText(self.server.web_admin.web_interface.username)
        self.players_capacity.setText("{} / {}".format(len(self.server.players), self.server.capacity))

        self.game_type.label.setText(GAME_TYPE_DISPLAY[self.server.match.game_type])
        self.difficulty.label.setText(DIFF_DISPLAY[self.server.match.difficulty])
        self.length.label.setText(LEN_DISPLAY[self.server.match.length])
        self.map.label.setText(self.server.match.level.name)

        self.players_graph.plot(server)

        server.signals.player_join.connect(self.players_changed)
        server.signals.player_quit.connect(self.players_changed)
        server.signals.match_start.connect(self.match_changed)

    @Slot(Player)
    def players_changed(self, player):
        self.players_capacity.setText("{} / {}".format(len(self.server.players), self.server.capacity))
        self.players_graph.plot(self.server)

    @Slot(Match)
    def match_changed(self, match):
        self.game_type.label.setText(GAME_TYPE_DISPLAY[match.game_type])
        self.difficulty.label.setText(DIFF_DISPLAY[match.difficulty])
        self.length.label.setText(LEN_DISPLAY[match.length])
        self.map.label.setText(match.level.name)


