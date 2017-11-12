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
 
class CommandMe(Command):
    def __init__(self, server, adminOnly = True):
        Command.__init__(self, server, adminOnly)

    def execute(self, username, args, admin):
        player = self.server.get_player(username)
        if player:
            message = "This is what I've recorded...\n" + \
                    "username: " + str(player.username) + "\n" + \
                    "session_start: " + str(player.session_start) + "\n" + \
                    "t_logins: " + str(player.total_logins) + "\n" + \
                    "t_deaths: " + str(player.total_deaths) + "\n" + \
                    "t_kills: " + str(player.total_kills) + "\n" + \
                    "t_time: " + str(player.total_time) + "\n" + \
                    "t_dosh: " + str(player.total_dosh) + "\n" + \
                    "t_dosh_spent: " + str(player.total_dosh_spent) + "\n" + \
                    "t_health_lost: " + str(player.total_health_lost) + "\n" + \
                    "g_dosh: " + str(player.session_dosh) + "\n" + \
                    "g_dosh_spent: " + str(player.dosh_spent) + "\n" + \
                    "w_kills: " + str(player.wave_kills) + "\n" + \
                    "w_health_lost: " + str(player.health_lost_wave) + "\n" + \
                    "c_dosh: " + str(player.dosh) + "\n" + \
                    "c_kills: " + str(player.kills) + "\n" + \
                    "c_health: " + str(player.health) + "\n" + \
                    "c_perk: " + str(player.perk) + "\n" + \
                    "c_ping: " + str(player.ping) + "\n"
            return message
        else:
            return "Player " + username + " not found on server."
