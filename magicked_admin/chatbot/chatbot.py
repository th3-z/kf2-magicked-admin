from server.chat.listener import Listener
from chatbot.commands.command_map import CommandMap

import time
import threading
import server

from utils.text import trim_string, millify

class Chatbot(Listener):
    
    def __init__(self, server):
        self.server = server
        self.chat = server.chat
        # The in-game chat can fit 21 Ws horizontaly
        self.word_wrap = 21
        self.max_lines = 7
        
        self.commands = CommandMap(server, self)
        self.silent = False

        #self.chat.submit_message("Beep beep, I'm back\ntype !help for usage")
        print("INFO: Bot on server " + server.name + " initialised")

    def recieveMessage(self, username, message, admin=False):
        if message[0] == '!':
            # Drop the '!' because its no longer relevant
            args = message[1:].split(' ')
            self.command_handler(username, args, admin)

    def command_handler(self, username, args, admin=False):
        if args[0] in self.commands.command_map:
            command = self.commands.command_map[args[0]]
            response = command.execute(username, args, admin)
            if not self.silent:
                self.chat.submit_message(response)
        elif username != "server" and not self.silent:
            self.chat.submit_message("Sorry, I didn't understand that request.")
            
        
    def start_timed_command(self, args, time):
        # DEPRECATED
        timed_command = TimedCommand(args, time, self)
        self.timed_commands.append(timed_command)
        timed_command.start()

    def stop_timed_commands(self):
        # DEPRECATED
        for tc in self.timed_commands:
            tc.terminate()
            tc.join()

            self.timed_commands = []

    def terminate(self):
        # DEPRECATED
        self.stop_timed_commands()
        
