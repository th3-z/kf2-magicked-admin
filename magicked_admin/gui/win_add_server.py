import logging
from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QMessageBox
from PySide2.QtCore import Qt

from utils.net import resolve_address
from web_admin.web_interface import WebInterface, AuthorizationException

logger = logging.getLogger(__name__)


class WinAddServer(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle("Add server")
        self.setFixedSize(295, 263)
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
        test_button = QPushButton("Test connectivity")
        form_layout.addWidget(test_button)

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
        test_button.clicked.connect(self.test_settings)

    def test_settings(self):
        address = resolve_address(self.address.text())
        if address:
            self.address.setText(address)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Address ({}) is not responding.".format(self.address.text()))
            msg.setWindowTitle("Test failed")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        try:
            WebInterface(self.address.text(), self.username.text(), self.password.text())
        except AuthorizationException:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Incorrect credentials.")
            msg.setWindowTitle("Connectivity test failed")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Successfully logged in.".format(self.address.text()))
        msg.setWindowTitle("Connectivity test successful")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
