from server.server import Server
from server.managers.watchdog import Watchdog
from server.managers.motd_updater import MotdUpdater
from chatbot.chatbot import Chatbot
from utils.text import str_to_bool

import configparser
import sys
import signal
import os

DEBUG = True

if not os.path.exists("./magicked_admin.conf"):
    sys.exit("Configuration file not found.")
config = configparser.ConfigParser()
config.read("./magicked_admin.conf")

class MagickedAdministrator():
    
    def __init__(self):
        self.servers = []
        self.chatbots = []
        self.watchdogs = []
        self.motd_updaters = []
        
        signal.signal(signal.SIGINT, self.terminate)

    def run(self):

        for server_name in config.sections():
            address = config[server_name]["address"] 
            user = config[server_name]["username"]
            password = config[server_name]["password"]
            game_password = config[server_name]["game_password"]
            motd_scoreboard = str_to_bool(config[server_name]["motd_scoreboard"])
            scoreboard_type = config[server_name]["scoreboard_type"]
            map_autochange = str_to_bool(config[server_name]["map_autochange"])
            multiadmin_enabled = str_to_bool(config[server_name]["multiadmin_enabled"])
            
            server = Server(server_name, address, user, password,
                            game_password)
            self.servers.append(server)
			
            if map_autochange:
                wd = Watchdog(server)
                wd.start()
                self.watchdogs.append(wd)
                
            if motd_scoreboard:
                motd_updater = MotdUpdater(server, scoreboard_type)
                motd_updater.start()
                self.motd_updaters.append(motd_updater)

            cb = Chatbot(server)
            server.chat.add_listener(cb)
            self.chatbots.append(cb)
			
        print("INFO: Initialisation complete\n")
            
    def terminate(self, signal, frame):
        print("\nINFO: Terminating...")
        for server in self.servers:
            server.terminate()
        #for cb in self.chatbots:
        #    cb.terminate()
        for wd in self.watchdogs:
            wd.terminate()
        for motd_updater in self.motd_updaters:
            motd_updater.terminate()

if __name__ == "__main__":
    application = MagickedAdministrator()
    application.run()

    sys.exit(0)

