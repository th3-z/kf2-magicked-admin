import logging
from datetime import datetime

from PySide2.QtCore import Slot
from PySide2.QtWidgets import (QLineEdit, QPlainTextEdit, QPushButton,
                               QVBoxLayout, QWidget)

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
        self.server.signals.post_chat.emit("gui", message, 3)

    @server.setter
    def server(self, server):
        if server == self._server or not server:
            return
        elif self._server:
            self._server.signals.chat.disconnect(self.receive_message)

        self._server = server

        for message in server.chat_worker.log:
            self.receive_message(message.username, message.message, message.user_flags, date=message.date)

        server.signals.chat.connect(self.receive_message)

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
        self.textedit.clear()
