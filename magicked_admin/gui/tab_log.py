import logging

from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QPlainTextEdit, QPushButton, QVBoxLayout, QWidget


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


class TabLog(QWidget):
    COLORS = {
        logging.DEBUG: 'black',
        logging.INFO: 'blue',
        logging.WARNING: 'orange',
        logging.ERROR: 'red',
        logging.CRITICAL: 'purple',
    }

    def __init__(self, parent):
        super().__init__(parent)

        self.textedit = QPlainTextEdit(self)
        font = QFont('nosuchfont')
        font.setStyleHint(font.Monospace)
        self.textedit.setFont(font)
        self.textedit.setReadOnly(True)
        self.clear_button = QPushButton('Clear log window', self)

        logger = logging.getLogger()
        handler = QtHandler(self.update_status)
        formatter = logging.Formatter("[%(asctime)s %(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Lay out all the widgets
        layout = QVBoxLayout(self)
        layout.addWidget(self.textedit)
        layout.addWidget(self.clear_button)

        # Connect slots and signals
        self.clear_button.clicked.connect(self.clear_display)

    @Slot(str, logging.LogRecord)
    def update_status(self, status, record):
        color = self.COLORS.get(record.levelno, 'black')
        s = '<pre><font color="%s">%s</font></pre>' % (color, status)
        self.textedit.appendHtml(s)

    @Slot()
    def clear_display(self):
        self.textedit.clear()
