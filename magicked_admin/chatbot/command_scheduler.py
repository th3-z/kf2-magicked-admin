import threading
import time

from chatbot.commands.command import Command
from utils import debug
from utils.text import millify
from utils.time import seconds_to_hhmmss
from web_admin.constants import *
from web_admin.chat import ChatListener
from utils.text import pad_output

ALL_WAVES = 999


class CommandScheduler(ChatListener):

    def __init__(self, server, chatbot):
        self.server = server
        self.chatbot = chatbot

        self.scheduled_commands = []

    def schedule_command(self, command):
        self.scheduled_commands.append(command)

    def unschedule_commands(self, command_type=None):
        for command in self.scheduled_commands:
            if command.__class__.__name__ == command_type or not command_type:
                self.scheduled_commands.remove(command)

    def receive_message(self, username, message, user_flags):
        if not user_flags & USER_TYPE_INTERNAL:
            return
        
        for command in self.scheduled_commands:
            if command.event_check(self.server, message):
                self.run_command(command)

    def poll(self):
        for command in self.scheduled_commands:
            if command.event_check(self.server, message=None):
                self.run_command(command)

    def run_command(self, command):
        self.chatbot.handle_command(
            "internal", command.command, USER_TYPE_INTERNAL
        )

        if command.run_once:
            self.scheduled_commands.remove(command)
        else:
            command.reset()


class ScheduledCommand(Command):

    def __init__(self, command, run_once=False):
        self.command = command
        self.run_once = run_once

    def event_check(self, server, message):
        raise NotImplemented("event_check() must be implemented")

    def reset(self):
        pass


class CommandOnTime(ScheduledCommand):

    def __init__(self, command, interval, run_once=False):
        ScheduledCommand.__init__(self, command, run_once)

        self.interval = interval
        self.last_run = time.time()

    def event_check(self, server, message):
        time_now = time.time()
        return (time_now - self.last_run) > self.interval

    def reset(self):
        self.last_run = time.time()


class CommandOnWave(ScheduledCommand):

    def __init__(self, command, wave, run_once=False):
        ScheduledCommand.__init__(command, run_once)

        self.wave = wave

    def event_check(self, server, message):
        if not message:
            return False

        length = server.game.length
        wave = (length + 1) + (self.wave + 1) if self.wave < 0 else self.wave

        message = message.split()
        
        if message[0] == "new_wave":
            new_wave = message[1]

            if new_wave == wave:
                return True
        
        return False


class CommandOnJoin(ScheduledCommand):

    def __init__(self, command):
        ScheduledCommand.__init__(command)

    def event_check(self, server, message):
        if not message:
            return False

        message = message.split()

        if message[0] == "player_join":
            # TODO Use steam id
            username = message[1]

            self.commmand.replace("%PLR%", username)

            return True

        return False


class CommandOnTrader(ScheduledCommand):

    def __init__(self, command):
        ScheduledCommand.__init__(command)

    def event_check(self, server, message):
        if not message:
            return False

        message = message.split()

        if message[0] == "t_open":
            return True

        return False

