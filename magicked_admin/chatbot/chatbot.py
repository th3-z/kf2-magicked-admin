from web_admin.chat import ChatListener
from chatbot.commands.command_map import CommandMap
from chatbot.commands.event_commands import CommandGreeter

from os import path

from utils import find_data_file, DEBUG


class Chatbot(ChatListener):
    """
    responsible for sending chat to the web_admin.
    """

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

        if path.exists(find_data_file(server.name + ".init")):
            self.execute_script(find_data_file(server.name + ".init"))

        if DEBUG:
            print("Bot on server " + server.name + " initialised")

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
        if DEBUG:
            print("Executing script: " + file_name)
        print("Executing script: " + file_name)
        with open(file_name) as script:
            for line in script:
                print("\t\t" + line.strip())
                args = line.split()
                self.command_handler("server", args, admin=True)
