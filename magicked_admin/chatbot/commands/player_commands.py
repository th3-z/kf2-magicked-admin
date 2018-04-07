# Should I change this to always return message vs. returning text?

from chatbot.commands.command import Command
from utils.text import trim_string, millify

class CommandServerdosh(Command):
    def __init__(self, server, adminOnly = True):
        Command.__init__(self, server, adminOnly)
Yo
    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message

        self.server.write_all_players()
        return str(self.server.database.server_dosh()) + \
                " dosh has been earned on this server"
                #" dosh has been earned on this server"
                # Code below is for adding dosh spent but not dealing with it right now.
                #" and " + () +\
                #" has been spent on this server."

class CommandServerKills(Command):
    def __init__(self, server, adminOnly = True):
        Command.__init__(self, server, adminOnly)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message

        #self.server.write_all_players()
        kills = self.server.database.server_kills()
        return str(kills) + \
                " ZEDs have been killed on this server"

class CommandKills(Command):
    def __init__(self, server, adminOnly = True):
        Command.__init__(self, server, adminOnly)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message

        player = self.server.get_player(username)
        if player:
            return "You've killed a total of " + str(player.total_kills) + \
                    " ZEDs, and " + str(player.kills) + " this game."
        else:
            return "Player not in game."

class CommandDosh(Command):
    def __init__(self, server, adminOnly = True):
        Command.__init__(self, server, adminOnly)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message

        player = self.server.get_player(username)
        if player:
            return  ("You've earned £" + str(player.total_dosh) + \
                    " in total, and £" + str(player.game_dosh) + \
                    " this game.").encode("iso-8859-1","ignore")
        else:
            return "Player not in game."

class CommandTopKills(Command):
    def __init__(self, server, adminOnly = True):
        Command.__init__(self, server, adminOnly)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message

        self.server.write_all_players()
        killers = self.server.database.top_kills()
        if len(killers) < 5:
            return "Not enough data."
        # [row][col]
        return "\n\nTop 5 players by kills:\n"+ \
            "\t"+str(millify(killers[0][1])) + "\t-\t" + trim_string(killers[0][0],20) + "\n" + \
            "\t"+str(millify(killers[1][1])) + "\t-\t" + trim_string(killers[1][0],20) + "\n" + \
            "\t"+str(millify(killers[2][1])) + "\t-\t" + trim_string(killers[2][0],20) + "\n" + \
            "\t"+str(millify(killers[3][1])) + "\t-\t" + trim_string(killers[3][0],20) + "\n" + \
            "\t"+str(millify(killers[4][1])) + "\t-\t" + trim_string(killers[4][0],20)

class CommandTopDosh(Command):
    def __init__(self, server, adminOnly = True):
        Command.__init__(self, server, adminOnly)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message

        self.server.write_all_players()
        doshers = self.server.database.top_dosh()
        if len(doshers) < 5:
            return "Not enough data."

        message = "\n\nTop 5 players by earnings:\n"+ \
            "\t£"+str(millify(doshers[0][1])) + "\t-\t" + trim_string(doshers[0][0],20) + "\n" + \
            "\t£"+str(millify(doshers[1][1])) + "\t-\t" + trim_string(doshers[1][0],20) + "\n" + \
            "\t£"+str(millify(doshers[2][1])) + "\t-\t" + trim_string(doshers[2][0],20) + "\n" + \
            "\t£"+str(millify(doshers[3][1])) + "\t-\t" + trim_string(doshers[3][0],20) + "\n" + \
            "\t£"+str(millify(doshers[4][1])) + "\t-\t" + trim_string(doshers[4][0],20)
        return message.encode("iso-8859-1","ignore")
