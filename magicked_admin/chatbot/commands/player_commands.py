from chatbot.commands.command import Command
from utils.text import millify, trim_string
from utils.time import seconds_to_hhmmss


class CommandServerDosh(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message

        self.server.write_all_players()
        dosh = self.server.database.server_dosh()
        return millify(dosh) + " Dosh has been earned on this server"


class CommandServerKills(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message

        self.server.write_all_players()
        kills = self.server.database.server_kills()
        return millify(kills) + " ZEDs have been killed on this server"


class CommandKills(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message

        player = self.server.get_player_by_username(username)
        if player:
            pos_kills = self.server.database.rank_kills(player.steam_id)
            return ("You've killed a total of {} ZEDs (#{}), "
                    "and {} this game.").format(
                str(player.total_kills),
                str(pos_kills),
                str(player.kills)
            )
        else:
            return "Player {} not in game.".format(username)


class CommandDosh(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message

        player = self.server.get_player_by_username(username)
        if player:
            pos_dosh = self.server.database.rank_dosh(player.steam_id)
            return ("You've earned a total of £{} dosh (#{}), "
                    "and £{} this game.").format(
                str(player.total_dosh),
                str(pos_dosh),
                str(player.game_dosh)
            ).encode("iso-8859-1", "ignore")
        else:
            return "Player not in game."


class CommandTopKills(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message

        if len(args) > 1 and args[1] == '-w' and len(self.server.players) > 0:
            self.server.players.sort(key=lambda player: player.wave_kills, reverse=True)
            top_killer = self.server.players[0]
            return "Player {} killed the most zeds this wave: {} zeds"\
                .format(top_killer.username, top_killer.wave_kills)

        self.server.write_all_players()
        records = self.server.database.top_kills()

        message = "\n\nTop 5 players by total kills:\n"

        for player in records[:5]:
            username = trim_string(player['username'], 20)
            kills = millify(player['kills'])
            message += "\t{}\t-   {}\n".format(
                kills, username
            )

        return message


class CommandTopDosh(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message

        if len(args) > 1 and args[1] == '-w' and len(self.server.players) > 0:
            self.server.players.sort(key=lambda player: player.wave_dosh, reverse=True)
            top_dosh = self.server.players[0]
            return "Player {} earned the most this wave: £{}"\
                .format(top_dosh.username, millify(top_dosh.wave_dosh))\
                .encode("iso-8859-1", "ignore")

        self.server.write_all_players()
        records = self.server.database.top_dosh()

        message = "\n\nTop 5 players by Dosh earned:\n"

        for player in records[:5]:
            username = trim_string(player['username'], 20)
            dosh = millify(player['dosh'])
            message += "\t£{}\t-   {}\n".format(
                dosh, username
            )

        return message


class CommandTopTime(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message

        self.server.write_all_players()
        records = self.server.database.top_time()

        message = "\n\nTop 5 players by play time:\n"

        for player in records[:5]:
            username = trim_string(player['username'], 20)
            time = seconds_to_hhmmss(player['time_online'])
            message += "\t{}\t-   {}\n".format(
                time, username
            )

        return message
