from listener import Listener
import time
import threading
import server

ALL_WAVES = 99

class WaveCommand():
    
    def __init__(self, args, wave, length, chatbot):
        if wave > 0:
            self.wave = wave
        if wave < 0:
            # the boss wave is length+1, this should equate to -1
            self.wave = (length + 1) + (wave + 1)

        self.args = args
        self.chatbot = chatbot

    def new_wave(self, wave):
        if wave == self.wave or self.wave == ALL_WAVES:
            self.chatbot.command_handler("server", self.args, admin=True)
        

class TimedCommand(threading.Thread):

    def __init__(self, args, time_interval, chatbot):
        self.exit_flag = threading.Event()
        self.args = args
        self.chatbot = chatbot
        self.time_interval = float(time_interval)

        threading.Thread.__init__(self)

    def terminate(self):
        self.exit_flag.set()

    def run(self):
        while not self.exit_flag.wait(self.time_interval):
            self.chatbot.command_handler("server", self.args, admin=True)

class Chatbot(Listener):
    
    def __init__(self, server):
        self.server = server
        self.chat = server.chat
        # The in-game chat can fit 21 Ws
        self.word_wrap = 21
        self.max_lines = 7

        self.timed_commands = []
        self.wave_commands = []
        self.trader_commands = []

        self.gg_flag = False

        self.chat.submit_message("Beep beep, I'm back\ntype !help for usage")
        print("Bot on server " + server.name + " initialised")

    def recieveMessage(self, username, message, admin=False, player=None):
        if message == "gg" and not self.gg_flag:
            self.chat.submit_message("wp")
            self.gg_flag = True
        if message[0] == '!':
            # Drop the '!' because its no longer relevant
            args = message[1:].split(' ')
            self.command_handler(username, args, admin, player)

    def command_handler(self, username, args, admin=False, player=None):
        if args[0] == "players":
            mesg = ""
            for player in self.server.players:
                mesg += str(player) + " \n"
            self.chat.submit_message(mesg)

        elif args[0] == "game":
            self.chat.submit_message(str(self.server.game))

        elif args[0] == "help":
            self.chat.submit_message("You're going to play,\nand I'm gonna watch,\nand everything will be just fine.")

        elif args[0] == "say":
            mesg = " ".join(args[1:])
            # Unescape escape characters in say command
            mesg = bytes(mesg.encode("iso-8859-1","ignore")).decode('unicode_escape')
            self.chat.submit_message(mesg)

        elif args[0] == "start_tc" and admin:
            try:
                self.start_timed_command(args[2:], int(args[1]))
                self.chat.submit_message("Timer command started.")
            except ValueError:
                self.chat.submit_message("Malformed command, \""+args[1]+"\" is not an integer.")

        elif args[0] == "stop_tc" and admin:
            self.stop_timed_commands()
            self.chat.submit_message("Timer commands halted.")

        elif args[0] == "start_wc"  and admin:
            if len(args) < 2:
                self.chat.submit_message("Malformed command, missing second argument.") 
                return
            try:
                int(args[1])
                wc = WaveCommand(args[2:], int(args[1]), int(self.server.game['length']), self)
            except ValueError:
                wc = WaveCommand(args[1:], ALL_WAVES, int(self.server.game['length']), self)
            self.wave_commands.append(wc)
            self.chat.submit_message("Wave command started.")

        elif args[0] == "stop_wc" and admin:
            self.wave_commands = []
            self.chat.submit_message("Wave commands halted.")

        elif args[0] == "start_trc" and admin:
            if len(args) < 2:
                self.chat.submit_message("Malformed command, missing second argument.") 
                return
            self.trader_commands.append(args[1:])
            self.chat.submit_message("Trader command started.") 
            

        elif args[0] == "stop_trc" and admin:
            self.trader_commands = []
            self.chat.submit_message("Trader commands halted.") 

        elif args[0] == "difficulty":
            if args[1] == "normal":
                self.server.set_difficulty(server.DIFF_NORM)
            elif args[1] == "hard":
                self.server.set_difficulty(server.DIFF_HARD)
            elif args[1] == "suicidal":
                self.server.set_difficulty(server.DIFF_SUI)
            elif args[1] == "hell":
                self.server.set_difficulty(server.DIFF_HOE)
            else:
                self.chat.submit_message("Difficulty not recognised. Options are normal, hard, suicidal, or hell.")

        elif args[0] == "length":
            if args[1] == "short":
                self.server.set_length(server.LEN_SHORT)
            elif args[1] == "medium":
                self.server.set_length(server.LEN_NORM)
            elif args[1] == "long":
                self.server.set_length(server.LEN_LONG)
            else:
                self.chat.submit_message("Length not recognised. Options are short, medium, or long.")

        elif args[0] == "silent" and admin:
            if self.chat.silent:
                self.chat.silent = False 
                self.chat.submit_message("Silent mode toggled.")
            else:
                self.chat.submit_message("Silent mode toggled.")
                self.chat.silent = True

        elif args[0] == "kills" and player:
            self.chat.submit_message( "You've killed a total of " + str(player.total_kills) + " ZEDs, and " + str(player.kills) + " this game.")

        elif args[0] == "dosh" and player:
            self.chat.submit_message( ("You've earned £" + str(player.total_dosh) + " in total, and £" + str(player.session_dosh) + " this game.").encode("iso-8859-1","ignore"))

        elif args[0] == "new_wave" and admin:
            for wave_command in self.wave_commands:
                wave_command.new_wave(int(args[1]))

        elif args[0] == "new_game" and admin:
            self.gg_flag = False

        elif args[0] == "t_open" and admin:
            for trader_command in self.trader_commands:
                self.command_handler("server", trader_command, admin=True)

        elif username != "server":
            self.chat.submit_message("Sorry, I didn't understand that request.")
        else:   
            print("WARNING: Unhandled internal command " + str(args) + " Admin=" + str(admin))
            
        
    def start_timed_command(self, args, time):
        timed_command = TimedCommand(args, time, self)
        self.timed_commands.append(timed_command)
        timed_command.start()

    def stop_timed_commands(self):
        for tc in self.timed_commands:
            tc.terminate()
            tc.join()

            self.timed_commands = []

    def close(self):
        self.stop_timed_commands()
        
