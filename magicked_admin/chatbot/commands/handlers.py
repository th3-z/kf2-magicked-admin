import gettext
import threading
import time

from chatbot.commands import ALL_WAVES
from utils.time import seconds_to_hhmmss
from web_admin.constants import *
from events import (
    EVENT_COMMAND, EVENT_WAVE_START, EVENT_PLAYER_JOIN, EVENT_TRADER_OPEN, EVENT_PLAYER_DEATH
)

_ = gettext.gettext


class OnTimeHandler(threading.Thread):
    def __init__(self, event_manager, command, interval, repeat=False):
        threading.Thread.__init__(self)

        self._event_manger = event_manager
        self._exit = False

        self.interval = interval
        self.repeat = repeat
        self.command = command
        self.dead = False

    def run(self):
        while True:
            time.sleep(self.interval)
            if self.dead:
                return

            self._event_manger.emit_event(
                EVENT_COMMAND, self.__class__,
                username="command_on_time",
                args=self.command.split(" "),
                user_flags=USER_TYPE_ADMIN
            )

            if not self.repeat:
                self.close()
                return

    def close(self):
        self.dead = True


class OnWaveHandler:
    def __init__(self, event_manager, command, wave=ALL_WAVES):
        self._event_manager = event_manager

        self.wave = wave
        self.command = command
        self.dead = False

        event_manager.register_event(EVENT_WAVE_START, self.receive_match)

    def receive_match(self, event, sender, match):
        if self.dead:
            return

        # Translate negative input to positive, '-1' runs on boss wave
        length = match.length
        wave = (length + 1) + (self.wave + 1) if self.wave < 0 else self.wave

        if wave == match.wave or self.wave == ALL_WAVES:
            self._event_manager.emit_event(
                EVENT_COMMAND, self.__class__,
                username="command_on_wave", args=self.command.split(" "),
                user_flags=USER_TYPE_ADMIN
            )

    def close(self):
        self.dead = True


class OnJoinHandler:
    def __init__(self, event_manager, command, returning=False):
        self._event_manager = event_manager

        self.returning = returning
        self.command = command
        self.dead = False

        event_manager.register_event(EVENT_PLAYER_JOIN, self.receive_player)

    def resolve_tokens(self, player):
        command = self.command
        command = command.replace("%PLR", player.username)
        command = command.replace("%DSH", str(player.total_dosh))
        command = command.replace("%DRK", str(player.rank_dosh))
        command = command.replace("%KLL", str(player.total_kills))
        command = command.replace("%KRK", str(player.rank_kills))
        command = command.replace("%TME", seconds_to_hhmmss(player.total_time))
        command = command.replace("%TRK", str(player.rank_time))
        command = command.replace("%SES", str(player.total_sessions))

        return command

    def receive_player(self, event, sender, player):
        if self.dead:
            return

        if self.returning and not player.total_sessions:
            return

        command = self.resolve_tokens(player)

        self._event_manager.emit_event(
            EVENT_COMMAND, self.__class__,
            username="command_on_join", args=command.split(" "),
            user_flags=USER_TYPE_ADMIN
        )

    def close(self):
        self.dead = True


class OnTraderHandler:
    def __init__(self, event_manager, command, wave=ALL_WAVES):
        self._event_manager = event_manager

        self.wave = wave
        self.command = command
        self.dead = False

        event_manager.register_event(EVENT_TRADER_OPEN, self.receive_match)

    def receive_match(self, event, sender, match):
        if self.dead:
            return

        # Translate negative input to positive, '-1' runs on boss wave
        length = match.length
        wave = (length + 1) + (self.wave + 1) if self.wave < 0 else self.wave

        if wave == match.wave or self.wave == ALL_WAVES:
            self._event_manager.emit_event(
                EVENT_COMMAND, self.__class__,
                username="command_on_trader", args=self.command.split(" "),
                user_flags=USER_TYPE_ADMIN
            )

    def close(self):
        self.dead = True


class OnDeathHandler:
    def __init__(self, event_manager, command):
        self._event_manager = event_manager

        self.command = command
        self.dead = False

        event_manager.register_event(EVENT_PLAYER_DEATH, self.receive_player)

    def resolve_tokens(self, player):
        # TODO: Use string format instead
        command = self.command
        command = command.replace("%PLR", player.username)
        command = command.replace("%DSH", str(player.total_dosh))
        command = command.replace("%DRK", str(player.rank_dosh))
        command = command.replace("%KLL", str(player.total_kills))
        command = command.replace("%KRK", str(player.rank_kills))
        command = command.replace("%TME", seconds_to_hhmmss(player.total_time))
        command = command.replace("%TRK", str(player.rank_time))
        command = command.replace("%SES", str(player.total_sessions))

        return command

    def receive_player(self, event, sender, player):
        if self.dead:
            return

        command = self.resolve_tokens(player)

        self._event_manager.emit_event(
            EVENT_COMMAND, self.__class__,
            username="command_on_death", args=command.split(" "),
            user_flags=USER_TYPE_ADMIN
        )

    def close(self):
        self.dead = True
