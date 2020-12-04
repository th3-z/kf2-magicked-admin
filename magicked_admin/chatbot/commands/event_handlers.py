import gettext
import threading
import time

from chatbot.commands import ALL_WAVES
from PySide2.QtCore import Slot, QThread
from server.match import Match
from server.player import Player
from utils.time import seconds_to_hhmmss
from web_admin.constants import *

_ = gettext.gettext


class OnTimeHandler(QThread):
    def __init__(self, signals, command, interval, repeat=False):
        super(OnTimeHandler, self).__init__()

        self.signals = signals
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

            self.signals.command.emit(
                "command_on_time", self.command.split(" "), USER_TYPE_ADMIN
            )

            if not self.repeat:
                return

    def close(self):
        self.dead = True


class OnWaveHandler:
    def __init__(self, signals, command, wave=ALL_WAVES):
        self.signals = signals

        self.wave = wave
        self.command = command
        self.dead = False

        signals.wave_start.connect(self.receive_match)

    @Slot(Match)
    def receive_match(self, match):
        if self.dead:
            return

        # Translate negative input to positive, '-1' runs on boss wave
        length = match.length
        wave = (length + 1) + (self.wave + 1) if self.wave < 0 else self.wave

        if wave == match.wave or self.wave == ALL_WAVES:
            self.signals.command.emit(
                "command_on_wave", self.command.split(" "), USER_TYPE_ADMIN
            )

    def close(self):
        self.dead = True


class OnJoinHandler:
    def __init__(self, signals, command, returning=False):
        self.signals = signals

        self.returning = returning
        self.command = command
        self.dead = False

        signals.player_join.connect(self.receive_player)

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

    @Slot(Player)
    def receive_player(self, player):
        if self.dead:
            return

        if self.returning and not player.total_sessions:
            return

        command = self.resolve_tokens(player)

        self.signals.command.emit(
            "command_on_join", command.split(" "), USER_TYPE_ADMIN
        )

    def close(self):
        self.dead = True


class OnTraderHandler:
    def __init__(self, signals, command, wave=ALL_WAVES):
        self.signals = signals

        self.wave = wave
        self.command = command
        self.dead = False

        signals.trader_open.connect(self.receive_match)

    @Slot(Match)
    def receive_match(self, match):
        if self.dead:
            return

        # Translate negative input to positive, '-1' runs on boss wave
        length = match.length
        wave = (length + 1) + (self.wave + 1) if self.wave < 0 else self.wave

        if wave == match.wave or self.wave == ALL_WAVES:
            self.signals.command.emit(
                "command_on_trader", self.command.split(" "), USER_TYPE_ADMIN
            )

    def close(self):
        self.dead = True


class OnDeathHandler:
    def __init__(self, signals, command):
        self.signals = signals

        self.command = command
        self.dead = False

        signals.player_death.connect(self.receive_player)

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

    @Slot(Player)
    def receive_player(self, player):
        if self.dead:
            return

        command = self.resolve_tokens(player)

        self.signals.command.emit(
            "command_on_death", command.split(" "), USER_TYPE_ADMIN
        )

    def close(self):
        self.dead = True
