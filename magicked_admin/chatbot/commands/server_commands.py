from os import path

import server.game as game
from chatbot.commands.command import Command
from web_admin.constants import *


class CommandBan(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.parser.add_argument("username")
        self.help_text = "Help text for the ban command"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if not args.username:
            return self.format_response(
                "Missing argument, username or Steam ID.", args
            )

        banned = self.server.ban_player(args.username)

        if banned:
            return self.format_response(
                "Player, {}, was banned.".format(banned), args
            )
        else:
            return self.format_response("Player not found.", args)


class CommandSay(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = "this is the say help"
        self.parser.add_argument("message", nargs="*")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        message = ' '.join(args.message)

        # Unescape escape characters e.g. \n -> newline
        message = bytes(message.encode("iso-8859-1", "ignore")) \
            .decode('unicode_escape')

        return self.format_response(message, args)


class CommandOp(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = "op help"
        self.parser.add_argument("username")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        player = self.server.get_player_by_username(args.username)
        if not player:
            message = "Couldn't find player '{}'".format(args.username)
        else:
            player.op = 1
            message = "Oped {}".format(player.username)

        self.server.write_all_players()

        return self.format_response(message, args)


class CommandDeop(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = "deop help"
        self.parser.add_argument("username")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        player = self.server.get_player_by_username(args.username)
        if not player:
            message = "Couldn't find player '{}'".format(args.username)
        else:
            player.op = 0
            message = "Deoped {}".format(player.username)

        self.server.write_all_players()

        return self.format_response(message, args)


class CommandEnforceLevels(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = "enforce_levels help"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        self.server.enforce_levels()


class CommandGameMaps(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = "game maps help text"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        message = ", ".join(self.server.get_maps())

        return self.format_response(message, args)


class CommandGameMap(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = "game map help text"
        self.parser.add_argument("map_title")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if args.map_name:
            map_title = self.server.find_map(args.map_title)
        else:
            map_title = self.server.game.game_map.title

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

        return self.format_response(message, args)


class CommandEnforceDosh(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = "enforce_dosh help"
        # TODO amount optional argument

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        self.server.enforce_dosh()


class CommandKick(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.parser.add_argument("username")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if not args.username:
            return self.format_response(
                "Missing argument, username or Steam ID.", args.pad_output
            )

        kicked = self.server.kick_player(args.username)

        if kicked:
            return self.format_response(
                "Player, {}, was kicked.".format(kicked), args
            )
        else:
            return self.format_response("Player not found.", args)


class CommandRun(Command):
    def __init__(self, server, chatbot):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.chatbot = chatbot
        self.help_text = "run help"
        self.parser.add_argument("file")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if not args.file:
            return self.format_response("No file was specified.", args)

        if not path.exists(args.file):
            return self.format_response("File not found", args)

        self.chatbot.execute_script(args.file)


class CommandRestart(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = "restart help"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        self.server.restart_map()
        return self.format_response("Restarting map...", args)


class CommandLoadMap(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = "load map help"
        self.parser.add_argument("map_name")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if not args.map_name:
            return self.format_response("Missing argument (map name)", args)

        self.server.change_map(args.map_name)
        return self.format_response("Changing map.", args)


class CommandPassword(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = "password help"
        self.parser.add_argument("state")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if not args.state:
            enabled = self.server.web_admin.has_game_password()
            message = "Game password is {}".format(
                "enabled" if enabled else "disabled"
            )

        else:
            if args.state in ['on', 'yes', 'y', '1', 'enable']:
                self.server.web_admin.set_game_password(
                    self.server.game_password
                )
                message = "Game password enabled"

            elif args.state in ['off', 'no', 'n', '0', 'disable']:
                self.server.web_admin.set_game_password()
                message = "Game password disabled"

            else:
                message = "Unrecognised option {}".format(args.state)

        return self.format_response(message, args)


class CommandSilent(Command):
    def __init__(self, server, chatbot):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.chatbot = chatbot
        self.help_text = "silent help"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if self.chatbot.silent:
            self.chatbot.silent = False
            return self.format_response("Silent mode disabled", args)
        else:
            self.chatbot.command_handler(
                "internal_command",
                "say Silent mode enabled.",
                USER_TYPE_INTERNAL
            )
            self.chatbot.silent = True


class CommandLength(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = "length help"
        self.parser.add_argument("length")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if not args.length:
            message = "Length not recognised. Options are " \
                      "short, medium, or long."
            return self.format_response(message, args)

        if args.length in ["short", "0"]:
            length = LEN_SHORT
        elif args.length in ["medium", "med", "normal", "1"]:
            length = LEN_NORM
        elif args.length in ["long", "2"]:
            length = LEN_LONG
        else:
            return self.format_response(
                "Length not recognised. Options are short, medium, or long.",
                args
            )

        self.server.set_length(length)
        return self.format_response(
            "Length change will take effect next game.",
            args
        )


class CommandDifficulty(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = "difficulty help"
        self.parser.add_argument("difficulty")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if not args.length:
            message = "Difficulty not recognised. Options are normal, hard, " \
                      "suicidal, or hell."
            return self.format_response(message, args)

        if args.length in ["normal", "0"]:
            difficulty = DIFF_NORM
        elif args.length in ["hard", "1"]:
            difficulty = DIFF_HARD
        elif args.length in ["suicidal", "sui", "2"]:
            difficulty = DIFF_SUI
        elif args.length in ["hell", "hoe", "hellonearth", "3"]:
            difficulty = DIFF_HOE
        else:
            return self.format_response(
                "Difficulty not recognised. Options are normal, hard, "
                "suicidal, or hell.",
                args
            )

        self.server.set_difficulty(difficulty)
        return self.format_response(
            "Difficulty change will take effect next game.",
            args
        )


class CommandGameMode(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = "game mode help"
        self.parser.add_argument("game_mode")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if not args.length:
            return self.format_response(
                "GameMode not recognised.  Options are endless, survival, "
                "weekly or versus.",
                args
            )

        if args.game_mode in ["e", "end", "endless"]:
            mode = GAME_TYPE_ENDLESS
        elif args.game_mode in ["s", "srv", "survival"]:
            mode = GAME_TYPE_SURVIVAL
        elif args.game_mode in ["w", "week", "weekly"]:
            mode = GAME_TYPE_WEEKLY
        elif args.game_mode in ["v", "vs", "versus"]:
            mode = GAME_TYPE_SURVIVAL_VS
        else:
            return self.format_response(
                "GameMode not recognised. Options are endless, survival, "
                "weekly or versus.",
                args
            )

        self.server.change_game_type(mode)
        return self.format_response(
            "Game mode will be changed to {0}.".format(str(mode)),
            args
        )
