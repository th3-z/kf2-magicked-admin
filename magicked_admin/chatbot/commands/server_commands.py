from os import path
import gettext

from .command import Command
from utils import find_data_file
from web_admin.constants import *
from server.level import Level

_ = gettext.gettext


class CommandAlias(Command):
    def __init__(self, server, chatbot):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.parser.add_argument(
            "-op", "--op",
            action="store_true"
        )
        self.parser.add_argument("name", nargs=1)
        self.parser.add_argument("command", nargs="*")

        self.help_text = _("Usage: !alias [--op] NAME -- COMMAND\n"
                           "\t-o --op - Set to restrict alias to ops\n"
                           "\tNAME - Name of alias \n"
                           "\tCOMMAND - Some command \n"
                           "Desc: Runs some Lua code")

        self.chatbot = chatbot

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if args.command:
            command = " ".join(args.command)
        else:
            return self.format_response(
                _("Missing argument, command"), args
            )

        if args.name:
            name = args.name[0]
        else:
            return self.format_response(
                _("Missing argument, name"), args
            )

        self.chatbot.add_alias(name, command, args.op)
        return _("Added alias")


class CommandLua(Command):
    def __init__(self, server, chatbot):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.parser.add_argument("lua", nargs="*")
        self.help_text = _("Usage: !lua LUA\n"
                           "\tLUA - Lua statements \n"
                           "Desc: Runs some Lua code")

        self.chatbot = chatbot

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if args.lua:
            lua = " ".join(args.lua)
        else:
            return self.format_response(
                _("Missing argument, Lua"), args
            )

        result = self.chatbot.lua_bridge.eval(lua)
        return str(result)


class CommandBan(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.parser.add_argument("username", nargs="*")
        self.help_text = _("Usage: !ban USERNAME\n"
                           "\tUSERNAME - Player to ban\n"
                           "Desc: Bans a player from the server")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if args.username:
            username = " ".join(args.username)
        else:
            return self.format_response(
                _("Missing argument, username or Steam ID"), args
            )

        banned = self.server.ban_player(username)
        if not banned:
            return self.format_response(_("Player not found"), args)

        return self.format_response(
            _("Player, {}, was banned").format(banned), args
        )


class CommandSay(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = _("Usage: !say MESSAGE\n"
                           "\tMESSAGE - Message to echo\n"
                           "Desc: Echos a message in chat")
        self.parser.add_argument("message", nargs="*")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        message = ' '.join(args.message)

        # Unescape escape characters e.g. \n -> newline
        message = bytes(message.encode("iso-8859-1", "ignore")) \
            .decode('unicode_escape')

        return self.format_response(message, args)


class CommandOp(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = _("Usage: !op USERNAME\n"
                           "\tUSERNAME - Player to give operator status\n"
                           "Desc: Allows a player to use admin commands")
        self.parser.add_argument("username", nargs="*")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if args.username:
            username = " ".join(args.username)
        else:
            return self.format_response(
                _("Missing argument, username or Steam ID"), args
            )

        player = self.server.get_player_by_username(username)
        if not player:
            message = _("Couldn't find player '{}'").format(username)
        else:
            player.op = 1
            message = _("Oped {}").format(player.username)

        return self.format_response(message, args)


class CommandDeop(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = _("Usage: !deop USERNAME\n"
                           "\tUSERNAME - Player to revoke op status for\n"
                           "Desc: Revokes a players ability to use admin "
                           "commands")
        self.parser.add_argument("username", nargs="*")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if args.username:
            username = " ".join(args.username)
        else:
            return self.format_response(
                _("Missing argument, username or Steam ID"), args
            )

        player = self.server.get_player_by_username(username)
        if not player:
            message = _("Couldn't find player '{}'").format(username)
        else:
            player.op = 0
            message = _("Deoped {}").format(player.username)

        return self.format_response(message, args)


class CommandGameMaps(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = _("Usage: !maps [--all]\n"
                           "\t-a --all - Show all available maps\n"
                           "Desc: Shows maps that are in the map cycle")
        self.parser.add_argument(
            "-a", "--all",
            action="store_true"
        )

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        message = ", ".join(self.server.get_maps(not args.all))

        return self.format_response(message, args)


class CommandGameMap(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=False, requires_patch=False)

        self.help_text = _("Usage: !map\n"
                           "Desc: Shows statistics about the current map")
        self.parser.add_argument("map_name", nargs="?")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if args.map_name:
            map_title = self.server.find_map(args.map_name)
        else:
            map_title = self.server.match.level.title

        level = Level(map_title)

        total_plays = (level.plays_survival
                       + level.plays_weekly
                       + level.plays_endless
                       + level.plays_survival_vs
                       + level.plays_other)

        message = _("Stats for {}:\n").format(level.name)
        message += _("Total plays: {} \n").format(total_plays)
        message += _("Record wave: {} \n").format(level.highest_wave)
        message += _("Survival wins: {} \n").format(level.wins_survival)

        return self.format_response(message, args)


class CommandEnforceDosh(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = _("Usage: !enforce_dosh AMOUNT\n"
                           "\tAMOUNT - Kicks players over this amount\n"
                           "Desc: Kicks players with more dosh than the "
                           "amount specified")
        self.parser.add_argument("amount", nargs="?")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if not args.amount:
            return self.format_response(
                _("Please specify a maximum amount of dosh"), args
            )

        try:
            amount = int(args.amount)
        except ValueError:
            return self.format_response(
                _("'{}' is not a valid number").format(args.amount),
                args
            )

        for player in self.server.players:
            if player.dosh > amount:
                self.server.web_admin.kick_player(player.player_key)


class CommandKick(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.parser.add_argument("username", nargs="*")
        self.help_text = _("Usage: !kick USERNAME\n"
                           "\tUSERNAME - Player to kick\n"
                           "Desc: Kicks a player from the match")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if args.username:
            username = " ".join(args.username)
        else:
            return self.format_response(
                _("Missing argument, username or Steam ID"), args
            )

        kicked = self.server.kick_player(username)
        if not kicked:
            return self.format_response(_("Player not found"), args)

        return self.format_response(
            _("Player, {}, was kicked").format(kicked), args
        )


class CommandUpdateMotd(Command):
    def __init__(self, server, motd_updater):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.motd_updater = motd_updater

        self.help_text = _("Usage: !update_motd\n"
                           "Desc: Updates the MOTD from the template file")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        self.motd_updater.update()

        return self.format_response(
            _("Updated the MOTD"), args
        )


class CommandReloadMotd(Command):
    def __init__(self, server, motd_updater):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.motd_updater = motd_updater

        self.help_text = _("Usage: !reload_motd\n"
                           "Desc: Reload the server's *.motd file")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        self.motd_updater.reload()

        return self.format_response(
            _("Reloaded the MOTD"), args
        )


class CommandRun(Command):
    def __init__(self, server, chatbot):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.chatbot = chatbot
        self.help_text = _("Usage: !run FILE\n"
                           "\tFILE - Some file in 'conf/scripts'\n"
                           "Desc: Runs a script")
        self.parser.add_argument("file", nargs="*")

        self.scripts_folder = "conf/scripts"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if not args.file:
            return self.format_response(_("No script was specified"), args)

        args.file = " ".join(args.file)
        script_path = find_data_file(self.scripts_folder + "/" + args.file)
        if not path.exists(script_path):
            return self.format_response(_("Script not found"), args)

        self.chatbot.execute_script(script_path)


class CommandRestart(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = _("Usage: !restart\n"
                           "Desc: Restarts the match")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        self.server.restart_map()
        return self.format_response(_("Restarting map..."), args)


class CommandLoadMap(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = _("Usage: !load_map MAP_NAME\n"
                           "\tMAP_NAME - Map to load\n"
                           "Desc: Immediately changes the map.")
        self.parser.add_argument("map_name", nargs="?")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if not args.map_name:
            return self.format_response(_("Missing argument (map name)"), args)

        self.server.change_map(args.map_name)
        return self.format_response(_("Changing map"), args)


class CommandPassword(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = _("Usage: !password [--set] STATE\n"
                           "\tSTATE - On, off, or new password\n"
                           "\t-s --set - Set a new password\n"
                           "Desc: Enables or disables the game password "
                           "configured in 'conf/magicked_admin.conf', state "
                           "can be on, off, or a new password.")
        self.parser.add_argument("-s", "--set", type=str)
        self.parser.add_argument("state", nargs="?")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if not (args.state or args.set):
            enabled = self.server.web_admin.has_game_password()
            return self.format_response(
                _("Game password is currently {}").format(
                    _("enabled") if enabled else _("disabled")
                ), args
            )

        if args.set:
            self.server.match_password = args.set

        if args.set or args.state in ['on', 'yes', 'y', '1', 'enable']:
            self.server.web_admin.set_game_password(
                self.server.match_password
            )
            message = _("Game password enabled")

        elif args.state in ['off', 'no', 'n', '0', 'disable']:
            self.server.web_admin.set_game_password()
            message = _("Game password disabled")

        else:
            message = _("Unrecognised option {}").format(args.state)

        return self.format_response(message, args)


class CommandSilent(Command):
    def __init__(self, server, chatbot):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.chatbot = chatbot
        self.help_text = _("Usage: !silent [--quiet]\n"
                           "\t-q --quiet - Suppresses output'\n"
                           "Desc: Toggles command output globally")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if self.chatbot.silent:
            self.chatbot.silent = False
            return self.format_response(_("Silent mode disabled"), args)
        else:
            message = self.format_response(_("Silent mode enabled"), args)
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

        self.help_text = _("Usage: !length LENGTH\n"
                           "\tLENGTH - Length to change to\n"
                           "Desc: Changes the game length next match")
        self.parser.add_argument("length", nargs="?")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if not args.length:
            message = _("Length not recognised, options are: "
                        "short, medium, or long")
            return self.format_response(message, args)

        if args.length in ["short", "0"]:
            length = LEN_SHORT
        elif args.length in ["medium", "med", "normal", "1"]:
            length = LEN_NORM
        elif args.length in ["long", "2"]:
            length = LEN_LONG
        else:
            return self.format_response(
                _("Length not recognised, options are: short, medium, or "
                  "long"),
                args
            )

        self.server.set_length(length)
        return self.format_response(
            _("Length change will take effect next game"),
            args
        )


class CommandDifficulty(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = _("Usage: !difficulty DIFFICULTY\n"
                           "\tDIFFICULTY - Difficulty to change to\n"
                           "Desc: Changes the difficulty next match")
        self.parser.add_argument("difficulty", nargs="?")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if not args.difficulty:
            message = _("Difficulty not recognised, options are: normal, "
                        "hard, suicidal, or hell")
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
                _("Difficulty not recognised, options are: normal, hard, "
                  "suicidal, or hell"),
                args
            )

        self.server.set_difficulty(difficulty)
        return self.format_response(
            _("Difficulty change will take effect next game"),
            args
        )


class CommandGameMode(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)

        self.help_text = _("Usage: !game_mode MODE\n"
                           "\tMODE - Mode to change to\n"
                           "Desc: Immediately changes the game mode")
        self.parser.add_argument("game_mode", nargs="?")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if not args.game_mode:
            return self.format_response(
                _("Mode not recognised, options are: endless, survival, "
                  "weekly or versus"),
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
                _("GameMode not recognised, options are: endless, survival, "
                  "weekly or versus"),
                args
            )

        self.server.change_game_type(mode)

        return self.format_response(
            _("Game mode will be changed to {}").format(
                str(GAME_TYPE_DISPLAY[mode])
            ),
            args
        )
