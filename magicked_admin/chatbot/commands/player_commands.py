from chatbot.commands.command import Command
from utils.text import millify, trim_string
from utils.time import seconds_to_hhmmss
from utils.text import pad_output


class CommandServerDosh(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err

        self.server.write_all_players()
        dosh = self.server.database.server_dosh()
        return pad_output(
            millify(dosh) + " Dosh has been earned on this server"
        )


class CommandServerKills(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err

        self.server.write_all_players()
        kills = self.server.database.server_kills()
        return pad_output(
            millify(kills) + " ZEDs have been killed on this server"
        )


class CommandKills(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err

        player = self.server.get_player_by_username(username)
        if player:
            pos_kills = self.server.database.rank_kills(player.steam_id)
            return pad_output(
                "You've killed a total of {} ZEDs (#{}), and {} this game."
                "".format(
                    str(player.total_kills),
                    str(pos_kills),
                    str(player.kills)
                )
            )
        else:
            return pad_output("Player {} not in game.".format(username))


class CommandDosh(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err

        player = self.server.get_player_by_username(username)
        if player:
            pos_dosh = self.server.database.rank_dosh(player.steam_id)
            return pad_output(
                "You've earned a total of £{} dosh (#{}), and £{} this game."
                "".format(
                    str(player.total_dosh),
                    str(pos_dosh),
                    str(player.game_dosh)
                )
            )
        else:
            return pad_output("Player not in game.")


class CommandTopKills(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err

        self.server.write_all_players()
        records = self.server.database.top_kills()

        message = "Top 5 players by total kills:\n"

        for player in records[:5]:
            username = trim_string(player['username'], 20)
            kills = millify(player['kills'])
            message += "\t{}\t-   {}\n".format(
                kills, username
            )

        return pad_output(message[:-1])


class CommandTopDosh(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err

        self.server.write_all_players()
        records = self.server.database.top_dosh()

        message = "Top 5 players by Dosh earned:\n"

        for player in records[:5]:
            username = trim_string(player['username'], 20)
            dosh = millify(player['dosh'])
            message += "\t£{}\t-   {}\n".format(
                dosh, username
            )

        return pad_output(message[:-1])


class CommandTopTime(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err

        self.server.write_all_players()
        records = self.server.database.top_time()

        message = "Top 5 players by play time:\n"

        for player in records[:5]:
            username = trim_string(player['username'], 20)
            time = seconds_to_hhmmss(player['time_online'])
            message += "\t{}\t-   {}\n".format(
                time, username
            )

        return pad_output(message[:-1])


class CommandTopWaveKills(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=True)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err

        if not len(self.server.players):
            return None

        self.server.players.sort(
            key=lambda player: player.wave_kills,
            reverse=True
        )

        top = self.server.players[0]
        return pad_output(
            "Player {} killed the most ZEDs this wave: {}".format(
                top.username, millify(top.wave_kills)
            )
        )


class CommandTopWaveDosh(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=True)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err

        if not len(self.server.players):
            return None

        self.server.players.sort(
            key=lambda player: player.wave_dosh,
            reverse=True
        )

        top = self.server.players[0]
        return pad_output(
            "Player {} earned the most Dosh this wave: £{}".format(
                top.username, millify(top.wave_dosh)
            )
        )


