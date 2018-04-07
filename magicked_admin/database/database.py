import sqlite3
import datetime
from os import path

class ServerDatabase:

    def __init__(self, name):
        self.sqlite_db_file = name + "_db" + ".sqlite"

        if not path.exists(self.sqlite_db_file):
            self.build_schema()
        self.conn = sqlite3.connect(self.sqlite_db_file, check_same_thread = False)
        self.cur = self.conn.cursor()

        print("INFO: Database for " + name + " initialised")

    def build_schema(self):
        print("INFO: Building fresh schema...")

        conn = sqlite3.connect(self.sqlite_db_file)
        cur = conn.cursor()

        with open('database/server_schema.sql') as schema_file:
            cur.executescript(schema_file.read())

        conn.commit()
        conn.close()

    def start_session(self, player):
        pass

    def end_session(self, player):
        pass

    def end_game(self, game):
        pass

    # SUM(dosh_spent) Add in later.
    def server_dosh(self):
        self.cur.execute('SELECT SUM(dosh) FROM players')
        all_rows = self.cur.fetchall()
        # Errors out when you call it with 0 with "NoneType"
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def server_kills(self):
        self.cur.execute('SELECT SUM(kills) FROM players')
        all_rows = self.cur.fetchall()
        # Errors out when you call it with 0 with "NoneType"
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def top_kills(self):
        self.cur.execute('SELECT username, kills FROM players ORDER BY kills DESC')
        all_rows = self.cur.fetchall()
        return all_rows

    def top_dosh(self):
        self.cur.execute('SELECT username, dosh FROM players ORDER BY dosh DESC')
        all_rows = self.cur.fetchall()
        return all_rows

    def player_dosh(self, username):
        self.cur.execute('SELECT (dosh) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_dosh_spent(self, username):
        self.cur.execute('SELECT (dosh_spent) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_kills(self, username):
        self.cur.execute('SELECT (kills) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_deaths(self, username):
        self.cur.execute('SELECT (deaths) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_logins(self, username):
        self.cur.execute('SELECT (logins) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_time(self, username):
        self.cur.execute('SELECT (time_online) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def player_health_lost(self, username):
        self.cur.execute('SELECT (health_lost) FROM players WHERE username=?',
                         (username,))
        all_rows = self.cur.fetchall()
        if all_rows:
            return int(all_rows[0][0])
        else:
            return 0

    def load_player(self, player):
        player.total_kills = self.player_kills(player.username)
        player.total_dosh =  self.player_dosh(player.username)
        player.total_deaths = self.player_deaths(player.username)
        player.total_dosh_spent = self.player_dosh_spent(player.username)
        player.total_logins = self.player_logins(player.username)
        player.total_health_lost = self.player_health_lost(player.username)
        player.total_time = self.player_time(player.username)

    def save_player(self, player, final=False):
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

        if final:
            now = datetime.datetime.now()
            elapsed_time = now - player.session_start
            seconds = elapsed_time.total_seconds()
            new_time = player.total_time + seconds

            self.cur.execute("UPDATE players SET time_online = ? WHERE username = ?",
                             (new_time, player.username))

        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()
