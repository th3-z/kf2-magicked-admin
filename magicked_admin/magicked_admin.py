"""
Killing Floor 2 Magicked Admin
Copyright th3-z (the_z) 2018
Released under the terms of the MIT license
"""

import os
import signal
import sys

from colorama import init
from termcolor import colored

from chatbot.chatbot import Chatbot
from server.motd_updater import MotdUpdater
from server.server import Server
from settings import Settings
from utils import banner, die, find_data_file, info, warning
from utils.text import str_to_bool

init()

banner()

settings = Settings()

REQUESTS_CA_BUNDLE_PATH = find_data_file("./certifi/cacert.pem")

if hasattr(sys, "frozen"):
    import certifi.core

    os.environ["REQUESTS_CA_BUNDLE"] = REQUESTS_CA_BUNDLE_PATH
    certifi.core.where = REQUESTS_CA_BUNDLE_PATH

    import requests.utils
    import requests.adapters
    requests.utils.DEFAULT_CA_BUNDLE_PATH = REQUESTS_CA_BUNDLE_PATH
    requests.adapters.DEFAULT_CA_BUNDLE_PATH = REQUESTS_CA_BUNDLE_PATH


class MagickedAdmin:
    
    def __init__(self):
        signal.signal(signal.SIGINT, self.terminate)
        self.servers = []
        self.sigint_count = 0

    def run(self):
        for server_name in settings.sections():

            server = Server(server_name,
                            settings.setting(server_name, "address"),
                            settings.setting(server_name, "username"),
                            settings.setting(server_name, "password")
                            )

            server.game_password = \
                settings.setting(server_name, "game_password")
            server.url_extras = \
                settings.setting(server_name, "url_extras")

            level_threshold = int(settings.setting(server_name, "level_threshold"))
            if level_threshold > 0:
                server.level_threshold = level_threshold

            dosh_threshold = int(settings.setting(server_name, "dosh_threshold"))
            if dosh_threshold > 0:
                server.dosh_threshold = dosh_threshold

            has_motd_scoreboard = str_to_bool(
                settings.setting(server_name, "motd_scoreboard")
            )

            if has_motd_scoreboard:
                scoreboard_type = settings.setting(server_name, "scoreboard_type")
                MotdUpdater(server, scoreboard_type).start()

            self.servers.append(server)

            Chatbot(server,
                    str_to_bool(settings.setting(server_name, "enable_greeter")),
                    settings.setting(server_name, "username")
                    )

        info("Initialisation complete!\n")

        while True:
            command = input()
            for server in self.servers:
                server.web_admin.chat.submit_message(command)
            
    def terminate(self, signal, frame):
        if self.sigint_count > 2:
            print() # \n
            warning("Closing immediately!")
            os._exit(0)
            return
        
        self.sigint_count += 1
        if self.sigint_count > 1:
            return
        
        print() # \n
        info("Program interrupted, saving data...")

        for server in self.servers:
            server.close()

        die()


if __name__ == "__main__":
    application = MagickedAdmin()
    application.run()
