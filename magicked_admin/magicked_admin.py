"""
Killing Floor 2 Magicked Admin
Copyright th3-z (the_z) 2018
Released under the terms of the MIT license
"""

import argparse
import gettext
import logging
import os
import sys
import time
from signal import SIGINT, SIGTERM, signal

from database import db_init
from PySide2.QtCore import QObject, Signal, QThread
from PySide2.QtWidgets import QApplication
from server.server import Server
from settings import Settings
from utils import find_data_file
from web_admin import WebAdmin
from web_admin.web_interface import WebInterface

gettext.bindtextdomain('magicked_admin', find_data_file('locale'))
gettext.textdomain('magicked_admin')
gettext.install('magicked_admin', find_data_file('locale'))

parser = argparse.ArgumentParser(
    description='Killing Floor 2 Magicked Administrator'
)
parser.add_argument(
    '-n', '--nogui', action='store_true',
    help='Disables the GUI for headless operation'
)
args = parser.parse_args()

root_logger = logging.getLogger()
logger = logging.getLogger(__name__)

GUI_MODE = not args.nogui

if hasattr(sys, "frozen"):
    import certifi.core

    requests_ca_bundle_path = find_data_file("./certifi/cacert.pem")
    os.environ["REQUESTS_CA_BUNDLE"] = requests_ca_bundle_path
    os.environ["QT_PLUGIN_PATH"] = find_data_file("lib/Qt/plugins")
    certifi.core.where = requests_ca_bundle_path

    import requests.adapters
    import requests.utils

    requests.utils.DEFAULT_CA_BUNDLE_PATH = requests_ca_bundle_path
    requests.adapters.DEFAULT_CA_BUNDLE_PATH = requests_ca_bundle_path


class MagickedAdminSignals(QObject):
    server_configured = Signal(Server)


class MagickedAdmin:
    def __init__(self):
        self.servers = []
        self.signals = MagickedAdminSignals()

        signal(SIGINT, self.close)
        signal(SIGTERM, self.close)

        self.ui = None

        self.banner()
        db_init()

    def add_server(self, server_name, server_config):
        logger.info("Adding new server '{}'".format(server_name))
        if server_name in [server.name for server in self.servers]:
            return

        web_interface = WebInterface(
            server_config.address, server_config.username, server_config.password
        )
        web_admin = WebAdmin(web_interface)

        server = Server(
            # TODO: Pass full configuration
            web_admin, server_name, game_password=server_config.game_password, url_extras=server_config.url_extras
        )
        self.servers.append(server)

        if server_name not in Settings.servers.keys():
            Settings.add_server(server_name, server_config)

        self.signals.server_configured.emit(server)

    def remove_server(self, name):
        if name not in self.servers.keys():
            return

        for server in self.servers:
            if server.name == name:
                server.close()
                self.servers.remove(server)
                Settings.remove_server(name)

    def configure_servers(self):
        for server_name, server_config in Settings.servers.items():
            self.add_server(server_name, server_config)

    def close(self, signal=None, frame=None):
        logger.info("Program interrupted, shutting down...")

        if self.ui:
            self.ui.close()

        for server in self.servers:
            server.close()
            while not server.is_finished:
                continue

    @staticmethod
    def banner():
        version_text = "<<{}{}>>".format(
            Settings.version, "#DEBUG" if Settings.debug else ""
        )

        # figlet -f rectangles "example"
        lines = [
            "               _     _         _\n"
            " _____ ___ ___|_|___| |_ ___ _| |\n",
            "|     | .'| . | |  _| '_| -_| . |\n",
            "|_|_|_|__,|_  |_|___|_,_|___|___|\n",
            "        _ |___| _ \n",
            "  ___ _| |_____|_|___   {}\n".format(version_text),
            " | .'| . |     | |   |  {}\n".format(Settings.banner_url),
            " |__,|___|_|_|_|_|_|_|\n"
        ]
        print(str.join('', lines))


if __name__ == "__main__":
    root_logger.setLevel(Settings.log_level)
    formatter = logging.Formatter("[%(asctime)s %(levelname)-5.5s] %(message)s", "%Y-%m-%d %H:%M:%S")

    file_handler = logging.FileHandler(
        os.environ.get("LOGFILE", find_data_file("conf/magicked_admin.log")),
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

    app = QApplication(sys.argv)
    magicked_admin = MagickedAdmin()


    if GUI_MODE:
        from gui.gui import Gui
        gui = Gui(app, magicked_admin)
        magicked_admin.ui = gui

    elif len(Settings.servers.keys()) < 1:
        Settings.append_template()
        print(
            " [!] No servers have been configured yet, please amend '{}' with your server details".format(
                Settings.config_path_display
            )
        )

    magicked_admin.configure_servers()

    app.exec_()
    magicked_admin.close()
