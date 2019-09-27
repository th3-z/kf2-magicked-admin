from chatbot.commands.command import Command
from utils.text import millify, trim_string
from utils.time import seconds_to_hhmmss


class CommandServerDosh(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = "Usage: !server_dosh\n" \
                         "Desc: Shows total dosh earned on this server"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        self.server.write_all_players()
        dosh = self.server.database.server_dosh()
        return self.format_response(
            "£{} has been earned on this server".format(millify(dosh)),
            args
        )


class CommandServerKills(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = "Usage: !server_kills\n" \
                         "Desc: Shows total ZEDs killed on this server"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        self.server.write_all_players()
        kills = self.server.database.server_kills()
        return self.format_response(
            "{} ZEDs have been killed on this server".format(millify(kills)),
            args
        )


class CommandKills(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = "Usage: !kills USERNAME\n" \
                         "\tUSERNAME - User to get kill stats for\n" \
                         "Desc: Shows kill statistics for a player, username" \
                         " can be omitted to get personal stats"
        self.parser.add_argument("username", nargs="*")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if args.username:
            username = " ".join(args.username)

        player = self.server.get_player_by_username(username)
        if player:
            pos_kills = self.server.database.rank_kills(player.steam_id)
            return self.format_response(
                "You've killed a total of {} ZEDs (#{}), and {} this game"
                "".format(
                    str(player.total_kills),
                    str(pos_kills),
                    str(player.kills)
                ),
                args
            )
        else:
            return self.format_response(
                "Player {} not in game".format(username), args
            )


class CommandDosh(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = "Usage: !dosh USERNAME\n" \
                         "\tUSERNAME - User to get dosh stats for\n" \
                         "Desc: Shows dosh statistics for a player, username" \
                         " can be omitted to get personal stats"
        self.parser.add_argument("username", nargs="*")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if args.username:
            username = " ".join(args.username)

        player = self.server.get_player_by_username(username)
        if player:
            pos_dosh = self.server.database.rank_dosh(player.steam_id)
            return self.format_response(
                "You've earned a total of £{} dosh (#{}), and £{} this game"
                "".format(
                    str(player.total_dosh),
                    str(pos_dosh),
                    str(player.game_dosh)
                ),
                args
            )
        else:
            return self.format_response("Player not in game", args)


class CommandTopKills(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = "Usage: !top_kills\n" \
                         "Desc: Show the global kills leaderboard"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        self.server.write_all_players()
        records = self.server.database.top_kills()

        message = "Top 5 players by total kills:\n"

        for player in records[:5]:
            username = trim_string(player['username'], 20)
            kills = millify(player['score'])
            message += "\t{}\t-   {}\n".format(
                kills, username
            )

        return self.format_response(message[:-1], args)


class CommandTopDosh(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = "Usage: !top_dosh\n" \
                         "Desc: Shows the global dosh leaderboard"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        self.server.write_all_players()
        records = self.server.database.top_dosh()

        message = "Top 5 players by Dosh earned:\n"

        for player in records[:5]:
            username = trim_string(player['username'], 20)
            dosh = millify(player['score'])
            message += "\t£{}\t-   {}\n".format(
                dosh, username
            )

        return self.format_response(message[:-1], args)


class CommandTopTime(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = "Usage: !top_time\n" \
                         "Desc: Shows the global play time leaderboard"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        self.server.write_all_players()
        records = self.server.database.top_time()

        message = "Top 5 players by play time:\n"

        for player in records[:5]:
            username = trim_string(player['username'], 20)
            time = seconds_to_hhmmss(player['score'])
            message += "\t{}\t-   {}\n".format(
                time, username
            )

        return self.format_response(message[:-1], args)


class CommandScoreboard(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = "Usage: !scoreboard\n" \
                         "Desc: Shows full player scoreboard"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        message = "Scoreboard (name, kills, dosh):\n"

        self.server.players.sort(
            key=lambda player: player.kills,
            reverse=True
        )

        for player in self.server.players:
            username = trim_string(player.username, 20)
            dosh = millify(player.dosh)
            kills = player.kills
            message += "{}\t- {}Kills £{}\n".format(
                username, kills, dosh
            )

        return self.format_response(message[:-1], args)


class CommandTopWaveKills(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=True)

        self.help_text = "Usage: !top_wave_kills\n" \
                         "Desc: Shows who killed the most ZEDs in this wave"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if not len(self.server.players):
            return self.format_response("No players in game", args)

        self.server.players.sort(
            key=lambda player: player.wave_kills,
            reverse=True
        )

        top = self.server.players[0]
        return self.format_response(
            "Player {} killed the most ZEDs this wave: {}".format(
                top.username, millify(top.wave_kills)
            ),
            args
        )


class CommandTopWaveDosh(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=True)

        self.help_text = "Usage: !top_wave_dosh\n" \
                         "Desc: Shows who earned the most dosh this wave"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if not len(self.server.players):
            return None

        self.server.players.sort(
            key=lambda player: player.wave_dosh,
            reverse=True
        )

        top = self.server.players[0]
        return self.format_response(
            "Player {} earned the most Dosh this wave: £{}".format(
                top.username, millify(top.wave_dosh)
            ),
            args
        )
