"""
Killing Floor 2 Magicked Admin
Copyright th3-z (the_z) 2018
Released under the terms of the MIT license
"""

import gettext
import os
import sys
import argparse
import logging
from signal import signal, SIGTERM, SIGINT
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Signal, QObject

from chatbot.chatbot import Chatbot
from chatbot.motd_updater import MotdUpdater
from chatbot.commands.command_map import CommandMap
from server.server import Server, ServerSignals
from settings import Settings
from utils import find_data_file
from web_admin.state_transition_worker import StateTransitionWorker
from web_admin import WebAdmin
from web_admin.web_interface import WebInterface, AuthorizationException
from web_admin.chat_worker import ChatWorker
from lua_bridge.lua_bridge import LuaBridge
from database import db_init

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
    certifi.core.where = requests_ca_bundle_path

    import requests.utils
    import requests.adapters

    requests.utils.DEFAULT_CA_BUNDLE_PATH = requests_ca_bundle_path
    requests.adapters.DEFAULT_CA_BUNDLE_PATH = requests_ca_bundle_path


class MagickedAdminSignals(QObject):
    server_configured = Signal(Server)


class MagickedAdmin:

    def __init__(self):
        self.version = "0.2.0"
        self.servers = []
        self.qthreads = []
        self.ui = None
        self.signals = MagickedAdminSignals()

    def add_server(self, server_name, server_config):
        logger.info("Initialising {}".format(server_name))
        if server_name in [server.name for server in self.servers]:
            return

        web_interface = WebInterface(
            server_config.address, server_config.username,
            server_config.password, server_name
        )
        web_admin = WebAdmin(web_interface)

        server = Server(
            web_admin, server_name, game_password=server_config.game_password, url_extras=server_config.url_extras
        )
        self.servers.append(server)

        chat_worker = ChatWorker(server)
        chat_worker.start()
        self.qthreads.append(chat_worker)

        state_transition_worker = StateTransitionWorker(
            server, refresh_rate=int(server_config.refresh_rate)
        )
        state_transition_worker.start()
        self.qthreads.append(state_transition_worker)

        chatbot = Chatbot(server)
        commands = CommandMap().get_commands(
            server, chatbot, MotdUpdater(server)
        )
        for command_name, command in commands.items():
            chatbot.add_command(command_name, command)

        chatbot.run_init(find_data_file(
            "conf/scripts/" + server_name + ".init"
        ))
        #lua_bridge = LuaBridge(server, chatbot)
        #chatbot.lua_bridge = lua_bridge

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

    def run(self):
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

        self.banner()
        db_init()

        for server_name, server_config in Settings.servers.items():
            self.add_server(server_name, server_config)

    def close(self, signal=None, frame=None):
        logger.info("Program interrupted, shutting down...")
        for server in self.servers:
            server.close()
        for qthread in self.qthreads:
            qthread.close()

    def banner(self):
        version_text = "<<{}{}>>".format(
            self.version, "#DEBUG" if Settings.debug else ""
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
    magicked_admin = MagickedAdmin()
    signal(SIGINT, magicked_admin.close)
    signal(SIGTERM, magicked_admin.close)

    if GUI_MODE:
        from gui import Gui
        app = QApplication(sys.argv)
        gui = Gui(app, magicked_admin)
        magicked_admin.ui = gui
        magicked_admin.run()
        app.exec_()
        magicked_admin.close()

    elif len(Settings.servers.keys()) < 1:
        Settings.append_template()
        print(
            " [!] No servers have been configured yet, "
            "please amend '{}' with your server details".format(
                Settings.config_path_display
            )
        )

    else:
        magicked_admin.run()

    exit = False
    while not exit:
        exit = True
        for thread in magicked_admin.qthreads:
            if not thread.isFinished():
                exit = False

