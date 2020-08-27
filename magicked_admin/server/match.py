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
        self.start_date = None  # Time doesnt start until wave 1

        self.wave = 0
        self.trader_time = False
        # Wave progress counter from top-right of admin panel
        self.zeds_dead = 0
        self.zeds_total = 0

        self.players = []

        # @prop sum of sessions attached to this
        # self.zeds_killed = 0
        self.dosh_wave_earned = 0
        # @prop
        self.dosh_earned = 0

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


