import time

from chatbot.commands.command import Command
from server.player import Player
from utils.text import millify
from utils.time import seconds_to_hhmmss


lps_test_frames = [
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "-",
    "T",
    "H",
    "E",
    "-",
    "Q",
    "U",
    "I",
    "C",
    "K",
    "-",
    "B",
    "R",
    "O",
    "W",
    "N",
    "-",
    "F",
    "O",
    "X",
    "-",
    "J",
    "U",
    "M",
    "P",
    "S",
    "-",
    "O",
    "V",
    "E",
    "R",
    "-",
    "T",
    "H",
    "E",
    "-",
    "L",
    "A",
    "Z",
    "Y",
    "-",
    "D",
    "O",
    "G",
    "."
]

fps = 18
scroll_height = 7


class CommandLpsTest(Command):
    def __init__(self, server, chatbot, admin_only=True):
        self.chatbot = chatbot
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message

        for i in range(0, 300):
            line_start = i % len(lps_test_frames)
            line_end = (i + scroll_height) % len(lps_test_frames)

            message = "\n"
            if line_start > line_end:
                message += "\n".join(lps_test_frames[:line_end])
                message += "\n"
                message += "\n".join(lps_test_frames[line_start:])
            else:
                message += "\n".join(lps_test_frames[line_start:line_end])

            self.chatbot.chat.submit_message(message)

            time.sleep(1/fps)


class CommandPlayerCount(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message

        return "{}/{} Players are online".format(
            len(self.server.players), self.server.game.players_max
        )


class CommandPlayers(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message
        message = ""

        for player in self.server.players:
            message += str(player) + " \n"
        message = message.strip()
        return message


class CommandGame(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message
        return str(self.server.game)

class CommandGameMap(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message
        return str(self.server.game.game_map)


class CommandGameTime(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message
        return str(self.server.game.time)


class CommandHighWave(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message
        return "{} is the highest wave reached on this map."\
            .format(self.server.game.game_map.highest_wave)


class CommandHelp(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message
        return "Player commands:\n !me, !dosh, !kills, !server_dosh," \
               " !server_kills, !top_dosh, !top_kills, !stats"


class CommandStats(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message

        self.server.write_all_players()

        if len(args) > 1:
            requested_username = " ".join(args[1:])
        else:
            requested_username = username

        player = self.server.get_player_by_username(requested_username)
        if player:
            now = time.time()
            elapsed_time = now - player.session_start
        else:
            elapsed_time = 0
            player = Player(requested_username, "no-perk")
            self.server.database.load_player(player)

        fmt_time = seconds_to_hhmmss(
            player.total_time + elapsed_time
        )
        message = "Stats for {}:\n".format(player.username) +\
                  "Total play time: {} ({} sessions)\n"\
                      .format(fmt_time, player.sessions) +\
                  "Total deaths: {}\n".format(player.total_deaths) +\
                  "Total kills: {}\n".format(millify(player.total_kills)) +\
                  "Total dosh earned: {}\n"\
                      .format(millify(player.total_dosh)) +\
                  "Dosh this game: {}".format(millify(player.game_dosh))

        return message
