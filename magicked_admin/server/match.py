import logging
import time

from database import db_connector
from PySide2.QtCore import Slot
from web_admin.constants import MatchUpdateData

logger = logging.getLogger(__name__)


class Match:
    def __init__(self, server, level, game_type, difficulty, length):
        self.server = server
        self.signals = server.signals
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

        self.signals.match_update.connect(self.receive_update_data)

    @db_connector
    def _init_db(self, conn):
        sql = """
            INSERT INTO match
                (level_id, game_type, difficulty, length, server_id)
            VALUES
                (?, ?, ?, ?, ?)
        """
        cur = conn.cursor()
        cur.execute(sql, (
            self.level.level_id, self.game_type, self.difficulty, self.length, self.server.server_id
        ))
        conn.commit()

        self.match_id = cur.lastrowid

    @Slot(MatchUpdateData)
    def receive_update_data(self, match_update_data):
        new_wave = match_update_data.wave > self.wave

        if match_update_data.trader_open and not self.trader_time:
            # Waves are considered over once the trader opens
            logger.info("Wave {} ended on {}".format(self.wave, self.server.name))
            self.signals.wave_end.emit(self)
            self.trader_time = True
            self.signals.trader_open.emit(self)

        if not match_update_data.trader_open and self.trader_time:
            # Wave start is further down so the new match data is available
            self.trader_time = False
            self.signals.trader_close.emit(self)

        if match_update_data.wave and not self.start_date:
            # Match starts at wave 1, wave 0 is lobby
            self.start_date = time.time()
            logger.info("New match on {}, map: {}, mode: {}".format(
                self.server.name, self.level.name, self.game_type)
            )
            self.signals.match_start.emit(self)

        self.wave = match_update_data.wave
        self.zeds_dead = match_update_data.zeds_dead
        self.zeds_total = match_update_data.zeds_total

        if new_wave:
            logger.info("Wave {} started on {}".format(self.wave, self.server.name))
            self.signals.wave_start.emit(self)

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
