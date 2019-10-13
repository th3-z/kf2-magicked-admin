import gettext
from os import path

from chatbot import INIT_TEMPLATE
from utils import debug, find_data_file
from web_admin.chat import ChatListener
from web_admin.constants import *

_ = gettext.gettext


class Chatbot(ChatListener):
    def __init__(self, server, name):
        self.server_name = server.name
        self.name = name or "Unnamed"

        self.chat = server.web_admin.chat
        self.commands = {}
        self.silent = False

        init_path = find_data_file("conf/scripts/" + server.name + ".init")

        if path.exists(init_path):
            self.execute_script(init_path)
        else:
            with open(init_path, 'w+') as script_file:
                script_file.write(INIT_TEMPLATE)

    def add_command(self, name, command):
        self.commands[name] = command

    def receive_message(self, username, message, user_flags):
        if message[0] == '!':
            # Drop the '!' because its no longer relevant
            args = message[1:].split(' ')
            self.command_handler(username, args, user_flags)

    def command_handler(self, username, args, user_flags):
        if args is None or len(args) == 0:
            return

        if args[0].lower() in self.commands:
            command = self.commands[args[0].lower()]

            response = command.execute(username, args, user_flags)
            if not self.silent and response:
                self.chat.submit_message(response)

    def execute_script(self, filename):
        debug(_("Executing script: ") + path.basename(filename))

        with open(filename) as script:
            for line in script:
                command = line[:line.find(";")].strip()
                if command:
                    debug("!" + command)
                    args = command.split()
                    self.command_handler("internal_command", args,
                                         USER_TYPE_INTERNAL)
