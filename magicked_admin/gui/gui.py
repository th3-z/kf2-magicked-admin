import logging

from PySide2.QtWidgets import QMainWindow, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QStatusBar, QLabel, QComboBox, QSpacerItem, QSizePolicy, QHBoxLayout
from PySide2.QtCore import Slot, QRect

from server.server import Server
from gui.tab_log import TabLog
from gui.tab_chat import TabChat
from gui.tab_server import TabServer
from gui.win_add_server import WinAddServer

logger = logging.getLogger(__name__)


class Gui(QMainWindow):
    width = 900
    height = 450

    def __init__(self, app, magicked_admin):
        super().__init__()

        self.app = app
        self.magicked_admin = magicked_admin
        self.servers = magicked_admin.servers

        self.setWindowTitle("Killing Floor 2 Magicked Admin")
        # self.setGeometry(0, 0, Gui.width, Gui.height)

        # Menu bar
        self.menubar = self.menuBar()
        about = self.menubar.addMenu("About")
        about.triggered[QAction].connect(self.mb_process_trigger)

        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.addWidget(
            QLabel("Status bar test")
        )
        self.setStatusBar(self.status_bar)
        self.status_bar.show()

        # Main window
        window = QWidget(self)
        layout = QVBoxLayout(window)

        # Toolbar
        toolbar = QWidget()
        toolbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.cb_servers = QComboBox()
        self.cb_servers.addItem("Select a server...")
        magicked_admin.signals.server_configured.connect(self.receive_server_configured)
        self.cb_servers.currentIndexChanged.connect(self.cb_servers_selection)

        self.pb_add_server = QPushButton("Add server")
        self.pb_add_server.clicked.connect(self.pop_add_server)
        self.win_add_server = None

        toolbar_layout.addWidget(self.cb_servers)
        toolbar_layout.addWidget(self.pb_add_server)

        layout.addWidget(toolbar)

        # Tabs
        self.tab_widget = TabWidget(window, magicked_admin)
        layout.addWidget(self.tab_widget)

        self.setCentralWidget(window)
        self.show()

    def pop_add_server(self):
        self.win_add_server = WinAddServer(self.magicked_admin)
        self.win_add_server.show()

    def mb_process_trigger(self, q):
        logger.debug(q.text())

    def cb_servers_selection(self, i):
        if i > 0:
            server = self.servers[i-1]
        else:
            server = None

        self.tab_widget.tab_server.server = server

        if server:
            self.tab_widget.tab_chat.server = server
            self.tab_widget.toggle_server_tabs(True)
        else:
            self.tab_widget.toggle_server_tabs(False)

    @Slot(Server)
    def receive_server_configured(self, server):
        self.cb_servers.addItem(server.name)


class TabWidget(QWidget):
    def __init__(self, parent, magicked_admin):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        # Init tabs
        self.tabs = QTabWidget()
        self.tabs.resize(Gui.height, Gui.width)

        self.tab_server = TabServer(self, magicked_admin)
        self.tab_log = TabLog(self)
        self.tab_chat = TabChat(self)

        self.tabs.addTab(self.tab_server, "Server")
        self.tabs.addTab(self.tab_log, "Log")
        self.tabs.addTab(self.tab_chat, "Chat")

        layout.addWidget(self.tabs)

        self.toggle_server_tabs(False)

    def toggle_server_tabs(self, state):
        self.tabs.setTabEnabled(2, state)
