import gettext
import time

from database import db_connector

_ = gettext.gettext


class Player:

    def __init__(self, steam_id):
        self.steam_id = steam_id
        self.player_key = None
        self.session_id = None
        self.session_date = time.time()
        self.join_date = None
        self.op = False

        self.username = "the_z"
        self.perk = None
        self.perk_level = 99

        self.ip = None
        self.country = _("Unknown")
        self.country_code = "??"

        # Current
        self.dosh = None
        self.kills = None
        self.health = None
        self.ping = None

        # Session (game)
        self.session_dosh = None
        self.session_dosh_spent = None
        self.session_kills = None
        self.session_deaths = None
        self.session_damage_taken = None
        # self.session_time

        # Wave
        self.wave_dosh = None
        self.wave_dosh_spent = None
        self.wave_kills = None
        self.wave_deaths = None
        self.wave_damage_taken = None

        # Totals
        # self.total_dosh
        # self.total_dosh_spent
        # self.total_kills
        # self.total_deaths
        # self.total_damage_taken
        # self.total_time
        # self.total_sessions

        self._db_init()

    @db_connector
    def _db_init(self, conn):
        sql = """
            INSERT OR IGNORE INTO players
                (steam_id, insert_date)
            VALUES
                (?, ?)
        """
        cur = conn.cursor()
        cur.execute(sql, (self.steam_id, time.time()))
        conn.commit()

        sql = """
            SELECT
                op, insert_date
            FROM
                players
            WHERE
                steam_id = ?
        """
        cur.execute(sql, (self.steam_id,))
        result, = cur.fetchall()
        self.op = True if result['op'] else False
        self.join_date = result['insert_date']

    @db_connector
    def _historic_session_sum(self, conn, col):
        sql = """
            SELECT
                SUM(s.{}) AS {}
            FROM
                players p
                LEFT JOIN session s
                    ON s.steam_id = p.steam_id
            WHERE
                p.steam_id = ?
                AND s.end_date IS NOT NULL
        """.format(col, col)
        cur = conn.cursor()
        cur.execute(sql, (self.steam_id,))
        result, = cur.fetchall()

        return result[col]

    @db_connector
    def update_session(self, conn):
        sql = """
            UPDATE session SET
                kills = ?,
                deaths = ?,
                dosh = ?,
                dosh_spent = ?,
                damage_taken = ?
            WHERE
                session_id = ?
        """

        conn.cursor().execute(sql, (
                self.session_kills, self.session_deaths,
                self.session_dosh, self.session_dosh_spent,
                self.session_damage_taken,
                self.session_id
            )
        )

    @db_connector
    def op(self, conn, state):
        sql = """
            UPDATE players SET
                op = ?
            WHERE
                steam_id = ?
        """

        conn.cursor().execute(sql, (1 if state else 0, self.steam_id))

    @property
    def total_kills(self):
        return self._historic_session_sum("kills") + self.session_kills

    @property
    def total_dosh(self):
        return self._historic_session_sum("dosh") + self.session_dosh

    @property
    def total_dosh_spent(self):
        return self._historic_session_sum("dosh_spent")\
               + self.session_dosh_spent

    @property
    def total_deaths(self):
        return self._historic_session_sum("deaths") + self.session_deaths

    @property
    def total_damage_taken(self):
        return self._historic_session_sum("damage_taken") \
            + self.session_damage_taken

    @property
    @db_connector
    def total_sessions(self, conn):
        sql = """
            SELECT
                COUNT(session_id) AS sessions
            FROM
                session
            WHERE
                steam_id = ?
        """
        cur = conn.cursor()
        cur.execute(sql, (self.steam_id,))
        result, = cur.fetchall()

        return result['sessions']

    @property
    @db_connector
    def total_time(self, conn):
        sql = """
            SELECT
                SUM(end_date - start_date) AS time
            FROM
                session
            WHERE
                steam_id = ?
                end_date IS NOT NULL
        """

        cur = conn.cursor()
        cur.execute(sql, (self.steam_id,))
        result, = cur.fetchall()

        return result['time'] + self.session_time

    @property
    def session_time(self):
        return time.time() - self.session_date

    @db_connector
    def reset_stats(self, conn):
        sql = """
            DELETE FROM session
            WHERE
                steam_id = ?
        """
        conn.cur.execute(sql)

    def __str__(self):
        return _("Username: {}\nCountry: {} ({})\nOP: {}\nSteam ID:{}").format(
            self.username, self.country, self.ip, self.op, self.steam_id
        )
