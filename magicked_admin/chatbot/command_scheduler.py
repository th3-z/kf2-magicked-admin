import gettext
import threading
import time

from chatbot.commands.command import Command
from chatbot.commands import ALL_WAVES
from utils import warning
from utils.time import seconds_to_hhmmss
from web_admin.chat import ChatListener
from web_admin.constants import *

_ = gettext.gettext


class CommandSchedulerPollThread(threading.Thread):
    def __init__(self, scheduler, poll_interval):
        threading.Thread.__init__(self)

        self.__exit = False
        self.scheduler = scheduler
        self.poll_interval = poll_interval

    def run(self):
        while not self.__exit:
            time.sleep(self.poll_interval)  # Goodnight
            self.scheduler.poll()

    def stop(self):
        self.__exit = True


class CommandScheduler(ChatListener):
    def __init__(self, server, chatbot):
        self.server = server
        self.chatbot = chatbot

        self.scheduled_commands = []
        self.poll_interval = 1

        self.poller = CommandSchedulerPollThread(self, self.poll_interval)
        self.poller.start()

    def stop(self):
        self.poller.stop()

    def schedule_command(self, command):
        self.scheduled_commands.append(command)

    def unschedule_commands(self, command_type):
        stopped = 0

        for command in self.scheduled_commands:
            if command.__class__.__name__ == command_type.__name__:
                self.scheduled_commands.remove(command)
                stopped += 1

        if stopped:
            message = _("Stopped {} command(s)").format(stopped)
            return message

        return _("None running")

    def receive_message(self, username, message, user_flags):
        """
        Runs commands that run that respond to a internal event message
        """
        if not user_flags & USER_TYPE_INTERNAL:
            return

        if message[0] == '!':
            message = message[1:]
        else:
            return

        for command in self.scheduled_commands:
            if command.event_check(self.server, message):
                self.run_command(command, message)

    def poll(self):
        """
        Runs commands that run at intervals or otherwise bypass messaging
        Executor: CommandSchedulerPollThread
        """
        for command in self.scheduled_commands:
            if command.poll and command.event_check(self.server, message=None):
                self.run_command(command)

    def run_command(self, command, internal_message=None):
        command_resolved = command.resolve_command(internal_message)
        self.chatbot.command_handler(
            "internal", command_resolved.split(" "), USER_TYPE_INTERNAL
        )

        # TODO: Bug, shouldn't have to check command in commands
        if command.run_once and command in self.scheduled_commands:
            self.scheduled_commands.remove(command)
        else:
            command.reset()


class ScheduledCommand(Command):
    def __init__(self, server, command, run_once=False, poll=False):
        Command.__init__(self, server, admin_only=True, requires_patch=False)
        self.command = command
        self.run_once = run_once
        self.poll = poll

    def execute(self, username, args, user_flags):
        warning(
            _("Scheduled command ({}) ran directly by {}, please use "
              "CommandScheduler").format(
                " ".join(args),
                username
            )
        )

    def event_check(self, server, message):
        """
        Should return True if required conditions for execution are met
        """
        raise NotImplementedError("event_check() must be implemented")

    def reset(self):
        """
        Implement to define some action after the command has been executed
        """

    def resolve_command(self, internal_message):
        """
        Override to rewrite command before submission, e.g. token resolution
        """
        return self.command


class CommandOnTime(ScheduledCommand):
    def __init__(self, server, command, interval, run_once=False):
        ScheduledCommand.__init__(self, server, command, run_once, poll=True)

        self.interval = interval
        self.last_run = time.time()

    def event_check(self, server, message):
        time_now = time.time()
        return (time_now - self.last_run) > self.interval

    def reset(self):
        self.last_run = time.time()


class CommandOnWave(ScheduledCommand):
    def __init__(self, server, command, wave, run_once=False):
        ScheduledCommand.__init__(self, server, command, run_once)

        self.wave = wave

    def event_check(self, server, message):
        if not message:
            return False

        # Translate negative input to positive, '-1' runs on boss wave
        length = server.match.length
        wave = (length + 1) + (self.wave + 1) if self.wave < 0 else self.wave

        message = message.split()

        if message[0] == "new_wave":
            if wave == ALL_WAVES:
                return True

            new_wave = message[1]
            if int(new_wave) == wave:
                return True

        return False


class CommandOnJoin(ScheduledCommand):
    def __init__(self, server, command, returning=False):
        ScheduledCommand.__init__(self, server, command)
        self.returning = returning

    def event_check(self, server, message):
        if not message:
            return False

        args = message.split()
        if args[0] == "player_join":

            if self.returning:
                username = message.split(" ", 1)[1]
                player = self.server.get_player_by_username(username)
                return player.total_sessions > 1
            return True
        return False

    def resolve_command(self, internal_message):
        command = self.command
        username = internal_message.split(" ", 1)[1]

        if "%PLR" in self.command:
            player = self.server.get_player_by_username(username)
            pos_kills = player.rank_kills
            pos_dosh = player.rank_dosh
            pos_time = player.rank_time

            command = command.replace("%PLR", player.username)
            command = command.replace(
                "%BCK", "back" if player.total_sessions > 1 else ""
            )

            command = command.replace("%DSH", str(player.total_dosh))
            command = command.replace("%DRK", str(pos_dosh))

            command = command.replace("%KLL", str(player.total_kills))
            command = command.replace("%KRK", str(pos_kills))

            command = command.replace(
                "%TME", seconds_to_hhmmss(player.total_time)
            )
            command = command.replace("%TRK", str(pos_time))
            command = command.replace("%SES", str(player.total_sessions))

        return command


class CommandOnTrader(ScheduledCommand):
    def __init__(self, server, command, wave=ALL_WAVES):
        ScheduledCommand.__init__(self, server, command)

        self.wave = wave

    def event_check(self, server, message):
        if not message:
            return False

        args = message.split()

        # Translate negative input to positive, '-1' runs on boss wave
        length = server.match.length if server.match else 0
        wave = (length + 1) + (self.wave + 1) if self.wave < 0 else self.wave

        if args[0] == "t_open":
            new_wave = int(args[1])
            if self.wave != ALL_WAVES and new_wave != wave:
                return False
            return True
        return False
