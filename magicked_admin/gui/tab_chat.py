import logging
from datetime import datetime

from PySide2.QtCore import Slot
from PySide2.QtWidgets import (QLineEdit, QPlainTextEdit, QPushButton,
                               QVBoxLayout, QWidget, QHBoxLayout)

from web_admin.constants import USER_TYPE_ADMIN

logger = logging.getLogger(__name__)


class TabChat(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self._server = None

        self.textedit = QPlainTextEdit(self)
        self.textedit.setReadOnly(True)
        self.clear_button = QPushButton('Clear', self)
        self.tb_input = QLineEdit(self)
        self.send_button = QPushButton('Send', self)

        # Lay out all the widgets
        layout = QVBoxLayout(self)
        layout.addWidget(self.textedit)

        input_widget = QWidget()
        input_layout = QHBoxLayout(input_widget)
        input_layout.addWidget(self.clear_button)
        input_layout.addWidget(self.tb_input)
        input_layout.addWidget(self.send_button)
        layout.addWidget(input_widget)

        # Connect slots and signals
        self.tb_input.returnPressed.connect(self.send_message)
        self.clear_button.clicked.connect(self.clear_display)
        self.send_button.clicked.connect(self.send_message)

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, server):
        if server == self._server or not server:
            return
        elif self._server:
            self._server.signals.chat.disconnect(self.receive_message)

        self._server = server
        self.textedit.clear()

        for message in server.chat_worker.log:
            self.receive_message(message.username, message.message, message.user_flags, date=message.date)

        server.signals.chat.connect(self.receive_message)

    def send_message(self):
        message = self.tb_input.text()
        self.tb_input.clear()
        self.server.signals.post_chat.emit("gui", message, 3)

    @Slot(str, str, int)
    def receive_message(self, username, message, user_flags, date=None):
        if date:
            time = datetime.utcfromtimestamp(date).strftime("%Y/%m/%d %H:%M")
        else:
            time = datetime.now().strftime("%Y/%m/%d %H:%M")

        if user_flags & USER_TYPE_ADMIN:
            color = "#f47029"
        else:
            color = "#29aaf4"

        s = """
            {} <font color='{}'>{}</font>: {}
        """.format(time, color, username, message)
        self.textedit.appendHtml(s)

    @Slot()
    def clear_display(self):
        self.server.chat_worker.log = []
        self.textedit.clear()
