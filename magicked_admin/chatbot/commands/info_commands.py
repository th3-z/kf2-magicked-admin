from chatbot.commands.command import Command
from server.player import Player
from utils.time import seconds_to_hhmmss

import datetime

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
        return "Player commands:\n !dosh, !kills, !top_dosh, " + \
                "!top_kills, !stats, !me, !info"
 
class CommandInfo(Command):
    def __init__(self, server, adminOnly = True):
        Command.__init__(self, server, adminOnly)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        return "I'm a bot for ranked Killing Floor 2 servers. Visit:\n" + \
            "github.com/th3-z/kf-magicked-admin/\n" + \
            "for information, source code, and credits."
 
class CommandMe(Command):
    def __init__(self, server, adminOnly = True):
        Command.__init__(self, server, adminOnly)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
            
        stats_command = CommandStats(self.server, adminOnly=False)
        return stats_command.execute("server", ["stats", username], admin=True)

class CommandStats(Command):
    def __init__(self, server, adminOnly = True):
        Command.__init__(self, server, adminOnly)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        if len(args) < 2:
            return "Missing argument (username)"
            
        self.server.write_all_players()
        requested_username = " ".join(args[1:])
        
        player = self.server.get_player(requested_username)
        if player:
            now = datetime.datetime.now()
            elapsed_time = now - player.session_start
            session_time = elapsed_time.total_seconds()
        else:
            session_time = 0
            player = Player(requested_username, "no-perk")
            self.server.database.load_player(player)
            
        time = seconds_to_hhmmss(
            player.total_time + session_time
        )
        message = "Stats for " + player.username + ":\n" + \
                "Sessions:\t\t\t" + str(player.total_logins) + "\n" + \
                "Play time:\t\t" + time +"\n" + \
                "Deaths:\t\t\t" + str(player.total_deaths) + "\n" + \
                "Kills:\t\t\t\t" + str(player.total_kills) + "\n" + \
                "Dosh earned:\t\t" + str(player.total_dosh) + "\n" + \
                "Dosh spent:\t\t" + str(player.total_dosh_spent) + "\n" + \
                "Health lost:\t\t" + str(player.total_health_lost) + "\n" + \
                "Dosh this game:\t" + str(player.game_dosh) + "\n" + \
                "Kills this wave:\t\t" + str(player.wave_kills) + "\n" + \
                "Dosh this wave:\t" + str(player.wave_dosh)
                
        return message
