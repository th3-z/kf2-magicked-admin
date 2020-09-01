import gettext
import time

from database import db_connector
from utils import warning, BANNER_URL

from events import (
    EVENT_MATCH_UPDATE, EVENT_WAVE_START, EVENT_WAVE_END, EVENT_TRADER_OPEN,
    EVENT_TRADER_CLOSE, EVENT_MATCH_START
)

from colorama import init
from termcolor import colored

init()

_ = gettext.gettext


class Match:
    def __init__(self, server, level, game_type, difficulty, length):
        self.server = server
        self.match_id = 0
        self.level = level
        self.game_type = game_type
        self.difficulty = difficulty
        self.length = length
        self._start_date = None  # Time doesnt start until wave 1

        self.wave = 0
        self.trader_time = False
        # self.in_lobby
        # Wave progress counter from top-right of admin panel
        self.zeds_dead = 0
        self.zeds_total = 0

        self._init_db()

        server.event_manager.register_event(
            EVENT_MATCH_UPDATE, self.receive_update_data
        )

    @db_connector
    def _init_db(self, conn):
        sql = """
            INSERT INTO match
                (level_id, game_type, difficulty, length)
            VALUES
                (?, ?, ?, ?)
        """
        cur = conn.cursor()
        cur.execute(sql, (
            self.level.level_id, self.game_type, self.difficulty, self.length
        ))
        conn.commit()

        self.match_id = cur.lastrowid

    def receive_update_data(self, event, sender, match_update_data):
        new_wave = match_update_data.wave > self.wave

        if match_update_data.trader_open and not self.trader_time:
            # Waves are considered over once the trader opens
            self.server.event_manager.emit_event(
                EVENT_WAVE_END, self.__class__, match=self
            )
            self.trader_time = True
            self.server.event_manager.emit_event(
                EVENT_TRADER_OPEN, self.__class__, match=self
            )

        if not match_update_data.trader_open and self.trader_time:
            # Wave start is further down so the new match data is available
            self.trader_time = False
            self.server.event_manager.emit_event(
                EVENT_TRADER_CLOSE, self.__class__, match=self
            )

        if match_update_data.wave and not self.start_date:
            # Match starts at wave 1, wave 0 is lobby
            self.start_date = time.time()
            self.server.event_manager.emit_event(
                EVENT_MATCH_START, self.__class__, match=self
            )

        self.wave = match_update_data.wave
        self.zeds_dead = match_update_data.zeds_dead
        self.zeds_total = match_update_data.zeds_total

        if new_wave:
            self.server.event_manager.emit_event(
                EVENT_WAVE_START, self.__class__, match=self
            )

    @property
    def in_lobby(self):
        return bool(self._start_date)

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    @db_connector
    def start_date(self, start_date, conn):
        self._start_date = start_date

        sql = """
            UPDATE match SET
                start_date = ?
            WHERE
                match_id = ?
        """

        conn.cursor().execute(sql, (start_date, self.match_id))

    @db_connector
    def close(self, conn):
        sql = """
            UPDATE match SET
                end_date = ?,
                last_wave = ?
            WHERE
                match_id = ?
        """

        conn.cursor().execute(sql, (time.time(), self.wave, self.match_id))
