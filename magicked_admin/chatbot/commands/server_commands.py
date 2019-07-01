from os import path

import server.game as game
import server.server as server
from chatbot.commands.command import Command
from web_admin.constants import *
from utils.text import pad_output


class CommandSay(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message
        if len(args) < 2:
            return pad_output("No message was specified.")

        message = " ".join(args[1:])
        # Unescape escape characters in say command
        message = bytes(message.encode("iso-8859-1", "ignore"))\
            .decode('unicode_escape')
        return message


class CommandOp(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message
        
        player = self.server.get_player_by_username(args[1])
        if not player:
            return pad_output("Couldn't identify player '{}'".format(args[1]))
        
        if args[0] == "deop":
            player.op = 0
            self.server.write_all_players()
            return pad_output("Deoped {}".format(player.username))
        else:
            player.op = 1
            self.server.write_all_players()
            return pad_output("Oped {}".format(player.username))


class CommandEnforceLevels(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message

        self.server.enforce_levels()


class CommandGameMap(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message

        if args[0] == "maps":
            message = ", ".join(self.server.get_maps())
            return message

        elif len(args) == 1:
            map_title = self.server.game.game_map.title

        elif len(args) == 2:
            map_title = self.server.find_map(args[1])

        self.server.write_game_map()

        game_map = game.GameMap(map_title)
        self.server.database.load_game_map(game_map)

        total_plays = game_map.plays_survival \
                      + game_map.plays_weekly \
                      + game_map.plays_endless \
                      + game_map.plays_survival_vs \
                      + game_map.plays_other
        
        message = "Stats for {} ({}):\n".format(game_map.name, game_map.title)
        message += "Total plays: {} \n".format(total_plays)
        message += "Record wave: {} \n".format(game_map.highest_wave)
        message += "Survival wins: {} \n".format(game_map.wins_survival)
        return pad_output(message)


class CommandEnforceDosh(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message

        self.server.enforce_dosh()


class CommandKick(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message

        if len(args) < 2:
            return pad_output("Missing argument, username or Steam ID.")

        kicked = self.server.kick_player(args[1])

        if kicked:
            return pad_output("Player, {}, was kicked.".format(kicked))
        else:
            return pad_output("Player not found.")


class CommandBan(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message

        if len(args) < 2:
            return pad_output("Missing argument, username or Steam ID.")

        kicked = self.server.ban_player(args[1])

        if kicked:
            return pad_output("Player, {}, was banned.".format(kicked))
        else:
            return pad_output("Player not found.")


class CommandRun(Command):
    def __init__(self, server, chatbot):
        Command.__init__(self, server, admin_only=True)

        self.chatbot = chatbot

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message
        if len(args) < 2:
            return pad_output("No file was specified.")

        if not path.exists(args[1]):
            return pad_output("File not found")

        self.chatbot.execute_script(args[1])

        return


class CommandRestart(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message

        self.server.restart_map()
        return pad_output("Restarting map...")


class CommandLoadMap(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message

        if len(args) < 2:
            return pad_output("Missing argument (map name)")

        self.server.change_map(args[1])
        return pad_output("Changing map.")


class CommandPassword(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message

        # TODO rewrite

        if len(args) < 2:
            return "Game password state is " \
                   + str(self.server.web_admin.has_game_password())
        elif args[1] in ['on', 'yes', 'y', '1', 'enable', 'enabled']:
            self.server.web_admin.set_game_password(self.server.game_password)
            return "Game password enabled"
        elif args[1] in ['off', 'no', 'n', '0', 'disable', 'disabled']:
            self.server.web_admin.set_game_password()
            return "Game password disabled"
        elif args[1] == 'set' and len(args) > 2:
            self.server.web_admin.set_game_password(args[2])
            return "Game password set"
        else:
            return "Unrecognised argument: " + args[1] + "\n" \
                   + "Options are: on, off, set <password>"


class CommandSilent(Command):
    def __init__(self, server, chatbot):
        self.chatbot = chatbot
        Command.__init__(self, server, admin_only=True)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message

        if self.chatbot.silent:
            self.chatbot.silent = False
            return None
        else:
            self.chatbot.command_handler(
                "internal_command",
                pad_output("say Silent mode enabled."),
                USER_TYPE_INTERNAL
            )
            self.chatbot.silent = True


class CommandLength(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message
        if len(args) < 2:
            return pad_output(
                "Length not recognised. Options are short, medium, or long."
            )

        if args[1] in ["short", "0"]:
            length = LEN_SHORT
        elif args[1] in ["medium", "med", "normal", "1"]:
            length = LEN_NORM
        elif args[1] in ["long", "2"]:
            length = LEN_LONG
        else:
            return pad_output(
                "Length not recognised. Options are short, medium, or long."
            )

        self.server.set_length(length)
        return pad_output("Length change will take effect next game.")


class CommandDifficulty(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message
        if len(args) < 2:
            return pad_output(
                "Difficulty not recognised. "
                "Options are normal, hard, suicidal, or hell."
            )

        if args[1] in ["normal", "0"]:
            difficulty = DIFF_NORM
        elif args[1] in ["hard", "1"]:
            difficulty = DIFF_HARD
        elif args[1] in ["suicidal", "sui", "2"]:
            difficulty = DIFF_SUI
        elif args[1] in ["hell", "hoe", "hellonearth", "3"]:
            difficulty = DIFF_HOE
        else:
            return pad_output(
                "Difficulty not recognised. "
                "Options are normal, hard, suicidal, or hell."
            )

        self.server.set_difficulty(difficulty)
        return pad_output("Difficulty change will take effect next game.")


class CommandGameMode(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True)

    def execute(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message
        if len(args) < 2:
            return pad_output(
                "GameMode not recognised. "
                "Options are endless, survival, weekly or versus."
            )

        if args[1] in ["e", "end", "endless"]:
            mode = GAME_TYPE_ENDLESS
        elif args[1] in ["s", "srv", "survival"]:
            mode = GAME_TYPE_SURVIVAL
        elif args[1] in ["w", "week", "weekly"]:
            mode = GAME_TYPE_WEEKLY
        elif args[1] in ["v", "vs", "versus"]:
            mode = GAME_TYPE_SURVIVAL_VS
        else:
            return pad_output(
                "GameMode not recognised. "
                "Options are endless, survival, weekly or versus."
            )

        self.server.change_game_type(mode)
        return pad_output("GameMode will be changed to {0}.".format(str(mode)))
