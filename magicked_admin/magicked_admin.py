"""
Killing Floor 2 Magicked Admin
Copyright th3-z (the_z) 2018
Released under the terms of the MIT license
"""

import argparse
import gettext
import os
import signal
import sys
import locale

from colorama import init

# TODO: Improve package layouts
from chatbot.chatbot import Chatbot
from chatbot.command_scheduler import CommandScheduler
from chatbot.motd_updater import MotdUpdater
from chatbot.commands.command_map import CommandMap
from server.server import Server
from settings import Settings, CONFIG_PATH
from utils import banner, die, find_data_file, info, warning
from utils.net import phone_home
from server.game_tracker import GameTracker
from database.database import ServerDatabase
from server.game import Game, GameMap
from web_admin import WebAdmin
from web_admin.web_interface import WebInterface, AuthorizationException
from web_admin.chat import Chat
from web_admin.constants import *
from lua_bridge.lua_bridge import LuaBridge

gettext.bindtextdomain('magicked_admin', 'locale')
gettext.textdomain('magicked_admin')
gettext.install('magicked_admin', 'locale')

init()

parser = argparse.ArgumentParser(
    description=_('Killing Floor 2 Magicked Administrator')
)
parser.add_argument('-s', '--skip_setup', action='store_true',
                    help=_('Skips the guided setup process'))
args = parser.parse_args()

banner()

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
        phone_home()
        signal.signal(signal.SIGINT, self.terminate)
        self.stop_list = []
        self.sigint_count = 0
        self.settings = Settings(
            CONFIG_PATH,
            skip_setup=args.skip_setup
        )

    def reconfigure(self):
        self.settings = Settings(
            CONFIG_PATH,
            skip_setup=args.skip_setup,
            reconfigure=True
        )

    def make_server(self, name):
        address = self.settings.setting(name, "address")
        username = self.settings.setting(name, "username")
        password = self.settings.setting(name, "password")
        game_password = self.settings.setting(name, "game_password")
        url_extras = self.settings.setting(name, "url_extras")
        refresh_rate = float(self.settings.setting(name, "refresh_rate"))

        web_interface = WebInterface(address, username, password, name)
        chat = Chat(web_interface)
        chat.start()

        web_admin = WebAdmin(web_interface, chat)
        database = ServerDatabase(name)
        database.end_loose_sessions()
        game = Game(GameMap(), GAME_TYPE_UNKNOWN)

        server = Server(web_admin, database, game, name)

        if game_password:
            server.game_password = game_password
        if url_extras:
            server.url_extras = url_extras

        tracker = GameTracker(server, refresh_rate)
        tracker.start()

        self.stop_list.append(server)
        self.stop_list.append(chat)
        self.stop_list.append(tracker)

        return server

    def make_chatbot(self, name, server):
        chatbot = Chatbot(
            server.web_admin.chat,
            server_name=server.name, name=name
        )

        scheduler = CommandScheduler(server, chatbot)
        commands = CommandMap().get_commands(
            server, chatbot, scheduler, MotdUpdater(server)
        )

        for name, command in commands.items():
            chatbot.add_command(name, command)

        server.web_admin.chat.add_listener(chatbot)
        server.web_admin.chat.add_listener(scheduler)

        self.stop_list.append(scheduler)
        chatbot.run_init()

        return chatbot

    def run(self):
        servers = []

        language = self.settings.config['magicked_admin']['language']
        lang = gettext.translation(
            'magicked_admin', 'locale', [language]
        )
        lang.install()
        os.environ['LANGUAGE'] = language[:2]

        for server_name in self.settings.servers():
            # TODO: Gross

            try:
                server = self.make_server(server_name)
            except AuthorizationException:
                if len(self.settings.servers()) > 1:
                    warning(
                        _("Couldn't connect to server: {}").format(server_name)
                    )
                    continue
                else:
                    answer = input(
                        _("Authorization error connecting to '{}', reconfigure"
                          "? [Y/n]: ").format(
                            self.settings.setting(server_name, "address")
                        )
                    )
                    if answer.lower() in [_("yes"), _("y")]:
                        self.reconfigure()
                        self.run()
                    else:
                        die("Couldn't connect to server", pause=True)
                    return

            servers.append(server)
            chatbot = self.make_chatbot(
                self.settings.setting(server_name, "username"), server
            )
            lua_bridge = LuaBridge(server, chatbot)
            chatbot.add_lua_bridge(lua_bridge)
            server.web_admin.chat.add_listener(lua_bridge)

        info(_("Initialisation complete!\n"))

        if not args.skip_setup:
            while True:
                command = input()
                for server in servers:
                    server.web_admin.chat.submit_message(command)

    def terminate(self, signal, frame):
        if self.sigint_count > 1:
            print()  # \n
            warning(_("Closing immediately!"))
            os._exit(0)
            return

        self.sigint_count += 1
        if self.sigint_count > 1:
            return

        print()  # \n
        info(_("Program interrupted, saving data..."))

        for item in self.stop_list:
            item.stop()
        die()


if __name__ == "__main__":
    application = MagickedAdmin()
    application.run()
