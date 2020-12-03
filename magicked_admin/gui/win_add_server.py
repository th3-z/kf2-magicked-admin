import logging

from gui.vendor.waiting_spinner import QtWaitingSpinner
from PySide2.QtCore import QObject, QRunnable, Qt, QThreadPool, Signal, Slot
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QFormLayout, QGroupBox, QHBoxLayout, QLabel,
                               QLineEdit, QMessageBox, QPushButton,
                               QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
from settings import ServerConfig
from utils.net import resolve_address
from web_admin.web_interface import AuthorizationException, WebInterface

logger = logging.getLogger(__name__)

CONN_SUCCESS = 0
CONN_FAIL_CRED = 1
CONN_FAIL_ADDR = 2


def connection_test(address, username, password):
    address = resolve_address(address)
    if not address:
        return CONN_FAIL_ADDR

    try:
        WebInterface(address, username, password)
    except AuthorizationException:
        return CONN_FAIL_CRED

    return CONN_SUCCESS


class WinAddServerSignals(QObject):
    connection_status = Signal(int)


class TestConnWorker(QRunnable):
    def __init__(self, address, username, password, receiver):
        QRunnable.__init__(self)
        self.address = address
        self.username = username
        self.password = password

        self.receiver = receiver

    def run(self):
        status = connection_test(self.address, self.username, self.password)
        self.receiver.signals.connection_status.emit(status)


class WinAddServer(QWidget):

    def __init__(self, magicked_admin):
        QWidget.__init__(self)

        self.signals = WinAddServerSignals()
        self.magicked_admin = magicked_admin

        self.setWindowTitle("Add server")
        self.setFixedSize(282, 289)
        self.setWindowModality(Qt.ApplicationModal)

        form = QGroupBox("Server details")
        form_layout = QFormLayout(form)
        self.server_name = QLineEdit()
        form_layout.addRow(QLabel("Server name:"), self.server_name)
        self.address = QLineEdit()
        form_layout.addRow(QLabel("Address:"), self.address)
        self.username = QLineEdit()
        form_layout.addRow(QLabel("Username:"), self.username)
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        form_layout.addRow(QLabel("Password:"), self.password)

        form_test_widget = QWidget()
        form_test_layout = QHBoxLayout(form_test_widget)
        test_button = QPushButton("Test connectivity")
        form_test_layout.addWidget(test_button)
        self.status_spinner = QtWaitingSpinner(self, centerOnParent=False)
        self.status_spinner.setFixedSize(16, 16)
        self.status_spinner.setLineLength(6)
        self.status_spinner.setInnerRadius(2)
        self.status_spinner.setNumberOfLines(11)
        self.status_spinner.setLineWidth(1)
        form_test_layout.addWidget(self.status_spinner)
        self.status_response = QLabel()
        form_test_layout.addWidget(self.status_response)
        form_layout.addWidget(form_test_widget)

        buttons = QWidget()
        buttons_layout = QHBoxLayout(buttons)
        cancel_button = QPushButton("cancel")
        add_button = QPushButton("Add")
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        buttons_layout.addWidget(add_button)

        layout = QVBoxLayout(self)
        layout.addWidget(form)
        layout.addWidget(buttons)

        cancel_button.clicked.connect(self.close)
        add_button.clicked.connect(self.add_server)
        test_button.clicked.connect(self.test_connectivity)
        self.le_style = self.address.styleSheet()

        self.signals.connection_status.connect(self.receive_conn_status)

    def add_server(self):
        required_fields = [self.address, self.username, self.server_name, self.password]

        missing_field = False
        for field in required_fields:
            field.setStyleSheet(self.le_style)
            if not field.text():
                field.setStyleSheet("background-color: #ff5555;")
                missing_field = True
        if missing_field:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Fields are missing input.")
            msg.setWindowTitle("Cannot add server")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        address = resolve_address(self.address.text()) or self.address.text()
        config = ServerConfig(address, self.username.text(), self.password.text(), '123', '', '1')
        self.magicked_admin.add_server(self.server_name.text(), config)
        self.close()

    @Slot(int)
    def receive_conn_status(self, status):
        self.status_spinner.hide()
        self.status_spinner.stop()
        self.status_response.show()
        self.address.setStyleSheet(self.le_style)
        self.username.setStyleSheet(self.le_style)
        self.password.setStyleSheet(self.le_style)

        if status == CONN_SUCCESS:
            self.status_response.setPixmap(QIcon.fromTheme("dialog-ok").pixmap(16))
        elif status == CONN_FAIL_CRED:
            self.status_response.setPixmap(QIcon.fromTheme("dialog-cancel").pixmap(16))
            self.username.setStyleSheet("background-color: #ff5555;")
            self.password.setStyleSheet("background-color: #ff5555;")
        elif status == CONN_FAIL_ADDR:
            self.status_response.setPixmap(QIcon.fromTheme("dialog-cancel").pixmap(16))
            self.address.setStyleSheet("background-color: #ff5555;")

    def test_connectivity(self):
        self.status_spinner.start()
        self.status_spinner.show()
        self.status_response.hide()
        worker = TestConnWorker(self.address.text(), self.username.text(), self.password.text(), self)
        QThreadPool.globalInstance().start(worker)
