import threading
import time

from chatbot.commands.command import Command
from utils import debug
from utils.text import millify
from utils.time import seconds_to_hhmmss
from web_admin.constants import *
from utils.text import pad_output

ALL_WAVES = 999


class CommandGreeter(Command):

    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err

        if len(args) < 2:
            return pad_output("Missing argument (username)")

        requested_username = " ".join(args[1:])

        player = self.server.get_player_by_username(requested_username)
        if not player:
            debug("Bad player join command (not found) [{}]"
                  .format(requested_username)
            )
            return None

        if player.sessions > 1:
            pos_kills = self.server.database.rank_kills(player.steam_id)
            pos_dosh = self.server.database.rank_dosh(player.steam_id)
            return pad_output(
                "\nWelcome back {}.\n"
                "You've killed {} zeds (rank #{}) and  \n"
                "earned £{} (rank #{}) \n"
                "over {} sessions ({}).".format(
                    player.username,
                    millify(player.total_kills),
                    pos_kills,
                    millify(player.total_dosh),
                    pos_dosh,
                    player.sessions,
                    seconds_to_hhmmss(player.total_time)
                )
            )
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
            self.chatbot.command_handler(
                "internal_command", self.args, USER_TYPE_INTERNAL
            )


class CommandOnTime(threading.Thread):
    def __init__(self, args, time_interval, chatbot, repeat=False):
        self.exit_flag = threading.Event()
        self.args = args
        self.chatbot = chatbot
        self.time_interval = float(time_interval)
        self.repeat = repeat

        threading.Thread.__init__(self)

    def terminate(self):
        self.exit_flag.set()

    def run(self):
        if not self.repeat:
            time.sleep(self.time_interval)
            self.chatbot.command_handler(
                "internal_command", self.args, USER_TYPE_INTERNAL
            )
            return
        while not self.exit_flag.wait(self.time_interval):
            self.chatbot.command_handler(
                "internal_command", self.args, USER_TYPE_INTERNAL
            )


class CommandOnTimeManager(Command):
    def __init__(self, server, chatbot):
        self.command_threads = []
        self.chatbot = chatbot
        Command.__init__(self, server, admin_only=True, requires_patch=False)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err

        if args[0] == "stop_tc":
            return self.terminate_all()

        repeat = False
        if args[1] in ["-r", "--repeat", "-R"]:
            repeat = True

        if len(args) < 2:
            return pad_output("Missing argument (command).")

        try:
            time = int(args[1]) if not repeat else int(args[2])
        except ValueError:
            return pad_output(
                "Malformed command, \"{}\" is not an integer.".format(args[1])
            )

        time_command = CommandOnTime(
            args[2:] if not repeat else args[3:], time, self.chatbot, repeat
        )
        time_command.start()
        self.command_threads.append(time_command)
        return pad_output("Timed command started.")

    def terminate_all(self):
        if len(self.command_threads) > 0:
            for command_thread in self.command_threads:
                command_thread.terminate()
                self.command_threads = []
            return pad_output("Timed command stopped")
        else:
            return pad_output("Nothing is running.")


class CommandOnWaveManager(Command):
    def __init__(self, server, chatbot):
        self.commands = []
        self.chatbot = chatbot
        Command.__init__(self, server, admin_only=True, requires_patch=True)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err

        if args[0] == "stop_wc":
            return self.terminate_all()
        elif args[0] == "start_wc":
            if len(args) < 2:
                return pad_output("Missing argument (command).")
            return self.start_command(args[1:])
        elif args[0] == "new_wave":
            for command in self.commands:
                command.new_wave(int(args[1]))

    def terminate_all(self):
        if len(self.commands) > 0:
            self.commands = []
            return pad_output("Wave commands halted.")
        else:
            return pad_output("Nothing is running.")

    def start_command(self, args):
        if len(args) < 2:
            return pad_output("Missing argument (command).")
            
        game_length = self.server.game.length
        
        try:
            wc = CommandOnWave(
                args[1:], int(args[0]), game_length, self.chatbot
            )
        except ValueError:
            wc = CommandOnWave(args, ALL_WAVES, game_length, self.chatbot)

        self.commands.append(wc)
        return pad_output("Wave command started.")


class CommandOnTraderManager(Command):
    def __init__(self, server, chatbot):
        self.commands = []
        self.chatbot = chatbot

        Command.__init__(self, server, admin_only=True, requires_patch=True)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err

        if args[0] == "start_trc":
            if len(args) < 2:
                return pad_output("Missing argument (command).")
            return self.start_command(args[1:])
        elif args[0] == "stop_trc":
            return self.terminate_all()
        elif args[0] == "t_open":
            for command in self.commands:
                self.chatbot.command_handler(
                    "internal_command", command, USER_TYPE_INTERNAL
                )

    def terminate_all(self):
        if len(self.commands) > 0:
            self.commands = []
            return pad_output("Trader commands stopped.")
        else:
            return pad_output("Nothing is running.")

    def start_command(self, args):
        self.commands.append(args)
        return pad_output("Trader command started.")
