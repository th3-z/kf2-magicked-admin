import gettext

from chatbot.scroller import Scroller
from database.queries.leaderboards import top_by_col, top_by_playtime
from utils.text import center_str, millify, pad_width, str_width, trim_string
from utils.time import seconds_to_hhmmss

from .command import Command

_ = gettext.gettext


class CommandServerDosh(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = _("Usage: !server_dosh\n"
                           "Desc: Shows total dosh earned on this server")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        dosh = self.server.database.server_dosh()
        return self.format_response(
            _("£{} has been earned on this server").format(millify(dosh)),
            args
        )


class CommandServerKills(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = _("Usage: !server_kills\n"
                           "Desc: Shows total ZEDs killed on this server")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        kills = self.server.database.server_kills()
        return self.format_response(
            _("{} ZEDs have been killed on this server")
            .format(millify(kills)),
            args
        )


class CommandKills(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = _("Usage: !kills USERNAME\n"
                           "\tUSERNAME - User to get kill stats for\n"
                           "Desc: Shows kill statistics for a player, "
                           "username can be omitted to get personal stats")
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
        if not player:
            return self.format_response(
                _("Player {} not in game").format(username), args
            )

        pos_kills = self.server.database.rank_kills(player.steam_id)
        return self.format_response(
            _("You've killed a total of {} ZEDs (#{}), and {} this game")
            .format(
                str(player.total_kills),
                str(pos_kills),
                str(player.kills)
            ),
            args
        )


class CommandDosh(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = _("Usage: !dosh USERNAME\n"
                           "\tUSERNAME - User to get dosh stats for\n"
                           "Desc: Shows dosh statistics for a player, "
                           "username can be omitted to get personal stats")
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
        if not player:
            return self.format_response(_("Player not in game"), args)

        pos_dosh = self.server.database.rank_dosh(player.steam_id)
        return self.format_response(
            _("You've earned a total of £{} dosh (#{}), and £{} this"
              " game")
            .format(
                str(player.total_dosh),
                str(pos_dosh),
                str(player.game_dosh)
            ),
            args
        )


class CommandTopKills(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = _("Usage: !top_kills\n"
                           "Desc: Show the global kills leaderboard")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        header = center_str("~ Kills Leaderboard (weekly) ~")
        header += "\nRank | Kills  | Username"

        records = top_by_col('kills', self.server.server_id, limit=25, period=604800)
        rows = []

        for i, player in enumerate(records):
            username = trim_string(player['username'], 20)
            kills = millify(player['score'])
            kills = pad_width(str_width("Kills "), kills)

            rows.append("#{:02d}    | {} | {}".format(
                i + 1, kills, username
            ))

        rows.reverse()

        scroller = Scroller(self.server.web_admin, "\n".join(rows), header)
        scroller.start()

        return None


class CommandTopDosh(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = _("Usage: !top_dosh\n"
                           "Desc: Shows the global dosh leaderboard")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        header = center_str("~ Dosh Leaderboard ~")
        header += "\nRank | Dosh  | Username"

        records = top_by_col('dosh', self.server.server_id, limit=25)
        rows = []

        for i, player in enumerate(records):
            username = trim_string(player['username'], 20)
            dosh = millify(player['score'])
            dosh = pad_width(str_width("Dosh "), dosh)

            rows.append("#{:02d}    | {} | {}".format(
                i + 1, dosh, username
            ))

        rows.reverse()

        scroller = Scroller(self.server.web_admin, "\n".join(rows), header)
        scroller.start()

        return None


class CommandTopTime(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = _("Usage: !top_time\n"
                           "Desc: Shows the global play time leaderboard")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        header = center_str("~ Playtime leaderboard (weekly) ~")
        header += "\nRank | Time       | Username"

        records = top_by_playtime(self.server.server_id, limit=25)
        rows = []

        for i, player in enumerate(records):
            username = trim_string(player['username'], 20)
            time = seconds_to_hhmmss(player['playtime'])
            time = pad_width(str_width("Time      "), time)

            rows.append("#{:02d}    | {} | {}".format(
                i + 1, time, username
            ))

        rows.reverse()

        scroller = Scroller(self.server.web_admin, "\n".join(rows), header)
        scroller.start()

        return None


class CommandScoreboard(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = _("Usage: !scoreboard\n"
                           "Desc: Shows full player scoreboard")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        # TODO: Unused var? message = _("Scoreboard (name, kills, dosh):\n")

        header = center_str("Scoreboard")
        header += "\nKills | Dosh | Username"

        self.server.players.sort(
            key=lambda player: player.kills,
            reverse=True
        )

        rows = []

        for player in self.server.players:
            username = trim_string(player.username, 20)
            dosh = pad_width(str_width("Dosh"), "£" + millify(player.dosh))
            kills = pad_width(str_width("Kills"), millify(player.kills))
            rows.append(_("{} | {} | {}").format(
                kills, dosh, username
            ))

        scroller = Scroller(self.server.web_admin, "\n".join(rows), header)
        scroller.start()

        return None


class CommandTopWaveKills(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=True)

        self.help_text = _("Usage: !top_wave_kills\n"
                           "Desc: Shows who killed the most ZEDs in this "
                           "wave")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if not self.server.players:
            return self.format_response(_("No players in game"), args)

        self.server.players.sort(
            key=lambda player: player.wave_kills,
            reverse=True
        )

        top = self.server.players[0]
        return self.format_response(
            _("Player {} killed the most ZEDs this wave: {}").format(
                top.username, millify(top.wave_kills)
            ),
            args
        )


class CommandTopWaveDosh(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=True)

        self.help_text = _("Usage: !top_wave_dosh\n"
                           "Desc: Shows who earned the most dosh this wave")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if not self.server.players:
            return None

        self.server.players.sort(
            key=lambda player: player.wave_dosh,
            reverse=True
        )

        top = self.server.players[0]
        return self.format_response(
            _("Player {} earned the most Dosh this wave: £{}").format(
                top.username, millify(top.wave_dosh)
            ),
            args
        )
