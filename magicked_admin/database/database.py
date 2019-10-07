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
        self.conn = sqlite3.connect(self.sqlite_db_file,
                                    check_same_thread=False)

        # Assemble rows into dicts (col->val) rather than tuples
        self.conn.row_factory = lambda c, r: \
            dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])

        self.cur = self.conn.cursor()

    def build_schema(self):
        info(_("Building new database..."))

        conn = sqlite3.connect(self.sqlite_db_file)
        cur = conn.cursor()

        with open(find_data_file('database/schema.sql')) as schema_file:
            lock.acquire(True)
            cur.executescript(schema_file.read())
            lock.release()

        conn.commit()
        conn.close()

    def close(self):
        self.conn.commit()
        self.conn.close()

    def __rank_by_col(self, steam_id, col):
        query = """
            SELECT
                player1.*,
                COALESCE((
                    SELECT
                        count(*)
                    FROM
                        players as player2
                    WHERE
                        player2.? >= player1.?
                ), 0) AS col_rank
            FROM
                players AS player1
            WHERE
                player1.steam_id = ?
        """

        lock.acquire(True)
        self.cur.execute(query, (col, col, steam_id,))
        result = self.cur.fetchall()
        lock.release()

        if len(result):
            return result[0]["col_rank"]
        else:
            return None

    def rank_dosh(self, steam_id):
        return self.__rank_by_col(steam_id, "dosh")

    def rank_kills(self, steam_id):
        return self.__rank_by_col(steam_id, "kills")

    def rank_time(self, steam_id):
        return self.__rank_by_col(steam_id, "time_online")

    def rank_kd(self, steam_id):
        query = """
            SELECT
                player1.*,
                (
                    SELECT
                        count(*)
                    FROM
                        players as player2
                    WHERE
                        (player2.kills/player2.deaths)
                        >= (player1.kills/player1.deaths)
                ) AS kd_rank
            FROM
                players AS player1
            WHERE
                player1.steam_id = ?
        """

        lock.acquire(True)
        self.cur.execute(query, (steam_id,))
        result = self.cur.fetchall()
        lock.release()

        if len(result):
            return result[0]["kd_rank"]
        else:
            return None

    def __server_sum_col(self, col):
        query = """
            SELECT
                COALESCE(SUM(?), 0) as total
            FROM
                players
        """

        lock.acquire(True)
        self.cur.execute(query, (col,))
        result = self.cur.fetchall()
        lock.release()

        if result:
            return result[0]["total"]
        else:
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
                ? AS score
            FROM
                players
            ORDER BY
                ? DESC
        """

        lock.acquire(True)
        self.cur.execute(query, (col, col,))
        result = self.cur.fetchall()
        lock.release()

        if len(result):
            return result
        else:
            return []

    def top_kills(self):
        return self.__server_top_by_col("kills")

    def top_dosh(self):
        return self.__server_top_by_col("dosh")

    def top_time(self):
        return self.__server_top_by_col("time_online")

    def __init_player(self, steam_id):
        # Other columns have defaults in schema
        init_sql = """
            INSERT INTO players(steam_id)
            VALUES(?)
        """

        lock.acquire(True)
        self.cur.execute(init_sql, (steam_id,))
        self.conn.commit()
        lock.release()

    def load_player(self, player, r_flag=False):
        if not player.steam_id:
            return

        player_sql = """
            SELECT
                username, kills, dosh, deaths, sessions, time_online, op
            FROM
                players
            WHERE
                steam_id = ?
        """

        lock.acquire(True)
        self.cur.execute(player_sql, (player.steam_id,))
        player_result = self.cur.fetchall()
        lock.release()

        if len(player_result) != 1 and not r_flag:
            # Init player row and retry, never retry more than once
            self.__init_player(player.steam_id)
            self.load_player(player, True)
            return

        player_result = player_result[0]
        player.total_kills = player_result['kills']
        player.total_dosh = player_result['dosh']
        player.total_deaths = player_result['deaths']
        player.sessions = player_result['sessions']
        player.total_time = player_result['time_online']
        player.op = player_result['op']

    def save_player(self, player):
        save_sql = """
            UPDATE players SET
                username = ?,
                kills = ?,
                dosh = ?,
                deaths = ?,
                sessions = ?,
                time_online = ?,
                op = ?
            WHERE
                steam_id = ?
        """

        lock.acquire(True)
        self.cur.execute(save_sql,
                         (player.username, player.total_kills,
                          player.total_dosh, player.total_deaths,
                          player.sessions, player.total_time, player.op,
                          player.steam_id))
        lock.release()
        self.conn.commit()

    def __init_game_map(self, title):
        # Other columns have defaults in schema
        init_sql = """
            INSERT INTO maps(title)
            VALUES(?)
        """

        lock.acquire(True)
        self.cur.execute(init_sql, (title.upper(),))
        lock.release()
        self.conn.commit()

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

        if not len(highest_wave_result):
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
        self.conn.commit()

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
        self.conn.commit()
