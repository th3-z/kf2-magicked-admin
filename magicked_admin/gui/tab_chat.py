import logging

from PySide2.QtCore import Signal, Slot, QObject
from PySide2.QtWidgets import QVBoxLayout, QPlainTextEdit, QPushButton, QWidget, QLineEdit

logger = logging.getLogger(__name__)


class TabChat(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self._server = None

        self.textedit = QPlainTextEdit(self)
        self.textedit.setReadOnly(True)
        self.clear_button = QPushButton('Clear', self)
        self.clear_button.setDisabled(True)
        self.tb_input = QLineEdit(self)
        self.tb_input.setDisabled(True)
        self.send_button = QPushButton('Send', self)
        self.send_button.setDisabled(True)

        # Lay out all the widgets
        layout = QVBoxLayout(self)
        layout.addWidget(self.textedit)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.tb_input)
        layout.addWidget(self.send_button)

        # Connect slots and signals
        self.clear_button.clicked.connect(self.clear_display)
        self.send_button.clicked.connect(self.send_message)

    @property
    def server(self):
        return self._server

    def send_message(self):
        message = self.tb_input.text()
        print("emit")
        self.server.signals.post_chat.emit("gui", message, 3)

    @server.setter
    def server(self, server):
        self.send_button.setDisabled(False)
        self.tb_input.setDisabled(False)
        self.clear_button.setDisabled(False)
        logger.debug(server.name)
        self._server = server
        server.signals.chat.connect(self.receive_message)

    @Slot(str, str, int)
    def receive_message(self, username, message, user_flags):
        s = """
            <font color='#0f0'>{}</font>: {}
        """.format(username, message)
        self.textedit.appendHtml(s)

    @Slot()
    def clear_display(self):
        self.textedit.clear()
