import datetime
import logging
import random
import sys
import time

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout
from PySide2.QtCore import Signal, Slot

from settings import Settings
from gui.tab_log import TabLog
from gui.tab_chat import TabChat


class Gui(QMainWindow):
    width = 900
    height = 450

    def __init__(self, app):
        super().__init__()

        self.app = app

        self.setWindowTitle("Killing Floor 2 Magicked Admin")
        self.setGeometry(0, 0, Gui.width, Gui.height)

        self.tab_widget = TabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.show()


class TabWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        # Init tabs
        self.tabs = QTabWidget()
        self.tabs.resize(Gui.height, Gui.width)

        self.tab_server = QWidget()
        self.tab_log = QWidget()
        self.tab_chat = QWidget()

        self.tabs.addTab(self.tab_server, "Server")
        self.tabs.addTab(self.tab_log, "Log")
        self.tabs.addTab(self.tab_chat, "Chat")

        self.tab_log.layout = QVBoxLayout(self)
        self.tab_log.layout.addWidget(TabLog(self))
        self.tab_log.setLayout(self.tab_log.layout)

        self.tab_chat.layout = QVBoxLayout(self)
        self.tab_chat.layout.addWidget(TabChat(self))
        self.tab_chat.setLayout(self.tab_chat.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
