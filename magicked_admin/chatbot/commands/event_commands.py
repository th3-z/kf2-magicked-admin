import gettext

from chatbot.commands.handlers import (
    OnJoinHandler, OnTimeHandler, OnTraderHandler, OnWaveHandler
)
from chatbot.commands.command import Command
from chatbot.commands import ALL_WAVES
from utils import warning

_ = gettext.gettext

"""

ontime <command> [options] command
!on_time add --seconds 5 --repeat "say something"
!on_time show
!on_time del 5

!on_trader
!ls_on_trader


"""


class CommandOnTime(Command):
    def __init__(self, server, scheduler):
        Command.__init__(self, server, admin_only=True, requires_patch=False)
        self.scheduler = scheduler

        self.help_text = _("Usage: !start_tc [-r -t] COMMAND\n"
                           "\tCOMMAND - Command to run\n"
                           "\t-r --repeat - Optional, run repeatedly\n"
                           "\t-t --time - Seconds before running\n"
                           "Desc: Runs a command after some time delay")
        self.parser.add_argument("--time", "-t")
        self.parser.add_argument("--repeat", "-r", action="store_true")
        self.parser.add_argument("command", nargs="*")

    def execute(self, username, args, user_flags):
        if "--" not in args:
            warning(_("Ambiguous event command, please use ' -- ' to separate "
                      "commands"))
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if not args.time:
            return self.format_response(
                _("Please specify a time interval, '!start_tc -h' for help"),
                args
            )

        try:
            interval = float(args.time)
        except ValueError:
            return self.format_response(
                _("'{}' is not a valid time interval").format(args.time),
                args
            )

        if not args.command:
            return self.format_response(
                _("Please specify a command to run"), args
            )

        run_once = False if args.repeat else True

        command = CommandOnTime(
            self.server.event_manager, " ".join(args.command), interval, run_once=run_once
        )
        command.start()
        #self.scheduler.schedule_command(command)
        return self.format_response(_("Time interval command started"), args)



class CommandStartJoinCommand(Command):
    def __init__(self, server, scheduler):
        Command.__init__(self, server, admin_only=True, requires_patch=False)
        self.scheduler = scheduler

        self.help_text = _("Usage: !start_jc [--returning] COMMAND\n"
                           "\t-r --returning "
                           "- Set for only returning players\n"
                           "\tCOMMAND - Command to run\n"
                           "Desc: Runs a command when a player joins the "
                           "match")
        self.parser.add_argument("--returning", "-r", action="store_true")
        self.parser.add_argument("command", nargs="*")

        self.run_delay = 5

    def execute(self, username, args, user_flags):
        if "--" not in args:
            warning(_("Ambiguous event command, please use ' -- ' to separate "
                      "commands"))
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if not args.command:
            return self.format_response(
                _("Please specify a command to run"), args
            )

        delayed_command = [
            "start_tc", "-qt", str(self.run_delay), "--", *args.command
        ]

        command = CommandOnJoin(
            self.server, " ".join(delayed_command), returning=args.returning
        )
        self.scheduler.schedule_command(command)
        return self.format_response(_("Player join command started"), args)


class CommandStopJoinCommands(Command):
    def __init__(self, server, scheduler):
        Command.__init__(self, server, admin_only=True, requires_patch=False)
        self.scheduler = scheduler

        self.help_text = _("Usage: !stop_jc\n"
                           "Desc: Stops all join commands")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        return self.format_response(
            self.scheduler.unschedule_commands(CommandOnJoin),
            args
        )


class CommandStartWaveCommand(Command):
    def __init__(self, server, scheduler):
        Command.__init__(self, server, admin_only=True, requires_patch=True)
        self.scheduler = scheduler

        self.help_text = _("Usage: !start_wc [--wave] COMMAND\n"
                           "\t-w --wave - Optional, wave to run on\n"
                           "\tCOMMAND - Command to run\n"
                           "Desc: Run a command at the start of a wave, wave"
                           " can be omitted top run on every wave")
        self.parser.add_argument("--wave", "-w")
        self.parser.add_argument("command", nargs="*")

    def execute(self, username, args, user_flags):
        if "--" not in args:
            warning(_("Ambiguous event command, please use ' -- ' to separate "
                      "commands"))
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if args.wave:
            try:
                wave = int(args.wave)
            except ValueError:
                return self.format_response(
                    _("'{}' is not a valid wave number").format(args.wave),
                    args
                )
        else:
            wave = ALL_WAVES

        if not args.command:
            return self.format_response(
                _("Please specify a command to run"), args
            )

        command = CommandOnWave(
            self.server, " ".join(args.command), wave
        )
        self.scheduler.schedule_command(command)
        return self.format_response(_("Wave start command started"), args)


class CommandStopWaveCommands(Command):
    def __init__(self, server, scheduler):
        Command.__init__(self, server, admin_only=True, requires_patch=True)
        self.scheduler = scheduler

        self.help_text = _("Usage: !stop_wc\n"
                           "Desc: Stops all wave commands")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        return self.format_response(
            self.scheduler.unschedule_commands(CommandOnWave),
            args
        )


class CommandStartTimeCommand(Command):
    def __init__(self, server, scheduler):
        Command.__init__(self, server, admin_only=True, requires_patch=False)
        self.scheduler = scheduler

        self.help_text = _("Usage: !start_tc [-r -t] COMMAND\n"
                           "\tCOMMAND - Command to run\n"
                           "\t-r --repeat - Optional, run repeatedly\n"
                           "\t-t --time - Seconds before running\n"
                           "Desc: Runs a command after some time delay")
        self.parser.add_argument("--time", "-t")
        self.parser.add_argument("--repeat", "-r", action="store_true")
        self.parser.add_argument("command", nargs="*")

    def execute(self, username, args, user_flags):
        if "--" not in args:
            warning(_("Ambiguous event command, please use ' -- ' to separate "
                      "commands"))
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if not args.time:
            return self.format_response(
                _("Please specify a time interval, '!start_tc -h' for help"),
                args
            )

        try:
            interval = float(args.time)
        except ValueError:
            return self.format_response(
                _("'{}' is not a valid time interval").format(args.time),
                args
            )

        if not args.command:
            return self.format_response(
                _("Please specify a command to run"), args
            )

        run_once = False if args.repeat else True

        command = CommandOnTime(
            self.server.event_manager, " ".join(args.command), interval, run_once=run_once
        )
        command.start()
        #self.scheduler.schedule_command(command)
        return self.format_response(_("Time interval command started"), args)


class CommandStopTimeCommands(Command):
    def __init__(self, server, scheduler):
        Command.__init__(self, server, admin_only=True, requires_patch=False)
        self.scheduler = scheduler

        self.help_text = _("Usage: !stop_tc\n"
                           "Desc: Stops all timed commands")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        return self.format_response(
            self.scheduler.unschedule_commands(CommandOnTime),
            args
        )


class CommandStartTraderCommand(Command):
    def __init__(self, server, scheduler):
        Command.__init__(self, server, admin_only=True, requires_patch=False)
        self.scheduler = scheduler

        self.help_text = _("Usage: !start_trc [--wave] COMMAND\n"
                           "\tCOMMAND - Command to run\n"
                           "\t-w --wave - Optional, wave to run on\n"
                           "Desc: Runs a command when the trader opens, wave"
                           " can be omitted to run every time the trader "
                           "opens")
        self.parser.add_argument("--wave", "-w")
        self.parser.add_argument("command", nargs="*")

    def execute(self, username, args, user_flags):
        if "--" not in args:
            warning(_("Ambiguous event command, please use ' -- ' to separate "
                      "commands"))
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if not args.command:
            return self.format_response(
                _("Please specify a command to run"), args
            )

        wave = args.wave if args.wave else ALL_WAVES
        try:
            wave = int(wave)
        except ValueError:
            return self.format_response(
                _("'{}' is not a valid wave number").format(args.wave),
                args
            )

        command = CommandOnTrader(
            self.server, " ".join(args.command), wave=wave
        )
        self.scheduler.schedule_command(command)
        return self.format_response(_("Trader open command started"), args)


class CommandStopTraderCommands(Command):
    def __init__(self, server, scheduler):
        Command.__init__(self, server, admin_only=True, requires_patch=False)
        self.scheduler = scheduler

        self.help_text = _("Usage: !stop_trc\n"
                           "Desc: Stops all trader commands")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        return self.format_response(
            self.scheduler.unschedule_commands(CommandOnTrader),
            args
        )
