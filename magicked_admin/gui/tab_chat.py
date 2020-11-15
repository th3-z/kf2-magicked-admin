import logging

from PySide2.QtCore import Signal, Slot, QObject
from PySide2.QtWidgets import QVBoxLayout, QPlainTextEdit, QPushButton, QWidget

from web_admin.chat_worker import ChatSignals


class Signaller(QObject):
    signal = Signal(str, logging.LogRecord)


class QtHandler(logging.Handler):
    def __init__(self, slotfunc, *args, **kwargs):
        super(QtHandler, self).__init__(*args, **kwargs)
        self.signaller = Signaller()
        self.signaller.signal.connect(slotfunc)

    def emit(self, record):
        s = self.format(record)
        self.signaller.signal.emit(s, record)


class TabChat(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.textedit = QPlainTextEdit(self)
        self.textedit.setReadOnly(True)
        self.clear_button = QPushButton('Clear', self)
        self.send_button = QPushButton('Send', self)

        # Lay out all the widgets
        layout = QVBoxLayout(self)
        layout.addWidget(self.textedit)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.send_button)

        # Connect slots and signals
        self.clear_button.clicked.connect(self.clear_display)
        cs = ChatSignals()
        cs.signal_chat.connect(self.receive_message)


    @Slot(str)
    def receive_message(self, message):
        s = '<pre><font color="">%s</font></pre>' % message
        self.textedit.appendHtml(s)

    @Slot()
    def clear_display(self):
        self.textedit.clear()
