import gettext
from os import path

from chatbot import INIT_TEMPLATE
from web_admin.constants import *

from PySide2.QtCore import Slot

_ = gettext.gettext


class Chatbot():
    def __init__(self, server):
        self._web_admin = server.web_admin
        self._commands = {}
        self.lua_bridge = None
        self.silent = False
        self._aliases = {}

        self.signals = server.signals
        self.signals.command.connect(self.receive_command)

    def add_alias(self, name, command, admin_only=True):
        self._aliases[name] = {
            "command": command,
            "admin_only": admin_only
        }

    def add_command(self, name, command):
        self._commands[name] = command

    @Slot(str, list, int)
    def receive_command(self, username, args, user_flags):
        if args is None or len(args) == 0:
            return

        # FIXME: Aliases only work as first arg
        if args[0].lower() in self._aliases.keys():
            command = self._aliases[args[0].lower()]
            if not command['admin_only']:
                user_flags = user_flags | USER_TYPE_ADMIN
            args = command['command'].split(" ")

        if args[0].lower() in self._commands:
            command = self._commands[args[0].lower()]
            response = command.execute(username, args, user_flags)
            if not self.silent and response:
                self._web_admin.submit_message(response)

    def execute_script(self, filename):
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
                    args = command.split()
                    self.signals.command.emit("script_executor", args, USER_TYPE_ADMIN)

    def run_init(self, filename):
        if not path.exists(filename):
            with open(filename, 'w+') as script_file:
                script_file.write(INIT_TEMPLATE)

        self.execute_script(filename)
