from chatbot.commands.command import Command
from utils.text import millify
from utils.time import seconds_to_hhmmss
from utils.logger import logger

import threading
import datetime

ALL_WAVES = 999


class CommandGreeter(Command):
    """
    Player greeter (more here.)
    """
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

        self.new_game_grace = 35
        self.new_game_time = datetime.datetime.now()

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message

        if args[0] == "new_game":
            logger.debug("Greeter received new game event")
            self.new_game_time = datetime.datetime.now()
            return None
        now = datetime.datetime.now()
        elapsed_time = now - self.new_game_time
        seconds = elapsed_time.total_seconds()

        if seconds < self.new_game_grace:
            logger.debug("Skipping welcome {}, new_game happened recently ({})"
                         " [{}/{}]"
                         .format(username, self.server.name, seconds,
                                 self.new_game_grace))
            return None

        if len(args) < 2:
            return "Missing argument (username)"

        requested_username = " ".join(args[1:])

        player = self.server.get_player(requested_username)
        if not player:
            logger.debug("DEBUG: Bad player join command (not found) [{}]"
                         .format(requested_username))
            return "Couldn't greet player {}.".format(requested_username)

        if player.total_logins > 1:
            pos_kills = self.server.database.rank_kills(requested_username)
            pos_dosh = self.server.database.rank_dosh(requested_username)
            return "\nWelcome back {}.\n" \
                   "You've killed {} zeds (#{}) and  \n" \
                   "earned £{} (#{}) \nover {} sessions " \
                   "({}).".format(player.username,
                                  millify(player.total_kills),
                                  pos_kills,
                                  millify(player.total_dosh),
                                  pos_dosh,
                                  player.total_logins,
                                  seconds_to_hhmmss(player.total_time))\
                .encode("iso-8859-1", "ignore")
        else:
            return None


class CommandOnWave:
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


class CommandOnTime(threading.Thread):
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

class CommandOnTimeManager(Command):
    def __init__(self, server, chatbot, admin_only = True):
        self.command_threads = []
        self.chatbot = chatbot
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        if args[0] == "stop_tc":
            return self.terminate_all()
        if len(args) < 2:
            return "Missing argument (command)."
        try:
            time = int(args[1])
        except ValueError:
            return "Malformed command, \""+args[1]+"\" is not an integer."

        time_command = CommandOnTime(args[2:], time, self.chatbot)
        time_command.start()
        self.command_threads.append(time_command)
        return "Timed command started."

    def terminate_all(self):
        if len(self.command_threads) > 0:
            for command_thread in self.command_threads:
                command_thread.terminate()
                self.command_threads = []
            return "Timed command stopped"
        else:
            return "Nothing is running."


class CommandOnWaveManager(Command):
    def __init__(self, server, chatbot, admin_only = True):
        self.commands = []
        self.chatbot = chatbot
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message

        if args[0] == "stop_wc":
            return self.terminate_all()
        elif args[0] == "start_wc":
            if len(args) < 2:
                return "Missing argument (command)."
            return self.start_command(args[1:])
        elif args[0] == "new_wave":
            for command in self.commands:
                command.new_wave(int(args[1]))

    def terminate_all(self):
        if len(self.commands) > 0:
            self.commands = []
            return "Wave commands halted."
        else:
            return "Nothing is running."

    def start_command(self, args):
        if len(args) < 2:
            return "Missing argument (command)."

        game_length = int(self.server.game['length'])

        try:
            wc = CommandOnWave(args[1:], int(args[0]), game_length, self.chatbot)
        except ValueError:
            wc = CommandOnWave(args, ALL_WAVES, game_length, self.chatbot)

        self.commands.append(wc)
        return "Wave command started."


class CommandOnTraderManager(Command):
    def __init__(self, server, chatbot, admin_only = True):
        self.commands = []
        self.chatbot = chatbot

        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message

        if args[0] == "start_trc":
            if len(args) < 2:
                return "Missing argument (command)."
            return self.start_command(args[1:])
        elif args[0] == "stop_trc":
            return self.terminate_all()
        elif args[0] == "t_open":
            for command in self.commands:
                self.chatbot.command_handler("server", command, admin=True)

    def terminate_all(self):
        if len(self.commands) > 0:
            self.commands = []
            return "Trader commands stopped."
        else:
            return "Nothing is running."

    def start_command(self, args):
        self.commands.append(args)
        return "Trader command started."
