from os import path

import server.game as game
from chatbot.commands.command import Command
from utils import find_data_file
from web_admin.constants import *


class CommandBan(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.parser.add_argument("username", nargs="*")
        self.help_text = "Usage: !ban USERNAME\n" \
                         "\tUSERNAME - Player to ban\n" \
                         "Desc: Bans a player from the server"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if args.username:
            username = " ".join(args.username)
        else:
            return self.format_response(
                "Missing argument, username or Steam ID", args
            )

        banned = self.server.ban_player(username)

        if banned:
            return self.format_response(
                "Player, {}, was banned".format(banned), args
            )
        else:
            return self.format_response("Player not found", args)


class CommandSay(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = "Usage: !say MESSAGE\n" \
                         "\tMESSAGE - Message to echo\n" \
                         "Desc: Echos a message in chat"
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

        self.help_text = "Usage: !op USERNAME\n" \
                         "\tUSERNAME - Player to give operator status\n" \
                         "Desc: Allows a player to use admin commands"
        self.parser.add_argument("username", nargs="*")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if args.username:
            username = " ".join(args.username)
        else:
            return self.format_response(
                "Missing argument, username or Steam ID", args
            )

        player = self.server.get_player_by_username(username)
        if not player:
            message = "Couldn't find player '{}'".format(username)
        else:
            player.op = 1
            message = "Oped {}".format(player.username)

        self.server.write_all_players()

        return self.format_response(message, args)


class CommandDeop(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = "Usage: !deop USERNAME\n" \
                         "\tUSERNAME - Player to revoke op status for\n" \
                         "Desc: Revokes a players ability to use admin " \
                         "commands"
        self.parser.add_argument("username", nargs="*")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if args.username:
            username = " ".join(args.username)
        else:
            return self.format_response(
                "Missing argument, username or Steam ID", args
            )

        player = self.server.get_player_by_username(username)
        if not player:
            message = "Couldn't find player '{}'".format(username)
        else:
            player.op = 0
            message = "Deoped {}".format(player.username)

        self.server.write_all_players()

        return self.format_response(message, args)


class CommandGameMaps(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = "Usage: !maps [--all]\n" \
                         "\t-a --all - Show all available maps\n" \
                         "Desc: Shows maps that are in the map cycle"
        self.parser.add_argument(
            "-a", "--all",
            action="store_true"
        )

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        message = ", ".join(self.server.get_maps(not args.all))

        return self.format_response(message, args)


class CommandGameMap(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = "Usage: !map\n" \
                         "Desc: Shows statistics about the current map"
        self.parser.add_argument("map_name", nargs="?")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if args.map_name:
            map_title = self.server.find_map(args.map_name)
        else:
            map_title = self.server.game.game_map.title

        self.server.write_game_map()

        game_map = game.GameMap(map_title)
        self.server.write_game_map()
        self.server.database.load_game_map(game_map)

        total_plays = game_map.plays_survival \
            + game_map.plays_weekly \
            + game_map.plays_endless \
            + game_map.plays_survival_vs \
            + game_map.plays_other

        message = "Stats for {}:\n".format(game_map.name)
        message += "Total plays: {} \n".format(total_plays)
        message += "Record wave: {} \n".format(game_map.highest_wave)
        message += "Survival wins: {} \n".format(game_map.wins_survival)

        return self.format_response(message, args)


class CommandEnforceDosh(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = "Usage: !enforce_dosh\n" \
                         "Desc: Kicks players with more dosh than the " \
                         "threshold configured in 'conf/magicked_admin.conf'"
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

        self.parser.add_argument("username", nargs="*")
        self.help_text = "Usage: !kick USERNAME\n" \
                         "\tUSERNAME - Player to kick\n" \
                         "Desc: Kicks a player from the match"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if args.username:
            username = " ".join(args.username)
        else:
            return self.format_response(
                "Missing argument, username or Steam ID", args
            )

        kicked = self.server.kick_player(username)

        if kicked:
            return self.format_response(
                "Player, {}, was kicked".format(kicked), args
            )
        else:
            return self.format_response("Player not found", args)


class CommandRun(Command):
    def __init__(self, server, chatbot):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.chatbot = chatbot
        self.help_text = "Usage: !run FILE\n" \
                         "\tFILE - Some file in 'conf/scripts'\n" \
                         "Desc: Runs a script"
        self.parser.add_argument("file", nargs="*")

        self.scripts_folder = "scripts"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if not args.file:
            return self.format_response("No script was specified", args)

        args.file = " ".join(args.file)
        script_path = find_data_file(self.scripts_folder + "/" + args.file)
        if not path.exists(script_path):
            return self.format_response("Script not found", args)

        self.chatbot.execute_script(script_path)


class CommandRestart(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = "Usage: !restart\n" \
                         "Desc: Restarts the match"

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

        self.help_text = "Usage: !load_map MAP_NAME\n" \
                         "\tMAP_NAME - Map to load\n" \
                         "Desc: Immediately changes the map."
        self.parser.add_argument("map_name", nargs="?")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if not args.map_name:
            return self.format_response("Missing argument (map name)", args)

        self.server.change_map(args.map_name)
        return self.format_response("Changing map", args)


class CommandPassword(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = "Usage: !password [--set] STATE\n" \
                         "\tSTATE - On, off, or new password\n" \
                         "\t-s --set - Set a new password\n" \
                         "Desc: Enables or disables the game password " \
                         "configured in 'conf/magicked_admin.conf', state " \
                         "can be on, off, or a new password."
        self.parser.add_argument("-s", "--set", type=str)
        self.parser.add_argument("state", nargs="?")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if not (args.state or args.set):
            enabled = self.server.web_admin.has_game_password()
            return self.format_response(
                "Game password is currently {}".format(
                    "enabled" if enabled else "disabled"
                ), args
            )

        if args.set:
            self.server.game_password = args.set

        if args.set or args.state in ['on', 'yes', 'y', '1', 'enable']:
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
        self.help_text = "Usage: !silent [--quiet]\n" \
                         "\t-q --quiet - Suppresses output'\n" \
                         "Desc: Toggles command output globally"

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
            message = self.format_response("Silent mode enabled", args)
            if message:
                self.chatbot.command_handler(
                    "internal_command",
                    "say {}".format(message).split(),
                    USER_TYPE_INTERNAL
                )
            self.chatbot.silent = True


class CommandLength(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = "Usage: !length LENGTH\n" \
                         "\tLENGTH - Length to change to\n" \
                         "Desc: Changes the game length next match"
        self.parser.add_argument("length", nargs="?")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if not args.length:
            message = "Length not recognised, options are: " \
                      "short, medium, or long"
            return self.format_response(message, args)

        if args.length in ["short", "0"]:
            length = LEN_SHORT
        elif args.length in ["medium", "med", "normal", "1"]:
            length = LEN_NORM
        elif args.length in ["long", "2"]:
            length = LEN_LONG
        else:
            return self.format_response(
                "Length not recognised, options are: short, medium, or long",
                args
            )

        self.server.set_length(length)
        return self.format_response(
            "Length change will take effect next game",
            args
        )


class CommandDifficulty(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = "Usage: !difficulty DIFFICULTY\n" \
                         "\tDIFFICULTY - Difficulty to change to\n" \
                         "Desc: Changes the difficulty next match"
        self.parser.add_argument("difficulty", nargs="?")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if not args.difficulty:
            message = "Difficulty not recognised, options are: normal, " \
                      "hard, suicidal, or hell"
            return self.format_response(message, args)

        if args.difficulty in ["normal", "0"]:
            difficulty = DIFF_NORM
        elif args.difficulty in ["hard", "1"]:
            difficulty = DIFF_HARD
        elif args.difficulty in ["suicidal", "sui", "2"]:
            difficulty = DIFF_SUI
        elif args.difficulty in ["hell", "hoe", "hellonearth", "3"]:
            difficulty = DIFF_HOE
        else:
            return self.format_response(
                "Difficulty not recognised, options are: normal, hard, "
                "suicidal, or hell",
                args
            )

        self.server.set_difficulty(difficulty)
        return self.format_response(
            "Difficulty change will take effect next game",
            args
        )


class CommandGameMode(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = "Usage: !game_mode MODE\n" \
                         "\tMODE - Mode to change to\n" \
                         "Desc: Immediately changes the game mode"
        self.parser.add_argument("game_mode", nargs="?")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if not args.game_mode:
            return self.format_response(
                "Mode not recognised, options are: endless, survival, "
                "weekly or versus",
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
                "GameMode not recognised, options are: endless, survival, "
                "weekly or versus",
                args
            )

        self.server.change_game_type(mode)
        return self.format_response(
            "Game mode will be changed to {0}".format(
                str(GAME_TYPE_DISPLAY[mode])
            ),
            args
        )
