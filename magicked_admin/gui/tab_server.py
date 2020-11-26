import logging

from PySide2.QtCore import Signal, Slot, QObject, QUrl, QMargins
from PySide2.QtWidgets import QVBoxLayout, QPlainTextEdit, QPushButton, QWidget, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout
from PySide2.QtGui import QPixmap, Qt, QFont, QDesktopServices, QPainter
from PySide2.QtCharts import QtCharts
import time

from utils import find_data_file
from database.queries.graphs import players_time, kills_time, noise_filter
from gui.graphs.server import PlayersGraph, KillsGraph

logger = logging.getLogger(__name__)


class WelcomeWi(QWidget):
    def __init__(self, parent, magicked_admin):
        super().__init__(parent)

        self.header = QLabel()
        self.header.setText("Killing Floor 2 Magicked Admin")
        self.header.setFont(QFont('nosuchfont', 24))
        self.header.setAlignment(Qt.AlignHCenter)

        self.version = QLabel()
        self.version.setText(magicked_admin.version)
        self.version.setAlignment(Qt.AlignHCenter)

        self.logo = QLabel()
        pm_logo = QPixmap(find_data_file('gui/res/logo.png'))
        pm_logo.scaledToHeight(64)
        self.logo.setPixmap(pm_logo)
        self.logo.setAlignment(Qt.AlignHCenter)

        self.guide = QLabel()
        self.guide.setText("<em>No server selected, add or select a server at the top-right.</em>")
        self.guide.setAlignment(Qt.AlignHCenter)

        self.docs = QLabel()
        doclink = "https://kf2-ma.th3-z.xyz"
        self.docs.setText("<a href='{}'>Documentation</a>".format(doclink))
        self.docs.setAlignment(Qt.AlignHCenter)
        self.docs.linkActivated.connect(self.link)

        layout = QVBoxLayout(self)
        layout.addWidget(self.header)
        layout.addWidget(self.version)
        layout.addWidget(self.logo)
        layout.addWidget(self.guide)
        layout.addWidget(self.docs)
        layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

    def link(self, url):
        QDesktopServices.openUrl(QUrl(url))


class ServerWi(QWidget):
    def __init__(self, parent, server):
        super().__init__(parent)

        layout_columns = QHBoxLayout(self)

        left = QWidget()
        layout_left = QVBoxLayout(left)
        layout_left.addWidget(QLabel(server.name))
        layout_columns.addWidget(left)

        # TODO: Hide right col when window is small
        right = QWidget()
        layout_right = QVBoxLayout(right)
        layout_right.addWidget(PlayersGraph(self, server))
        layout_right.addWidget(KillsGraph(self, server))
        layout_columns.addWidget(right)





class TabServer(QWidget):

    def __init__(self, parent, magicked_admin):
        super().__init__(parent)

        self._server = None

        self.welcome_widget = WelcomeWi(self, magicked_admin)
        self.server_widget = None

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(
            self.welcome_widget
        )

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, server):
        if server == self._server:
            return

        if not server:
            self.server_widget.deleteLater()
            self.server_widget = None
            self.welcome_widget.show()
        else:
            self.welcome_widget.hide()
            self.server_widget = ServerWi(self, server)
            self.layout.addWidget(self.server_widget)
        self._server = server


