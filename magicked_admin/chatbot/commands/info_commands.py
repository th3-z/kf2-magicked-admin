from chatbot.commands.command import Command

class CommandPlayers(Command):  
    def __init__(self, server, adminOnly = True):
        Command.__init__(self, server, adminOnly)
        
    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        message = ""

        for player in self.server.players:
            message += str(player) + " \n"
        
        return message

class CommandGame(Command):
    def __init__(self, server, adminOnly = True):
        Command.__init__(self, server, adminOnly)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        return str(self.server.game)

class CommandHelp(Command):
    def __init__(self, server, adminOnly = True):
        Command.__init__(self, server, adminOnly)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        return "Player commands:\n !dosh, !kills, !top_dosh,\
                \n!top_kills, !difficulty, !length"