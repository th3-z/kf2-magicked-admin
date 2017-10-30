from listener import Listener
import time
import threading

class TimedCommand(threading.Thread):

    def __init__(self, args, time_interval, chatbot):
        self.running = True
        self.args = args
        self.chatbot = chatbot
        self.time_interval = float(time_interval)

        threading.Thread.__init__(self)

    def terminate(self):
        self.running = False

    def run(self):
        while self.running:
            self.chatbot.command_handler("tc", self.args, admin=True)
            time.sleep(self.time_interval)

class Chatbot(Listener):
    
    def __init__(self, server):
        self.server = server
        self.chat = server.chat
        # The in-game chat can fit 21 Ws
        self.word_wrap = 21
        self.max_lines = 7

        self.timed_commands = []

        self.chat.submit_message("Beep beep, I'm back\ntype !help for usage")
        print("Bot on server " + server.name + " initialised")

    def recieveMessage(self, username, message, admin):
        
        if message[0] == '!':
            # Drop the '!' because its no longer relevant
            args = message[1:].split(' ')
            self.command_handler(username, args, admin)
            

    def command_handler(self, username, args, admin):
        if args[0] == "players":
            mesg = ""
            for player in self.server.players:
                mesg += str(player) + " \n"
            
            self.chat.submit_message(mesg)
        if args[0] == "game":
            self.chat.submit_message(str(self.server.game))
        if args[0] == "help":
            self.chat.submit_message("I haven't written the help text yet.")
        if args[0] == "start_tc" and admin:
            self.start_timed_command(args[2:], args[1])
        if args[0] == "stop_tc" and admin:
            for tc in self.timed_commands:
                tc.terminate()
                self.timed_commands = []
        
    def start_timed_command(self, args, time):
        timed_command = TimedCommand(args, time, self)
        self.timed_commands.append(timed_command)
        timed_command.start()
        
        
