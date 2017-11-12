from chatbot.commands.command import Command
import server.server as server

class CommandSay(Command):
    def __init__(self, server, adminOnly = True):
        Command.__init__(self, server, adminOnly)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
                
        mesaage = " ".join(args[1:])
        # Unescape escape characters in say command
        message = bytes(mesg.encode("iso-8859-1","ignore")).decode('unicode_escape')
        return message

class CommandRestart(Command):
    def __init__(self, server, adminOnly = True):
        Command.__init__(self, server, adminOnly)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        
        self.server.restart_map()
        return "Restarting map."
        
class CommandTogglePassword(Command):
    def __init__(self, server, adminOnly = True):
        Command.__init__(self, server, adminOnly)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        
        new_state = self.server.toggle_password()
        if new_state:
            return "Game password enabled"
        else:
            return "Game password disabled"
            
class CommandSilent(Command):
    def __init__(self, server, chatbot, adminOnly = True):
        Command.__init__(self, server, adminOnly)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        
        if self.chatbot.silent:
            self.chatbot.silent = False 
            return "Silent mode disabled."
        else:
            self.chatbot.command_handler("server", "say Silent mode enabled.", admin=True)
            self.chatbot.silent = True
 
class CommandLength(Command):
    def __init__(self, server, adminOnly = True):
        Command.__init__(self, server, adminOnly)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        
        if args[1] == "short":
            length = server.LEN_SHORT
        elif args[1] == "medium":
            length = server.LEN_NORM
        elif args[1] == "long":
            length = server.LEN_LONG
        else:
            return "Length not recognised. Options are short, medium, or long."
        
        self.server.set_length(length)
        return "Length change will take effect next game."
        
class CommandDifficulty(Command):
    def __init__(self, server, adminOnly = True):
        Command.__init__(self, server, adminOnly)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        
        if args[1] == "normal":
            difficulty = server.DIFF_NORM
        elif args[1] == "hard":
            difficulty = server.DIFF_HARD
        elif args[1] == "suicidal":
            difficulty = server.DIFF_SUI
        elif args[1] == "hell":
            difficulty = server.DIFF_HOE
        else:
            return "Difficulty not recognised. Options are normal, hard, suicidal, or hell."
        
        self.server.set_difficulty(difficulty)
        return "Difficulty change will take effect next game."