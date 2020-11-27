import logging

from PySide2.QtCore import Signal, Slot, QObject, QUrl, QMargins
from PySide2.QtWidgets import QVBoxLayout, QPlainTextEdit, QPushButton, QWidget, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout, QGroupBox, QFormLayout
from PySide2.QtGui import QPixmap, Qt, QFont, QDesktopServices, QPainter

from utils import find_data_file

logger = logging.getLogger(__name__)


class TabHome(QWidget):

    def __init__(self, parent, magicked_admin):
        super().__init__(parent)

        header = QLabel()
        header.setText("Killing Floor 2 Magicked Admin")
        header.setFont(QFont('nosuchfont', 24))
        header.setAlignment(Qt.AlignHCenter)

        version = QLabel()
        version.setText(magicked_admin.version)
        version.setAlignment(Qt.AlignHCenter)

        logo = QLabel()
        pm_logo = QPixmap(find_data_file('gui/res/logo.png'))
        pm_logo.scaledToHeight(64)
        logo.setPixmap(pm_logo)
        logo.setAlignment(Qt.AlignHCenter)

        guide = QLabel()
        guide.setText("<em>No server selected, add or select a server at the top-right.</em>")
        guide.setAlignment(Qt.AlignHCenter)

        docs = QLabel()
        doclink = "https://kf2-ma.th3-z.xyz"
        docs.setText("<a href='{}'>Documentation</a>".format(doclink))
        docs.setAlignment(Qt.AlignHCenter)
        docs.linkActivated.connect(self.link)

        layout = QVBoxLayout(self)
        layout.addWidget(header)
        layout.addWidget(version)
        layout.addWidget(logo)
        layout.addWidget(guide)
        layout.addWidget(docs)
        layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

    def link(self, url):
        QDesktopServices.openUrl(QUrl(url))
