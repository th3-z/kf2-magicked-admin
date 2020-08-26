import gettext
import sqlite3
from os import path
from threading import Lock

from utils import find_data_file, info

_ = gettext.gettext
lock = Lock()


class ServerDatabase:

    def __init__(self, name):
        self.sqlite_db_file = find_data_file("conf/" + name + ".sqlite")

        if not path.exists(self.sqlite_db_file):
            self.build_schema()
        self.conn = sqlite3.connect(
            self.sqlite_db_file,
            check_same_thread=False,
            isolation_level=None
        )

        # Assemble rows into dicts (col->val) rather than tuples
        self.conn.row_factory = lambda c, r: \
            dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])

        self.cur = self.conn.cursor()

    def build_schema(self):
        info(_("Building new database..."))

        conn = sqlite3.connect(self.sqlite_db_file, isolation_level=None)
        cur = conn.cursor()

        with open(find_data_file('database/schema.sql')) as schema_file:
            lock.acquire(True)
            cur.executescript(schema_file.read())
            lock.release()

        conn.close()

    def close(self):
        self.conn.close()

    def __rank_by_col(self, steam_id, col):
        pass

    def rank_dosh(self, steam_id):
        pass

    def rank_kills(self, steam_id):
        pass

    def rank_time(self, steam_id):
        pass

    def rank_kd(self, steam_id):
        pass

    def __server_sum_col(self, col):
        query = """
            SELECT
                COALESCE(SUM({}), 0) as total
            FROM
                players
        """.format(col)

        lock.acquire(True)
        self.cur.execute(query)
        result = self.cur.fetchall()
        lock.release()

        if result:
            return result[0]["total"]
        return 0

    def server_kills(self):
        return self.__server_sum_col("kills")

    def server_dosh(self):
        return self.__server_sum_col("dosh")

    def server_time(self):
        return self.__server_sum_col("time")

    def __server_top_by_col(self, col):
        query = """
            SELECT
                username,
                {} as score
            FROM
                players
            ORDER BY
                {} DESC
        """.format(col, col)

        lock.acquire(True)
        self.cur.execute(query)
        result = self.cur.fetchall()
        lock.release()

        if result:
            return result
        return []

    def top_kills(self):
        return self.__server_top_by_col("kills")

    def top_dosh(self):
        return self.__server_top_by_col("dosh")

    def top_time(self):
        return self.__server_top_by_col("time_online")

    def __init_player(self, steam_id):
        pass


    def load_player(self, player, r_flag=False):
        pass

    def save_player(self, player):
        pass

    def __init_game_map(self, title):
        # Other columns have defaults in schema
        init_sql = """
            INSERT INTO maps(title)
            VALUES(?)
        """

        lock.acquire(True)
        self.cur.execute(init_sql, (title.upper(),))
        lock.release()

    def highest_wave(self, game_map):
        highest_wave_sql = """
            SELECT
                game_wave
            FROM
                map_records
            WHERE
                map_title = ?
            ORDER BY game_wave DESC
        """

        lock.acquire(True)
        self.cur.execute(highest_wave_sql, (game_map.title.upper(),))
        highest_wave_result = self.cur.fetchall()
        lock.release()

        if not highest_wave_result:
            return 0
        return highest_wave_result[0]['game_wave']

    def load_game_map(self, game_map, r_flag=False):
        map_sql = """
            SELECT
                name, plays_survival, plays_weekly, plays_endless,
                plays_survival_vs, plays_other, highest_wave
            FROM
                maps
            WHERE
                title = ?
        """

        lock.acquire(True)
        self.cur.execute(map_sql, (game_map.title.upper(),))
        map_result = self.cur.fetchall()
        lock.release()

        if len(map_result) != 1 and not r_flag:
            # Init map row and retry, never retry more than once
            self.__init_game_map(game_map.title.upper())
            self.load_game_map(game_map, True)
            return

        map_result = map_result[0]

        game_map.plays_survival = map_result['plays_survival']
        game_map.plays_survival_vs = map_result['plays_survival_vs']
        game_map.plays_weekly = map_result['plays_weekly']
        game_map.plays_endless = map_result['plays_endless']
        game_map.plays_other = map_result['plays_other']
        game_map.highest_wave = map_result['highest_wave']
        game_map.name = map_result['name']

    def save_game_map(self, game_map):
        save_query = """
            UPDATE maps SET
                name = ?,
                plays_survival = ?,
                plays_survival_vs = ?,
                plays_weekly = ?,
                plays_endless = ?,
                plays_other = ?,
                highest_wave = ?
            WHERE
                title = ?
        """

        lock.acquire(True)
        self.cur.execute(save_query,
                         (game_map.name, game_map.plays_survival,
                          game_map.plays_survival_vs, game_map.plays_weekly,
                          game_map.plays_endless, game_map.plays_other,
                          game_map.highest_wave, game_map.title.upper()))
        lock.release()

    def save_map_record(self, game, players, victory):
        save_query = """
            INSERT INTO map_records (
                map_title, game_time, game_length, game_difficulty,
                player_count, game_wave, game_victory
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?
            )
        """

        lock.acquire(True)
        self.cur.execute(save_query,
                         (game.game_map.title.upper(), game.time, game.length,
                          game.difficulty, players, game.wave,
                          int(victory)))
        lock.release()

    def execute(self):
        pass
