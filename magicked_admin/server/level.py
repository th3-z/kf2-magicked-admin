from database import db_connector


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
        # self.highest_wave

        self._init_db()

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
