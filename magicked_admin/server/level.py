from database import db_connector
from web_admin.constants import *


# 'Map' Conflicts with Python keyword
class Level:
    def __init__(self, title, name):
        self.level_id = 0
        # e.g. Black Forest
        self.name = name
        # e.g. KF-BlackForest
        self.title = title

        # TODO
        # self.plays_survival
        # self.plays_endless
        # self.plays_objective
        # self.total_kills
        # self.total_dosh

        self._init_db()

        print(self)

    @db_connector
    def _init_db(self, conn):
        sql = """
            INSERT OR IGNORE INTO level
                (title, name)
            VALUES
                (?, ?)
        """
        cur = conn.cursor()
        cur.execute(sql, (self.title, self.name))
        conn.commit()

        sql = """
            SELECT
                level_id
            FROM
                level
            WHERE
                title = ?
        """
        cur.execute(sql, (self.title,))
        result, = cur.fetchall()
        self.level_id = result['level_id']

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
        """

        cur = conn.cursor()
        cur.execute(sql, (self.title,))
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
                AND m.start_date IS NOT NULL
        """

        cur = conn.cursor()
        cur.execute(sql, (game_type,))
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
                m.start_date IS NOT NULL
        """

        cur = conn.cursor()
        cur.execute(sql)
        result, = cur.fetchall()

        return result['count']

    def __str__(self):
        return """
            title: {}
            name: {}
            plays survival: {}
            plays total: {}
        """.format(self.title, self.name, self.game_type_matches(GAME_TYPE_SURVIVAL), self.total_matches)