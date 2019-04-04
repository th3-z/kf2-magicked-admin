import sqlite3
import datetime
from os import path
from threading import Lock

from utils import find_data_file, DEBUG

lock = Lock()


class ServerDatabase:

    def __init__(self, name):
        self.sqlite_db_file = find_data_file(name + "_db" + ".sqlite")

        if not path.exists(self.sqlite_db_file):
            self.build_schema()
        self.conn = sqlite3.connect(self.sqlite_db_file,
                                    check_same_thread=False)
        self.cur = self.conn.cursor()

        if DEBUG:
            print("Database for " + name + " initialised")

    def build_schema(self):
        print("Building new database...")

        conn = sqlite3.connect(self.sqlite_db_file)
        cur = conn.cursor()

        with open(find_data_file('database/server_schema.sql')) as schema_file:
            cur.executescript(schema_file.read())

        conn.commit()
        conn.close()

    def rank_kills(self, username):
        subquery = "SELECT count(*) FROM players AS player2 WHERE player2.kills >= player1.kills"
        query = "SELECT player1.*,({}) AS kill_rank FROM players AS player1 WHERE player1.username=?".format(subquery)
        lock.acquire(True)
        self.cur.execute(query, (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        return all_rows[0][-1]

    def rank_dosh(self, username):
        subquery = "SELECT count(*) FROM players as player2 WHERE player2.dosh >= player1.dosh"
        query = "SELECT  player1.*,({}) AS dosh_rank FROM  players AS player1 WHERE player1.username=?".format(subquery)
        lock.acquire(True)
        self.cur.execute(query, (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        return all_rows[0][-1]

    def rank_death(self, username):
        subquery = "SELECT count(*) FROM players as player2 WHERE player2.deaths <= player1.deaths"
        query = "SELECT player1.*,({}) AS death_rank FROM  players AS player1 WHERE player1.username=?".format(subquery)
        lock.acquire(True)
        self.cur.execute(query, (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        return all_rows[0][-1] + 1

    def rank_kd(self, username):
        subquery = "SELECT count(*) FROM players as p2 WHERE p2.kills / p2.deaths >= p1.kills / p1.deaths"
        query = "SELECT p1.*,({}) AS kd_rank FROM  players AS p1 WHERE player1.username=?".format(subquery)
        lock.acquire(True)
        self.cur.execute(query, (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        return all_rows[0][-1] + 1

    def rank_time(self, username):
        subquery = "SELECT count(*) FROM players as player2 WHERE player2.time_online >= player1.time_online"
        query = "SELECT player1.*,({}) AS time_rank  FROM  players AS player1 WHERE p1.username=?".format(subquery)
        lock.acquire(True)
        self.cur.execute(query, (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        return all_rows[0][-1] + 1

    # SUM(dosh_spent) Add in later.
    def server_dosh(self):
        lock.acquire(True)
        self.cur.execute('SELECT SUM(dosh) FROM players')
        all_rows = self.cur.fetchall()
        lock.release()
        # Errors out when you call it with 0 with "NoneType"
        if all_rows and all_rows[0][0]:
            return int(all_rows[0][0])
        else:
            return 0

    def server_kills(self):
        lock.acquire(True)
        self.cur.execute('SELECT SUM(kills) FROM players')
        all_rows = self.cur.fetchall()
        lock.release()
        # Errors out when you call it with 0 with "NoneType"
        if all_rows and all_rows[0][0]:
            return int(all_rows[0][0])
        else:
            return 0

    def top_kills(self):
        lock.acquire(True)
        self.cur.execute('SELECT username, kills FROM players ORDER BY kills DESC')
        all_rows = self.cur.fetchall()
        lock.release()
        return all_rows

    def top_dosh(self):
        lock.acquire(True)
        self.cur.execute('SELECT username, dosh FROM players ORDER BY dosh DESC')
        all_rows = self.cur.fetchall()
        lock.release()
        return all_rows

    def player_dosh(self, username):
        lock.acquire(True)
        self.cur.execute('SELECT (dosh) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_dosh_spent(self, username):
        lock.acquire(True)
        self.cur.execute('SELECT (dosh_spent) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_kills(self, username):
        lock.acquire(True)
        self.cur.execute('SELECT (kills) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_deaths(self, username):
        lock.acquire(True)
        self.cur.execute('SELECT (deaths) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_logins(self, username):
        lock.acquire(True)
        self.cur.execute('SELECT (logins) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_time(self, username):
        lock.acquire(True)
        self.cur.execute('SELECT (time_online) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_health_lost(self, username):
        lock.acquire(True)
        self.cur.execute('SELECT (health_lost) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        lock.release()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def load_player(self, player):
        # TODO id as parameter, return new player obj
        player.total_kills = self.player_kills(player.username)
        player.total_dosh = self.player_dosh(player.username)
        player.total_deaths = self.player_deaths(player.username)
        player.total_dosh_spent = self.player_dosh_spent(player.username)
        player.total_logins = self.player_logins(player.username)
        player.total_health_lost = self.player_health_lost(player.username)
        player.total_time = self.player_time(player.username)

    def save_player(self, player, final=False):
        lock.acquire(True)
        self.cur.execute("INSERT OR IGNORE INTO players (username) VALUES (?)",
                         (player.username,))

        self.cur.execute("UPDATE players SET dosh_spent = ? WHERE username = ?",
                         (player.total_dosh_spent, player.username))

        self.cur.execute("UPDATE players SET dosh = ? WHERE username = ?",
                         (player.total_dosh, player.username))
        self.cur.execute("UPDATE players SET kills = ? WHERE username = ?",
                         (player.total_kills, player.username))
        self.cur.execute("UPDATE players SET deaths = ? WHERE username = ?",
                         (player.total_deaths, player.username))
        self.cur.execute("UPDATE players SET health_lost = ? WHERE username = ?",
                         (player.total_health_lost, player.username))
        self.cur.execute("UPDATE players SET logins = ? WHERE username = ?",
                         (player.total_logins, player.username))
        lock.release()

        if final:
            now = datetime.datetime.now()
            elapsed_time = now - player.session_start
            seconds = elapsed_time.total_seconds()
            new_time = player.total_time + seconds

            lock.acquire(True)
            self.cur.execute("UPDATE players SET time_online = ? WHERE username = ?",
                             (new_time, player.username))
            lock.release()

        self.conn.commit()

    def save_game_map(self, game_map):
        lock.acquire(True)
        self.cur.execute("INSERT OR IGNORE INTO maps (name, title) VALUES (?, ?)",
                         (game_map.name, game_map.title))

        self.cur.execute("UPDATE maps SET plays_survival = ? WHERE name = ?",
                         (game_map.plays_survival, game_map.name))
        self.cur.execute("UPDATE maps SET plays_survival_vs = ? WHERE name = ?",
                         (game_map.plays_survival_vs, game_map.name))
        self.cur.execute("UPDATE maps SET plays_weekly = ? WHERE name = ?",
                         (game_map.plays_weekly, game_map.name))
        self.cur.execute("UPDATE maps SET plays_endless = ? WHERE name = ?",
                         (game_map.plays_endless, game_map.name))
        self.cur.execute("UPDATE maps SET highest_wave = ? WHERE name = ?",
                         (game_map.highest_wave, game_map.name))

        lock.release()

        self.conn.commit()

    def save_map_record(self, game, players):
        lock.acquire(True)
        self.cur.execute(
            "INSERT INTO map_records (map_name, game_time, game_length, game_difficulty, player_count) VALUES (?, ?, ?, ?, ?)",
            (game.game_map.name, game.time, game.length, game.difficulty,
             players))
        lock.release()
        self.conn.commit()

    def load_game_map(self, game_map):
        lock.acquire(True)

        self.cur.execute("INSERT OR IGNORE INTO maps (name, title) VALUES (?, ?)",
                         (game_map.name, game_map.title))

        # TODO: Change all of these into a single query that returns a list
        self.cur.execute('SELECT (plays_survival) FROM maps WHERE name=?',
                         (game_map.name,))
        plays_survival = int(self.cur.fetchall()[0][0])

        self.cur.execute('SELECT (plays_survival_vs) FROM maps WHERE name=?',
                         (game_map.name,))
        plays_survival_vs = int(self.cur.fetchall()[0][0])

        self.cur.execute('SELECT (plays_weekly) FROM maps WHERE name=?',
                         (game_map.name,))
        plays_weekly = int(self.cur.fetchall()[0][0])

        self.cur.execute('SELECT (plays_endless) FROM maps WHERE name=?',
                         (game_map.name,))
        plays_endless = int(self.cur.fetchall()[0][0])

        self.cur.execute('SELECT (plays_other) FROM maps WHERE name=?',
                         (game_map.name,))
        plays_other = int(self.cur.fetchall()[0][0])

        self.cur.execute('SELECT (highest_wave) FROM maps WHERE name=?',
                         (game_map.name,))
        highest_wave = int(self.cur.fetchall()[0][0])
        lock.release()

        game_map.plays_survival = plays_survival
        game_map.plays_survival_vs = plays_survival_vs
        game_map.plays_weekly = plays_weekly
        game_map.plays_endless = plays_endless
        game_map.plays_other = plays_other
        game_map.highest_wave = highest_wave

    def close(self):
        self.conn.commit()
        self.conn.close()
