from chatbot.commands.command import Command
import server.server as server
import server.game as game

from os import path

class CommandSay(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        if len(args) < 2:
            return "No message was specified."

        message = " ".join(args[1:])
        # Unescape escape characters in say command
        message = bytes(message.encode("iso-8859-1", "ignore"))\
            .decode('unicode_escape')
        return message

class CommandEnforceLevels(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message

        self.server.enforce_levels()


class CommandRun(Command):
    def __init__(self, server, chatbot, admin_only=True):
        Command.__init__(self, server, admin_only)

        self.chatbot = chatbot

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        if len(args) < 2:
            return "No file was specified."

        if not path.exists(args[1]):
            return "File not found"

        self.chatbot.execute_script(args[1])

        return


class CommandRestart(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message

        self.server.restart_map()
        return "Restarting map."


class CommandLoadMap(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message

        if len(args) < 2:
            return "Missing argument (map name)"

        self.server.change_map(args[1])
        return "Changing map."


class CommandPassword(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message

        if len(args) < 2:
            return "Game password state is " + str(self.server.web_admin.has_game_password())
        elif args[1] in ['on', 'yes', 'y', '1', 'enable', 'enabled']:
            self.server.web_admin.set_game_password(self.server.game_password)
            return "Game password enabled"
        elif args[1] in ['off', 'no', 'n', '0', 'disable', 'disabled']:
            self.server.web_admin.set_game_password()
            return "Game password disabled"
        else:
            return "Unrecognised argument: " + args[1] + "\n" \
                   + "Options are: on, off"


class CommandSilent(Command):
    def __init__(self, server, chatbot, admin_only=True):
        self.chatbot = chatbot
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message

        if self.chatbot.silent:
            self.chatbot.silent = False
            return None
        else:
            self.chatbot.command_handler("server", "say Silent mode enabled.",
                                         admin=True)
            self.chatbot.silent = True


class CommandLength(Command):
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        if len(args) < 2:
            return "Length not recognised. Options are short, medium, or long."

        if args[1] in ["short", "0"]:
            length = game.LEN_SHORT
        elif args[1] in ["medium", "med", "normal", "1"]:
            length = game.LEN_NORM
        elif args[1] in ["long", "2"]:
            length = game.LEN_LONG
        else:
            return "Length not recognised. Options are short, medium, or long."

        self.server.set_length(length)
        return "Length change will take effect next game."


class CommandDifficulty(Command):
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        if len(args) < 2:
            return "Difficulty not recognised. " + \
                   "Options are normal, hard, suicidal, or hell."

        if args[1] in ["normal", "0"]:
            difficulty = game.DIFF_NORM
        elif args[1] in ["hard", "1"]:
            difficulty = game.DIFF_HARD
        elif args[1] in ["suicidal", "sui", "2"]:
            difficulty = game.DIFF_SUI
        elif args[1] in ["hell", "hoe", "hellonearth", "3"]:
            difficulty = game.DIFF_HOE
        else:
            return "Difficulty not recognised. " + \
                   "Options are normal, hard, suicidal, or hell."

        self.server.set_difficulty(difficulty)
        return "Difficulty change will take effect next game."


class CommandGameMode(Command):
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        if len(args) < 2:
            return "GameMode not recognised. " + \
                   "Options are endless, survival, weekly or versus."

        if args[1] in ["e", "end", "endless"]:
            mode = game.GAME_TYPE_ENDLESS
        elif args[1] in ["s", "srv", "survival"]:
            mode = game.GAME_TYPE_SURVIVAL
        elif args[1] in ["w", "week", "weekly"]:
            mode = game.GAME_TYPE_WEEKLY
        elif args[1] in ["v", "vs", "versus"]:
            mode = game.GAME_TYPE_SURVIVAL_VS
        else:
            return "GameMode not recognised. " + \
                   "Options are endless, survival, weekly or versus."

        self.server.change_game_type(mode)
        return "GameMode will be changed to {0}.".format(str(mode))
