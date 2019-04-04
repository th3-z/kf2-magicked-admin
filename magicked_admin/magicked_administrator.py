'''

Killing Floor 2 Magicked Administrator
Copyright th3-z (the_z) 2018
Released under the terms of the MIT license

== Task list ==
    # Figlet splash screen
    # Regression tests
    # Clean up PEP8 violations


'''

import logging
import os
import signal
import sys

from colorama import init
from termcolor import colored

from chatbot.chatbot import Chatbot
from server.server import Server
from settings import Settings
from utils import DEBUG, die, find_data_file
from utils.text import str_to_bool

init()



settings = Settings()

REQUESTS_CA_BUNDLE_PATH =  find_data_file("./certifi/cacert.pem")

if hasattr(sys, "frozen"):
    import certifi.core

    os.environ["REQUESTS_CA_BUNDLE"] = REQUESTS_CA_BUNDLE_PATH
    certifi.core.where = REQUESTS_CA_BUNDLE_PATH

    import requests.utils
    import requests.adapters
    requests.utils.DEFAULT_CA_BUNDLE_PATH = REQUESTS_CA_BUNDLE_PATH
    requests.adapters.DEFAULT_CA_BUNDLE_PATH = REQUESTS_CA_BUNDLE_PATH

class MagickedAdministrator:
    
    def __init__(self):
        signal.signal(signal.SIGINT, self.terminate)
        self.servers = []

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
            server.level_threshold = \
                settings.setting(server_name, "level_threshold")

            has_motd_scoreboard = str_to_bool(
                settings.setting(server_name, "motd_scoreboard")
            )

            #if has_motd_scoreboard:
                #scoreboard_type = settings.setting(server_name, "scoreboard_type")
                #MotdUpdater(server, scoreboard_type).start()

            self.servers.append(server)

            Chatbot(server,
                    str_to_bool(settings.setting(server_name, "enable_greeter")),
                    settings.setting(server_name, "username")
                    )

        print("Initialisation complete!")

        while True:
            command = input()
            for server in self.servers:
                server.web_admin.chat.submit_message(command)
            
    def terminate(self, signal, frame):
        print("\nProgram interrupted, terminating...")

        if DEBUG:
            # noinspection PyProtectedMember
            os._exit(0)

        for server in self.servers:
            server.write_all_players(final=True)
            server.write_game_map()
            server.close()

        die()


if __name__ == "__main__":
    if DEBUG:
        debug_message = "Debug mode is enabled!"
        print(colored(debug_message, 'red'))

    application = MagickedAdministrator()
    application.run()
