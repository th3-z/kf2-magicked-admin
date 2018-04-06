from server.chat.listener import Listener
from chatbot.commands.command_map import CommandMap

import time
import threading
import server
from os import path
#from FuzzyWuzzy import Fuzz
#from FuzzyWuzzy import process

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

        if path.exists(server.name + ".init"):
            self.execute_script(server.name + ".init")

        print("INFO: Bot on server " + server.name + " initialised")

    def recieveMessage(self, username, message, admin=False):
        if message[0] == '!':
            # Drop the '!' because its no longer relevant
            args = message[1:].split(' ')
            self.command_handler(username, args, admin)

    def command_handler(self, username, args, admin=False):
        if args == None or len(args) == 0:
            return
        # Put FuzzyWuzzy Here?
        #choices = ['restart','toggle_pass','silent','length','difficulty','players','game','help','info','kills',
        #'dosh','top_kills','total_kills','top_dosh','me','stats']
        #match = process.extractOne(args, choices, scorer= fuzz.ratio, scorecutoff= 90)
        if args[0] in self.commands.command_map:
            command = self.commands.command_map[args[0]]
            response = command.execute(username, args, admin)
            if not self.silent:
                self.chat.submit_message(response)
        # Removing these lines for now until I figure out how to deal with CD shit. 
        #elif username != "server" and not self.silent:
            #self.chat.submit_message("Sorry, I didn't understand that request.")

    def execute_script(self, file_name):
        print("INFO: Executing script: " + file_name)
        with open(file_name) as script:
            for line in script:
                print("\t\t" + line.strip())
                args = line.split()
                self.command_handler("server", args, admin=True)
