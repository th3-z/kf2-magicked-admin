import logging

from PySide2.QtCore import Signal, Slot, QObject, QUrl
from PySide2.QtWidgets import QVBoxLayout, QPlainTextEdit, QPushButton, QWidget, QLabel, QSpacerItem, QSizePolicy
from PySide2.QtGui import QPixmap, Qt, QFont, QDesktopServices

from utils import find_data_file

logger = logging.getLogger(__name__)


class TabServer(QWidget):

    def __init__(self, parent, magicked_admin):
        super().__init__(parent)

        self._server = None

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

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, server):
        self._server = server

    def link(self, url):
        QDesktopServices.openUrl(QUrl(url))
