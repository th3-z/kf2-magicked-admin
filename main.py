from server import Server
from server_mapper import ServerMapper
from chat import ChatLogger
from chatbot import Chatbot

import configparser

config = configparser.ConfigParser()
config.read("./config")

def run():

    for server_name in config.sections():
        user = config[server_name]["username"]
        password = config[server_name]["password"]
        address = config[server_name]["address"] 

        # Unused
        clan_motto = config[server_name]["clan_motto"]
        web_link = config[server_name]["web_link"]

        server = Server(server_name, address, user, password)
        #chat_log = ChatLogger(server)

        cb = Chatbot(server)
        server.chat.add_listener(cb)
        #chat_log.start()

        sm = ServerMapper(server)
        sm.start()

        print(server)

    print("\nAll done.")



if __name__ == "__main__":
    run()

