from database import db_connector
from web_admin.constants import *


# 'Map' Conflicts with Python keyword
class Level:
    def __init__(self, title, name, server):
        self.level_id = 0
        # e.g. Black Forest
        self.name = name
        # e.g. KF-BlackForest
        self.title = title

        self.server = server

        # self.total_kills
        # self.total_dosh

        self._init_db()

    @db_connector
    def _init_db(self, conn):
        sql = """
            INSERT OR IGNORE INTO level
                (title, name, server_id)
            VALUES
                (?, ?, ?)
        """
        cur = conn.cursor()
        cur.execute(sql, (self.title, self.name, self.server.server_id))
        conn.commit()

        sql = """
            SELECT
                level_id, name
            FROM
                level
            WHERE
                title = ?
                and server_id = ?
        """
        cur.execute(sql, (self.title, self.server.server_id))
        result, = cur.fetchall()
        self.level_id = result['level_id']
        self.name = result['name']

    @property
    def plays_survival(self):
        return self.plays_game_type(GAME_TYPE_SURVIVAL)

    @property
    def plays_weekly(self):
        return self.plays_game_type(GAME_TYPE_WEEKLY)

    @property
    def plays_endless(self):
        return self.plays_game_type(GAME_TYPE_ENDLESS)

    @property
    def plays_survival_vs(self):
        return self.plays_game_type(GAME_TYPE_SURVIVAL_VS)

    @property
    def plays_other(self):
        return 0  # TODO: ?

    @db_connector
    def plays_game_type(self, game_type, conn):
        sql = """
            SELECT
                COUNT(*) AS plays
            FROM
                level l
                INNER JOIN match m ON
                    m.level_id = ?
            WHERE
                m.game_type = ?
        """

        cur = conn.cursor()
        cur.execute(sql, (self.level_id, game_type))
        result, = cur.fetchall()

        return result['plays']

    @property
    @db_connector
    def highest_wave(self, conn):
        sql = """
            SELECT
                MAX(m.last_wave) AS highest_wave
            FROM
                level l
                INNER JOIN match m ON
                    m.level_id = l.level_id
            WHERE
                l.title = ?
                and l.server_id = ?
        """

        cur = conn.cursor()
        cur.execute(sql, (self.title, self.server.server_id))
        result, = cur.fetchall()

        return result['highest_wave']

    @db_connector
    def game_type_matches(self, game_type, conn):
        sql = """
            SELECT
                COUNT(*) AS count
            FROM
                level l
                INNER JOIN match m
                    ON l.level_id = m.level_id
            WHERE
                m.game_type = ?
                AND m.server_id = ?
                AND m.start_date IS NOT NULL
        """

        cur = conn.cursor()
        cur.execute(sql, (game_type, self.server.server_id))
        result, = cur.fetchall()

        return result['count']

    @property
    @db_connector
    def total_matches(self, conn):
        sql = """
            SELECT
                COUNT(*) AS count
            FROM
                level l
                INNER JOIN match m
                    ON l.level_id = m.level_id
            WHERE
                l.server_id = ?
                m.start_date IS NOT NULL
        """

        cur = conn.cursor()
        cur.execute(sql, (self.server.server_id,))
        result, = cur.fetchall()

        return result['count']
