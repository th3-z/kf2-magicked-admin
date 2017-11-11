
class Command():
    
    def __init__(self, server):
        self. server = server

        self.not_auth_message = "You're not authorised to use that command."

    def execute(self, username, args, admin):
        raise NotImplementedError("Command.execute() not implemented")

class CommandMapFactory():
    
    def __init__(self, server, chat):
        pass

    def get_commands():
        pass

class CommandPlayers(Command):
   
    def __init__(self, server):
        Command.__init__(self, server)
        
    def execute(self, username, args, admin):
        message = ""

        for player in self.server.players:
            mesg += str(player) + " \n"
        
        return message

class CommandGame(Command):
        
    def __init__(self, server):
        Command.__init__(self, server)

    def execute(self, username, args, admin):
        return str(self.server.game)

class CommandHelp(Command):

    def __init__(self, server):
        Command.__init__(self, server)

    def execute(self, username, args, admin):
        return "Player commands:\n !dosh, !kills, !top_dosh,\
                \n!top_kills, !diff   iculty, !length"

class CommandSay(Command):

    def __init__(self, server):
        Command.__init__(self, server)

    def execute(self, username, args, admin):
            return self.not_auth_message if not admin
                
            mesaage = " ".join(args[1:])
            # Unescape escape characters in say command
            message = bytes(mesg.encode("iso-8859-1","ignore")).decode('unicode_escape')
            return message

class CommandOnTime(Command):

    def __init__(self, server):
        self.command_threads = []
        Command.__init__(self, server)
    
    def execute(self, username, args, admin):
        return self.not_auth_message if not admin
        if args[0] == "stop_tc":
            self.terminate_all():
            return "Timed commands stopped"
        
        try:
            time = int(args[1])
        except ValueError:
            return "Malformed command, \""+args[1]+"\" is not an integer."

        time_command = TimedCommand(args[1:], time, self.chat

    def terminate_all(self):
        for command_thread in self.command_threads:
            commnd_thread.terminate

