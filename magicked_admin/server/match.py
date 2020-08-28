import gettext
import time

from database import db_connector

_ = gettext.gettext


class Match:
    def __init__(self, level, game_type, difficulty, length):
        self.match_id = 0
        self.level = level
        self.game_type = game_type
        self.difficulty = difficulty
        self.length = length
        self._start_date = None  # Time doesnt start until wave 1

        self.wave = 0
        self.trader_time = False
        # Wave progress counter from top-right of admin panel
        self.zeds_dead = 0
        self.zeds_total = 0

        self.players = []

        self._init_db()

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
