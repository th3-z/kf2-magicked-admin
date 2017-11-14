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
                !top_kills, !difficulty, !length,\
                !stats, !me"
 
class CommandMe(Command):
    def __init__(self, server, adminOnly = True):
        Command.__init__(self, server, adminOnly)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        self.server.write_all_players()
        player = self.server.get_player(username)
        if player:
            message = ("This is what I've recorded...\n" + \
                    "username: " + str(player.username) + "\n" + \
                    "session_start: " + str(player.session_start) + "\n" + \
                    "t_logins: " + str(player.total_logins) + "\n" + \
                    "t_deaths: " + str(player.total_deaths) + "\n" + \
                    "t_kills: " + str(player.total_kills) + "\n" + \
                    "t_time: {0:.2f}hrs\n" + \
                    "t_dosh: " + str(player.total_dosh) + "\n" + \
                    "t_dosh_spent: " + str(player.total_dosh_spent) + "\n" + \
                    "t_health_lost: " + str(player.total_health_lost) + "\n" + \
                    "g_dosh: " + str(player.game_dosh) + "\n" + \
                    "w_kills: " + str(player.wave_kills) + "\n" + \
                    "w_dosh: " + str(player.wave_dosh) + "\n" + \
                    "c_dosh: " + str(player.dosh) + "\n" + \
                    "c_kills: " + str(player.kills) + "\n" + \
                    "c_health: " + str(player.health) + "\n" + \
                    "c_perk: " + str(player.perk) + "\n" + \
                    "c_ping: " + str(player.ping) + "\n" \
                    ).format(player.total_time/60/60)
            return message
        else:
            return "Player " + username + " not found on server."

class CommandStats(Command):
    def __init__(self, server, adminOnly = True):
        Command.__init__(self, server, adminOnly)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        
        self.server.write_all_players()
        if len(args) < 2:
            return "Missing argument (username)"
        player = self.server.get_player(args[1])
        if player:
            message = ("Stats for " + player.username + "...\n" + \
                    "Sessions:\t\t\t" + str(player.total_logins) + "\n" + \
                    "Deaths:\t\t\t" + str(player.total_deaths) + "\n" + \
                    "Kills:\t\t\t\t" + str(player.total_kills) + "\n" + \
                    "Play time:\t\t{0:.2f}hrs\n" + \
                    "Dosh earned:\t\t" + str(player.total_dosh) + "\n" + \
                    "Dosh spent:\t\t" + str(player.total_dosh_spent) + "\n" + \
                    "Health lost:\t\t" + str(player.total_health_lost) + "\n" + \
                    "Dosh this game:\t" + str(player.game_dosh) + "\n" + \
                    "Kills this wave:\t\t" + str(player.wave_kills) + "\n" + \
                    "Dosh this wave:\t" + str(player.wave_dosh) \
                    ).format(player.total_time/60/60)
            return message
        else:
            return "Player " + args[1] + " not found on server."