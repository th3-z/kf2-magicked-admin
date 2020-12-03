import gettext
import time

from server.player import Player
from utils.text import millify
from utils.time import seconds_to_hhmmss

from .command import Command

_ = gettext.gettext


class CommandPlayerCount(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = _("Usage: !players\n"
                           "Desc: Shows the number of players currently "
                           "online")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        return self.format_response(
            _("{}/{} Players are online").format(
                len(self.server.players), self.server.capacity
            ),
            args
        )


class CommandPlayers(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = _("Usage: !players\n"
                           "Desc: Shows detailed information about online "
                           "players")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        players = self.server.players
        if not players:
            return self.format_response(_("No players in game"), args)

        message = ""
        for player in players:
            message += str(player) + " \n"

        return self.format_response(message.strip(), args)


class CommandGame(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = _("Usage: !game\n"
                           "Desc: Shows current game info and rules")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        return self.format_response(str(self.server.match), args)


class CommandGameMap(Command):
    def __init__(self, server, admin_only=False, requires_patch=False):
        Command.__init__(self, server, admin_only)

        self.help_text = _("Usage: !map\n"
                           "Desc: Shows statistics about the current map")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        return self.format_response(str(self.server.match.level), args)


class CommandGameTime(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = _("Usage: !game_time\n"
                           "Desc: Shows the number of seconds since the "
                           "match started. Excludes trader time and the boss"
                           " wave.")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        return self.format_response(str(self.server.match.time), args)


class CommandHighWave(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=True)

        self.help_text = _("Usage: !record_wave\n"
                           "Desc: Shows the highest wave reached on this map")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        return self.format_response(
            _("{} is the highest wave reached on this map").format(
                self.server.match.level.highest_wave
            ), args
        )


class CommandCommands(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = _("Usage: !commands\n"
                           "Desc: Lists all player commands")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        message = _("\nAvailable commands:\n"
                    "\t!record_wave,\n"
                    "\t!game,\n"
                    "\t!kills,\n"
                    "\t!dosh,\n"
                    "\t!top_kills,\n"
                    "\t!top_dosh,\n"
                    "\t!top_time,\n"
                    "\t!stats,\n"
                    "\t!game_time,\n"
                    "\t!server_kills,\n"
                    "\t!server_dosh,\n"
                    "\t!map,\n"
                    "\t!maps,\n"
                    "\t!player_count\n"
                    "Commands have help, e.g. '!stats -h'")

        return self.format_response(message, args)


class CommandStats(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = _("Usage: !stats USERNAME\n"
                           "\tUSERNAME - Person to get stats for\n"
                           "Desc: Shows statistics about a player, username "
                           "can be omitted to get personal stats")
        self.parser.add_argument("username", nargs="*")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if args.username:
            username = " ".join(args.username)

        player = self.server.get_player_by_username(username)
        if player:
            # TODO: Move this ...
            now = time.time()
            elapsed_time = now - player.session_start
        else:
            elapsed_time = 0
            player = Player(username, "no-perk")
            self.server.database.load_player(player)

        # ... And this
        fmt_time = seconds_to_hhmmss(
            player.total_time + elapsed_time
        )

        pos_kills = self.server.database.rank_kills(player.steam_id) or 0
        pos_dosh = self.server.database.rank_dosh(player.steam_id) or 0
        # todo Add pos_time to output
        # pos_time = self.server.database.rank_time(player.steam_id) or 0

        message = _("Stats for {}:\n"
                    "Total play time: {} ({} sessions)\n"
                    "Total deaths: {}\n"
                    "Total kills: {} (rank #{}) \n"
                    "Total dosh earned: £{} (rank #{})\n"
                    "Dosh this game: {}").format(
                        player.username, fmt_time, player.total_sessions,
                        player.total_deaths, millify(player.total_kills),
                        pos_kills, millify(player.total_dosh), pos_dosh,
                        millify(player.game_dosh))

        return self.format_response(message, args)
