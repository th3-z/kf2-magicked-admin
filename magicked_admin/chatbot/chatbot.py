from os import path

from chatbot import SCRIPT_TEMPLATE
from chatbot.commands.command_map import CommandMap
from chatbot.commands.event_commands import CommandGreeter
from utils import debug, find_data_file
from web_admin.chat import ChatListener


class Chatbot(ChatListener):

    def __init__(self, server, greeter_enabled=True, name=None):
        self.server_name = server.name
        if name:
            self.name = name
        else:
            self.name = "Unnamed"

        self.chat = server.web_admin.chat
        self.chat.add_listener(self)

        self.commands = CommandMap(server, self)
        self.silent = False
        self.greeter_enabled = True

        script_path = find_data_file(server.name + ".init")

        if path.exists(script_path):
            self.execute_script(script_path)
        else:
            with open(script_path,'w+') as script_file:
                script_file.write(SCRIPT_TEMPLATE)

    def receive_message(self, username, message, admin=False):
        if message[0] == '!':
            # Drop the '!' because its no longer relevant
            args = message[1:].split(' ')
            self.command_handler(username, args, admin)

    def command_handler(self, username, args, admin=False):
        if args is None or len(args) == 0:
            return

        if args[0].lower() in self.commands.command_map:
            command = self.commands.command_map[args[0].lower()]
            if not self.greeter_enabled and isinstance(command, CommandGreeter):
                return
            response = command.execute(username, args, admin)
            if not self.silent:
                self.chat.submit_message(response)

    def execute_script(self, file_name):
        debug("Executing script: " + path.basename(file_name))

        with open(file_name) as script:
            for line in script:
                buffered_output = ""
                command = line[:line.find(";")].strip()
                if command:
                    debug( "!" + command)
                    args = command.split()
                    self.command_handler("server", args, admin=True)
