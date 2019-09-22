from os import path

from chatbot import INIT_TEMPLATE
from chatbot.command_map import CommandMap
from chatbot.command_scheduler import CommandScheduler
from utils import debug, find_data_file
from web_admin.chat import ChatListener
from web_admin.constants import *
from utils import warning


class Chatbot(ChatListener):

    def __init__(self, server, greeter_enabled=True, name=None):
        self.server_name = server.name
        if name:
            self.name = name
        else:
            self.name = "Unnamed"

        self.chat = server.web_admin.chat
        self.chat.add_listener(self)

        self.scheduler = CommandScheduler(server, self)
        self.chat.add_listener(self.scheduler)

        self.commands = CommandMap(server, self)
        self.silent = False
        self.greeter_enabled = True

        init_path = find_data_file(server.name + ".init")

        if path.exists(init_path):
            self.execute_script(init_path)
        else:
            with open(init_path, 'w+') as script_file:
                script_file.write(INIT_TEMPLATE)

    def receive_message(self, username, message, user_flags):
        if message[0] == '!':
            # Drop the '!' because its no longer relevant
            args = message[1:].split(' ')
            self.command_handler(username, args, user_flags)

    def command_handler(self, username, args, user_flags):
        if args is None or len(args) == 0:
            return

        if args[0].lower() in self.commands.command_map:
            command = self.commands.command_map[args[0].lower()]

            response = command.execute(username, args, user_flags)
            if not self.silent and response:
                self.chat.submit_message(response)

    def execute_script(self, filename):
        debug("Executing script: " + path.basename(filename))

        with open(filename) as script:
            for line in script:
                command = line[:line.find(";")].strip()
                if command:
                    debug("!" + command)
                    args = command.split()
                    self.command_handler("internal_command", args,
                                         USER_TYPE_INTERNAL)
