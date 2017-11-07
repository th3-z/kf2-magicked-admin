from server import Server
from server_mapper import ServerMapper
from chat import ChatLogger
from chatbot import Chatbot
from watchdog import Watchdog

import configparser
import sys
import signal

config = configparser.ConfigParser()
config.read("./config")

class MagickedAdministrator():
    
    def __init__(self):
        self.servers = []
        self.bots = []
        self.watchdogs = []
        signal.signal(signal.SIGINT, self.terminate)

    def run(self):

        for server_name in config.sections():
            address = config[server_name]["address"] 
            user = config[server_name]["username"]
            password = config[server_name]["password"]
            game_password = config[server_name]["game_password"]
            motd_scoreboard = config[server_name]["motd_scoreboard"]
            map_autochange = config[server_name]["map_autochange"]

            server = Server(server_name, address, user, password, game_password, motd_scoreboard)

            if map_autochange == "True":
                wd = Watchdog(server)
                wd.start()
                self.watchdogs.append(wd)

            cb = Chatbot(server)
            server.chat.add_listener(cb)

            self.servers.append(server)
            self.bots.append(cb)

        print("Initialisation complete\n")

    def terminate(self, signal, frame):
        print("\nTerminating...")
        for server in self.servers:
            server.close()
        for bot in self.bots:
            bot.close()
        for wd in self.watchdogs:
            wd.terminate()

if __name__ == "__main__":
    application = MagickedAdministrator()
    application.run()

    sys.exit(0)

