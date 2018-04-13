from server.server import Server
from server.managers.motd_updater import MotdUpdater
from chatbot.chatbot import Chatbot
from utils.text import str_to_bool

import configparser
import logging
import sys
import signal
import os

logging.basicConfig(stream=sys.stdout)

logger = logging.getLogger(__name__)
if __debug__ and not hasattr(sys, 'frozen'):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

if not os.path.exists("./magicked_admin.conf"):
    logger.error("Configuration file not found")
    input("Press enter to exit...")
    sys.exit()

config = configparser.ConfigParser()
config.read("./magicked_admin.conf")


class MagickedAdministrator:
    
    def __init__(self):
        self.servers = []
        self.chatbots = []
        self.motd_updaters = []
        
        signal.signal(signal.SIGINT, self.terminate)

    def run(self):

        for server_name in config.sections():
            address = config[server_name]["address"] 
            user = config[server_name]["username"]
            password = config[server_name]["password"]
            game_password = config[server_name]["game_password"]
            motd_scoreboard = str_to_bool(
                config[server_name]["motd_scoreboard"]
            )
            scoreboard_type = config[server_name]["scoreboard_type"]
            enable_greeter = str_to_bool(
                config[server_name]["enable_greeter"]
            )
            
            server = Server(server_name, address, user, password,
                            game_password)
            self.servers.append(server)
                
            if motd_scoreboard:
                motd_updater = MotdUpdater(server, scoreboard_type)
                motd_updater.start()
                self.motd_updaters.append(motd_updater)

            cb = Chatbot(server, greeter_enabled=enable_greeter)
            server.chat.add_listener(cb)
            self.chatbots.append(cb)

        print("Initialisation complete")
            
    def terminate(self, signal, frame):
        print("Terminating, saving data...")
        for server in self.servers:
            server.write_all_players(final=True)

        sys.exit()


if __name__ == "__main__":
    application = MagickedAdministrator()
    application.run()

    sys.exit(0)

