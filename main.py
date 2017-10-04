from server import Server
from chat import ChatLogger

import configparser

config = configparser.ConfigParser()
config.read("./config")

def run():

    for server_name in config.sections():
        user = config[server_name]["admin_username"]
        password = config[server_name]["admin_password"]
        address = config[server_name]["webadmin_url"] 
        bot_user = config[server_name]["chatbot_username"]
        bot_password = config[server_name]["chatbot_password"]

        # Unused
        clan_motto = config[server_name]["clan_motto"]
        web_link = config[server_name]["web_link"]

        server = Server(server_name, address, user, password)
        chat_log = ChatLogger(server)
        chat_log.start()

        print(server)

    print("\nAll done.")



if __name__ == "__main__":
    run()

