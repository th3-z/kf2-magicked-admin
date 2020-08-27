import gettext
import time

from database import db_connector

_ = gettext.gettext


class Player:

    def __init__(self, steam_id, username):
        self.steam_id = steam_id
        self.player_key = None
        self.session_id = None
        self.session_date = int(time.time())
        self.join_date = None
        self.op = False

        self.username = username
        self.perk = "Unknown"
        self.perk_level = 0

        self.ip = "0.0.0.0"
        self.country = _("Unknown")
        self.country_code = "??"

        # Current
        self.dosh = 0
        self.kills = 0
        self.health = 0
        self.ping = 0

        # Session (game)
        self.session_dosh = 0
        self.session_dosh_spent = 0
        self.session_kills = 0
        self.session_deaths = 0
        self.session_damage_taken = 0
        # self.session_time

        # Wave
        self.wave_dosh = 0
        self.wave_dosh_spent = 0
        self.wave_kills = 0
        self.wave_deaths = 0
        self.wave_damage_taken = 0

        # Totals
        # self.total_dosh
        # self.total_dosh_spent
        # self.total_kills
        # self.total_deaths
        # self.total_damage_taken
        # self.total_time
        # self.total_sessions

        # Ranks
        # self.rank_dosh
        # self.rank_dosh_spent
        # self.rank_kills
        # self.rank_deaths
        # self.rank_damage_taken
        # self.rank_time
        # self.rank_sessions

        # Ratios
        # self.ratio_dosh_deaths
        # self.rank_ratio_dosh_deaths
        # self.ratio_kills_deaths
        # self.rank_ratio_kills_deaths

        self._db_init()

    @db_connector
    def _db_init(self, conn):
        sql = """
            INSERT OR IGNORE INTO player
                (steam_id, insert_date, username)
            VALUES
                (?, ?, ?)
        """
        cur = conn.cursor()
        cur.execute(sql, (self.steam_id, int(time.time()), self.username))
        conn.commit()

        sql = """
            SELECT
                op, insert_date, username
            FROM
                player
            WHERE
                steam_id = ?
        """
        cur.execute(sql, (self.steam_id,))
        result, = cur.fetchall()
        self.op = True if result['op'] else False
        self.join_date = result['insert_date']

        # TODO: update username

    @db_connector
    def _historic_session_sum(self, col, conn):
        sql = """
            SELECT
                SUM(s.{}) AS {}
            FROM
                player p
                LEFT JOIN session s
                    ON s.steam_id = p.steam_id
            WHERE
                p.steam_id = ?
                AND s.end_date IS NOT NULL
        """.format(col, col)
        cur = conn.cursor()
        cur.execute(sql, (self.steam_id,))
        result, = cur.fetchall()

        return result[col] if result else 0

    @db_connector
    def _rank_session_sum(self, col, conn):
        sql = """
                SELECT
                    COUNT(*) + 1 AS rank
                FROM
                    (
                        SELECT
                            SUM({}) AS metric
                        FROM
                            session
                        WHERE 
                            steam_id != ?
                        GROUP BY steam_id
                    ) others,
                    (
                        SELECT
                            SUM({}) AS metric
                        FROM
                            session
                        WHERE
                            steam_id = ?
                    ) player
                WHERE
                    others.metric >= player.metric
            """.format(col, col)

        cur = conn.cursor()
        cur.execute(sql, (self.steam_id, self.steam_id))
        result, = cur.fetchall()

        return result['rank']

    @db_connector
    def _rank_session_ratio(self, col_num, col_den, conn):
        sql = """
            SELECT
                COUNT(*) + 1 AS rank
            FROM
                (
                    SELECT
                        CAST(SUM({}) AS FLOAT) / SUM({}) AS metric
                    FROM
                        session
                    WHERE 
                        steam_id != ?
                    GROUP BY steam_id
                ) others,
                (
                    SELECT
                        CAST(SUM({}) AS FLOAT) / SUM({}) AS metric
                    FROM
                        session
                    WHERE
                        steam_id = ?
                ) player
            WHERE
                others.metric >= player.metric
        """.format(col_num, col_den, col_num, col_den)

        cur = conn.cursor()
        cur.execute(sql, (self.steam_id, self.steam_id))
        result, = cur.fetchall()

        return result['rank'] or 0.0  # Division by 0

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

    # TODO: Should be managed by server?
    @db_connector
    def op(self, state, conn):
        self.op = state

        sql = """
            UPDATE player SET
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
        return self._historic_session_sum("dosh_spent") \
            + self.session_dosh_spent

    @property
    def total_deaths(self):
        return self._historic_session_sum("deaths")\
            + self.session_deaths

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
                COALESCE(SUM(end_date - start_date), 0) AS time
            FROM
                session
            WHERE
                steam_id = ?
                AND end_date IS NOT NULL
                AND end_date_dirty = 0
        """

        cur = conn.cursor()
        cur.execute(sql, (self.steam_id,))
        result, = cur.fetchall()

        return result['time'] + self.session_time

    @property
    def rank_dosh(self):
        return self._rank_session_sum("dosh")

    @property
    def rank_dosh_spent(self):
        return self._rank_session_sum("dosh_spent")

    @property
    def rank_kills(self):
        return self._rank_session_sum("kills")

    @property
    def rank_deaths(self):
        return self._rank_session_sum("deaths")

    @property
    def rank_damage_taken(self):
        return self._rank_session_sum("damage_taken")

    @property
    @db_connector
    def rank_time(self, conn):
        sql = """
            SELECT
                COUNT(*) + 1 AS rank
            FROM
                (
                    SELECT
                        SUM(
                            CASE 
                                WHEN end_date IS NULL THEN {}
                                ELSE end_date
                            END - start_date
                        ) AS time
                    FROM
                        session
                    WHERE 
                        steam_id != ?
                        AND end_date_dirty = 0
                    GROUP BY steam_id
                ) others,
                (
                    SELECT
                        SUM(
                            CASE 
                                WHEN end_date IS NULL THEN {}
                                ELSE end_date
                            END - start_date
                        ) AS time
                    FROM
                        session
                    WHERE
                        steam_id = ?
                        AND end_date_dirty = 0
                ) player
            WHERE
                others.time >= player.time
        """.format(int(time.time()), int(time.time()))

        cur = conn.cursor()
        cur.execute(sql, (self.steam_id, self.steam_id))
        result, = cur.fetchall()

        return result['rank']

    @property
    @db_connector
    def rank_sessions(self, conn):
        sql = """
            SELECT
                COUNT(*) + 1 AS rank
            FROM
                (
                    SELECT
                        COUNT(*) AS sessions
                    FROM
                        session
                    WHERE 
                        steam_id != ?
                    GROUP BY steam_id
                ) others,
                (
                    SELECT
                        COUNT(*) AS sessions
                    FROM
                        session
                    WHERE
                        steam_id = ?
                ) player
            WHERE
                others.sessions >= player.sessions
        """

        cur = conn.cursor()
        cur.execute(sql, (self.steam_id, self.steam_id))
        result, = cur.fetchall()

        return result['rank']

    @property
    def ratio_dosh_deaths(self):
        if not self.total_deaths:
            return 0.
        return self.total_dosh / self.total_deaths

    @property
    def rank_ratio_dosh_deaths(self):
        return self._rank_session_ratio("dosh", "deaths")

    @property
    def ratio_kills_deaths(self):
        if not self.total_deaths:
            return 0.
        return self.total_kills / self.total_deaths

    @property
    def rank_ratio_kills_deaths(self):
        return self._rank_session_ratio("kills", "deaths")

    @property
    def session_time(self):
        return int(time.time()) - self.session_date

    @db_connector
    def reset_stats(self, conn):
        sql = """
            DELETE FROM session
            WHERE
                steam_id = ?
        """
        conn.cur.execute(sql)

    def __str__(self):
        return """
        Username: {}
        Country: {} ({})
        OP: {}
        Steam ID: {}
        
        Dosh: {}
        Kills: {}
        HP: {}
        Ping: {}
        
        s_dosh: {}
        s_dosh_spent: {}
        s_kills: {}
        s_deaths: {}
        s_damage: {}
        s_time: {}
        
        w_dosh: {}
        w_dosh_spent: {}
        w_kills: {}
        w_deaths: {}
        w_damage: {}
        
        t_dosh: {}
        t_dosh_spent: {}
        t_kills: {}
        t_deaths: {}
        t_damage_taken: {}
        t_time: {}
        t_sessions: {}
        
        r_dosh: {}
        r_dosh_spent: {}
        r_kills: {}
        r_deaths: {}
        r_damage: {}
        r_time: {}
        r_sessions: {}
        
        rat_dd: {}
        rat_r_dd: {}
        rat_kd: {}
        rat_r_kf: {}
        
        """.format(
            self.username,
            self.country,
            self.ip,
            self.op,
            self.steam_id,
            self.dosh,
            self.kills,
            self.health,
            self.ping,
            self.session_dosh,
            self.session_dosh_spent,
            self.session_kills,
            self.session_deaths,
            self.session_damage_taken,
            self.session_time,
            self.wave_dosh,
            self.wave_dosh_spent,
            self.wave_kills,
            self.wave_deaths,
            self.wave_damage_taken,
            self.total_dosh,
            self.total_dosh_spent,
            self.total_kills,
            self.total_deaths,
            self.total_damage_taken,
            self.total_time,
            self.total_sessions,
            self.rank_dosh,
            self.rank_dosh_spent,
            self.rank_kills,
            self.rank_deaths,
            self.rank_damage_taken,
            self.rank_time,
            self.rank_sessions,
            self.ratio_dosh_deaths,
            self.rank_ratio_dosh_deaths,
            self.ratio_kills_deaths,
            self.rank_ratio_kills_deaths,
        )
