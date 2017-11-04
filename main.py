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
            user = config[server_name]["username"]
            password = config[server_name]["password"]
            address = config[server_name]["address"] 

            # Unused
            # clan_motto = config[server_name]["clan_motto"]
            # web_link = config[server_name]["web_link"]

            server = Server(server_name, address, user, password)
            wd = Watchdog(server)
            wd.start()
            cb = Chatbot(server)
            server.chat.add_listener(cb)

            self.servers.append(server)
            self.bots.append(cb)
            self.watchdogs.append(wd)

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

