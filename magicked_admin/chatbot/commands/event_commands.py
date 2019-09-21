from chatbot.command_scheduler import (CommandOnJoin, CommandOnTime,
                                       CommandOnTrader, CommandOnWave)
from chatbot.commands.command import Command


class CommandStartJoinCommand(Command):
    def __init__(self, server, scheduler):
        Command.__init__(self, server, admin_only=True, requires_patch=False)
        self.scheduler = scheduler

        self.help_text = "start_jc help"
        self.parser.add_argument("command", nargs="*")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if not args.command:
            return self.format_response(
                "Please specify a command to run", args
            )

        command = CommandOnJoin(self.server, " ".join(args.command))
        self.scheduler.schedule_command(command)
        return self.format_response("Player join command started", args)


class CommandStopJoinCommands(Command):
    def __init__(self, server, scheduler):
        Command.__init__(self, server, admin_only=True, requires_patch=False)
        self.scheduler = scheduler

        self.help_text = "stop_jc help"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        return self.format_response(
            self.scheduler.unschedule_commands(CommandOnJoin),
            args
        )


class CommandStartWaveCommand(Command):
    def __init__(self, server, scheduler):
        Command.__init__(self, server, admin_only=True, requires_patch=False)
        self.scheduler = scheduler

        self.help_text = "start_wc help"
        self.parser.add_argument("wave")
        self.parser.add_argument("command", nargs="*")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        try:
            wave = int(args.wave)
        except ValueError:
            return self.format_response(
                "'{}' is not a valid wave number".format(args.wave),
                args
            )

        if not args.command:
            return self.format_response(
                "Please specify a command to run", args
            )

        command = CommandOnWave(
            self.server, " ".join(args.command), wave
        )
        self.scheduler.schedule_command(command)
        return self.format_response("Wave start command started", args)


class CommandStopWaveCommands(Command):
    def __init__(self, server, scheduler):
        Command.__init__(self, server, admin_only=True, requires_patch=False)
        self.scheduler = scheduler

        self.help_text = "stop_wc help"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        return self.format_response(
            self.scheduler.unschedule_commands(CommandOnWave),
            args
        )


class CommandStartTimeCommand(Command):
    def __init__(self, server, scheduler):
        Command.__init__(self, server, admin_only=True, requires_patch=False)
        self.scheduler = scheduler

        self.help_text = "start_tc help"
        self.parser.add_argument("interval")
        self.parser.add_argument("command", nargs="*")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        try:
            interval = float(args.interval)
        except ValueError:
            return self.format_response(
                "'{}' is not a valid time interval".format(args.interval),
                args
            )

        if not args.command:
            return self.format_response(
                "Please specify a command to run", args
            )

        command = CommandOnTime(
            self.server, " ".join(args.command), interval
        )
        self.scheduler.schedule_command(command)
        return self.format_response("Time interval command started", args)


class CommandStopTimeCommands(Command):
    def __init__(self, server, scheduler):
        Command.__init__(self, server, admin_only=True, requires_patch=False)
        self.scheduler = scheduler

        self.help_text = "stop_tc help"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        return self.format_response(
            self.scheduler.unschedule_commands(CommandOnTime),
            args
        )


class CommandStartTraderCommand(Command):
    def __init__(self, server, scheduler):
        Command.__init__(self, server, admin_only=True, requires_patch=False)
        self.scheduler = scheduler

        self.help_text = "start_tc help"
        self.parser.add_argument("command", nargs="*")

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        if not args.command:
            return self.format_response(
                "Please specify a command to run", args
            )

        command = CommandOnTrader(
            self.server, " ".join(args.command)
        )
        self.scheduler.schedule_command(command)
        return self.format_response("Trader open command started", args)


class CommandStopTraderCommands(Command):
    def __init__(self, server, scheduler):
        Command.__init__(self, server, admin_only=True, requires_patch=False)
        self.scheduler = scheduler

        self.help_text = "stop_wc help"

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        elif args.help:
            return self.format_response(self.help_text, args)

        return self.format_response(
            self.scheduler.unschedule_commands(CommandOnTrader),
            args
        )
