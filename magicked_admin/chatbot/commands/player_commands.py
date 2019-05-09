from chatbot.commands.command import Command
from utils.text import millify, trim_string


class CommandServerDosh(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(username, admin):
            return self.not_auth_message

        self.server.write_all_players()
        dosh = self.server.database.server_dosh()
        return millify(dosh) + " Dosh has been earned on this server"


class CommandServerKills(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(username, admin):
            return self.not_auth_message

        self.server.write_all_players()
        kills = self.server.database.server_kills()
        return millify(kills) + " ZEDs have been killed on this server"


class CommandKills(Command):
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(username, admin):
            return self.not_auth_message

        player = self.server.get_player_by_username(username)
        if player:
            pos_kills = self.server.database.rank_kills(username)
            return ("You've killed a total of {} ZEDs (#{}), "
                    "and {} this game.").format(
                str(player.total_kills),
                str(pos_kills),
                str(player.kills)
            )
        else:
            return "Player not in game."


class CommandDosh(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(username, admin):
            return self.not_auth_message

        player = self.server.get_player_by_username(username)
        if player:
            pos_dosh = self.server.database.rank_dosh(username)
            return ("You've earned a total of £{} dosh (#{}), "
                    "and {} this game.").format(
                str(player.total_dosh),
                str(pos_dosh),
                str(player.game_dosh)
            ).encode("iso-8859-1", "ignore")
        else:
            return "Player not in game."


class CommandTopKills(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(username, admin):
            return self.not_auth_message

        if len(args) > 1 and args[1] == '-w' and len(self.server.players) > 0:
            self.server.players.sort(key=lambda player: player.wave_kills, reverse=True)
            top_killer = self.server.players[0]
            return "Player {} killed the most zeds this wave: {} zeds"\
                .format(top_killer.username, top_killer.wave_kills)

        self.server.write_all_players()
        killers = self.server.database.top_kills()
        if len(killers) < 5:
            return "Not enough data."
        # [row][col]
        return "\n\nTop 5 players by total kills:\n" + \
            "\t"+str(millify(killers[0][1])) + "\t-\t" + trim_string(killers[0][0],20) + "\n" + \
            "\t"+str(millify(killers[1][1])) + "\t-\t" + trim_string(killers[1][0],20) + "\n" + \
            "\t"+str(millify(killers[2][1])) + "\t-\t" + trim_string(killers[2][0],20) + "\n" + \
            "\t"+str(millify(killers[3][1])) + "\t-\t" + trim_string(killers[3][0],20) + "\n" + \
            "\t"+str(millify(killers[4][1])) + "\t-\t" + trim_string(killers[4][0],20)


class CommandTopDosh(Command):
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(username, admin):
            return self.not_auth_message

        if len(args) > 1 and args[1] == '-w' and len(self.server.players) > 0:
            self.server.players.sort(key=lambda player: player.wave_dosh, reverse=True)
            top_dosh = self.server.players[0]
            return "Player {} earned the most this wave: £{}"\
                .format(top_dosh.username, millify(top_dosh.wave_dosh))\
                .encode("iso-8859-1", "ignore")

        self.server.write_all_players()
        doshers = self.server.database.top_dosh()
        if len(doshers) < 5:
            return "Not enough data."

        message = "\n\nTop 5 players by earnings:\n" + \
            "\t£"+str(millify(doshers[0][1])) + "\t-\t" + trim_string(doshers[0][0],20) + "\n" + \
            "\t£"+str(millify(doshers[1][1])) + "\t-\t" + trim_string(doshers[1][0],20) + "\n" + \
            "\t£"+str(millify(doshers[2][1])) + "\t-\t" + trim_string(doshers[2][0],20) + "\n" + \
            "\t£"+str(millify(doshers[3][1])) + "\t-\t" + trim_string(doshers[3][0],20) + "\n" + \
            "\t£"+str(millify(doshers[4][1])) + "\t-\t" + trim_string(doshers[4][0],20)
        return message.encode("iso-8859-1","ignore")
