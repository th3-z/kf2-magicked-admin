import server.server as server
from chatbot.commands.command import Command
from chatbot.command_scheduler import (
    CommandOnTime, CommandOnWave, CommandOnJoin, CommandOnTrader
)
from web_admin.constants import *
from utils.text import pad_output


class CommandStartJoinCommand(Command):
    def __init__(self, server, scheduler):
        self.scheduler = scheduler
        Command.__init__(self, server, admin_only=True, requires_patch=False)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err


class CommandStopJoinCommands(Command):
    def __init__(self, server, scheduler):
        self.scheduler = scheduler
        Command.__init__(self, server, admin_only=True, requires_patch=False)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err


class CommandStartWaveCommand(Command):
    def __init__(self, server, scheduler):
        self.scheduler = scheduler
        Command.__init__(self, server, admin_only=True, requires_patch=False)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err


class CommandStopWaveCommands(Command):
    def __init__(self, server, scheduler):
        self.scheduler = scheduler
        Command.__init__(self, server, admin_only=True, requires_patch=False)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err


class CommandStartTimeCommand(Command):
    def __init__(self, server, scheduler):
        self.scheduler = scheduler
        Command.__init__(self, server, admin_only=True, requires_patch=False)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err

        interval = args[1]
        command = args[2:]
        command = CommandOnTime()
        self.scheduler.schedule_command()


class CommandStopTimeCommands(Command):
    def __init__(self, server, scheduler):
        self.scheduler = scheduler
        Command.__init__(self, server, admin_only=True, requires_patch=False)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err


class CommandStartTraderCommand(Command):
    def __init__(self, server, scheduler):
        self.scheduler = scheduler
        Command.__init__(self, server, admin_only=True, requires_patch=False)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err


class CommandStopTraderCommands(Command):
    def __init__(self, server, scheduler):
        self.scheduler = scheduler
        Command.__init__(self, server, admin_only=True, requires_patch=False)

    def execute(self, username, args, user_flags):
        err = self.execute_pretest(username, user_flags)
        if err: return err


