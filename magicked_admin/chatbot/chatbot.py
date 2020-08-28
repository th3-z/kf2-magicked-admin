import gettext
from os import path

from chatbot import INIT_TEMPLATE
from utils import debug
from web_admin.chat import ChatListener
from web_admin.constants import *

_ = gettext.gettext


class Chatbot(ChatListener):
    def __init__(self, chat):
        self.chat = chat
        self._commands = {}
        self.lua_bridge = None
        self.silent = False
        self._aliases = {}

    def add_alias(self, name, command, admin_only=True):
        print(name)
        print(command)
        print(admin_only)
        self._aliases[name] = {
            "command": command,
            "admin_only": admin_only
        }

    def add_command(self, name, command):
        self._commands[name] = command

    def receive_message(self, username, message, user_flags):
        if message[0] == '!':
            # Drop the '!' because its no longer relevant
            args = message[1:].split(' ')
            self.command_handler(username, args, user_flags)

    def command_handler(self, username, args, user_flags):
        if args is None or len(args) == 0:
            return

        if args[0].lower() in self._commands:
            command = self._commands[args[0].lower()]
            response = command.execute(username, args, user_flags)
            if not self.silent and response:
                self.chat.submit_message(response)

        if args[0].lower() in self._aliases.keys():
            command = self._aliases[args[0].lower()]
            print(command)
            if not command['admin_only']:
                user_flags = user_flags | USER_TYPE_ADMIN
            self.command_handler(
                username, command['command'].split(" "), user_flags
            )

    def execute_script(self, filename):
        debug(_("Executing script: ") + path.basename(filename))

        fn, ext = path.splitext(filename)
        if ext == ".lua":
            self.lua_bridge.execute_script(filename)
            return

        with open(filename) as script:
            for line in script:
                comment_idx = line.find(";")
                if comment_idx != -1:
                    command = line[:comment_idx].strip()
                else:
                    command = line.strip()

                if command:
                    debug("!" + command)
                    args = command.split()
                    self.command_handler("internal_command", args,
                                         USER_TYPE_INTERNAL)

    def run_init(self, filename):
        if not path.exists(filename):
            with open(filename, 'w+') as script_file:
                script_file.write(INIT_TEMPLATE)

        self.execute_script(filename)
