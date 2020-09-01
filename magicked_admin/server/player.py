import gettext
import time

from database import db_connector
from server.session import close_session, start_session
from events import EVENT_WAVE_START, EVENT_PLAYER_UPDATE, EVENT_PLAYER_DEATH
from utils.alg import uuid

_ = gettext.gettext


class Player:
    def __init__(self, server, username, player_identity_data):
        self.server = server

        self.steam_id = player_identity_data.steam_id
        self.player_key = player_identity_data.player_key
        self.session_id = None
        self.session_date = int(time.time())
        self.join_date = None
        self._op = False

        self._username = None
        self.username = username
        self.perk = None
        self.perk_level = 0

        self.ip = player_identity_data.ip
        self.country = player_identity_data.country
        self.country_code = player_identity_data.country_code

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
        start_session(self.steam_id, self.server.match.match_id)

        self.server.event_manager.register_event(
            EVENT_PLAYER_UPDATE + "." + uuid(self.username),
            self.receive_update_data
        )
        self.server.event_manager.register_event(
            EVENT_WAVE_START, self.receive_wave_start
        )

    @db_connector
    def _db_init(self, conn):
        sql = """
            INSERT OR IGNORE INTO player
                (steam_id, insert_date)
            VALUES
                (?, ?)
        """
        cur = conn.cursor()
        cur.execute(sql, (self.steam_id, int(time.time())))
        conn.commit()

        sql = """
            SELECT
                op, insert_date
            FROM
                player
            WHERE
                steam_id = ?
        """
        cur.execute(sql, (self.steam_id,))
        result, = cur.fetchall()
        self.op = True if result['op'] else False
        self.join_date = result['insert_date']

    def close(self):
        self._update_session()
        close_session(self.session_id)

    @property
    def username(self):
        return self._username

    @username.setter
    @db_connector
    def username(self, username, conn):
        self._username = username

        sql = """
            UPDATE player SET
                username = ?
            WHERE
                steam_id = ?
        """

        conn.cursor().execute(sql, (username, self.steam_id))

    def receive_wave_start(self, event, sender, match):
        self.wave_kills = 0
        self.wave_dosh = 0
        self.wave_dosh_spent = 0
        self.wave_damage_taken = 0
        self.wave_deaths = 0

    def receive_update_data(self, event, sender, player_update_data):
        self.session_kills += player_update_data.kills - self.kills
        self.session_dosh += max(player_update_data.dosh - self.dosh, 0)
        self.session_dosh_spent += max(self.dosh - player_update_data.dosh, 0)
        self.session_damage_taken += max(self.health - player_update_data.health, 0)

        self.wave_kills += player_update_data.kills - self.kills
        self.wave_dosh += max(player_update_data.dosh - self.dosh, 0)
        self.wave_dosh_spent += max(self.dosh - player_update_data.dosh, 0)
        self.wave_damage_taken += max(self.health - player_update_data.health, 0)

        if not player_update_data.health and player_update_data.health < self.health:
            self.session_deaths += 1
            self.wave_deaths += 1
            self.server.event_manager.emit_event(
                EVENT_PLAYER_DEATH, self.__class__, player=self
            )

        self.kills = player_update_data.kills
        self.dosh = player_update_data.dosh
        self.health = player_update_data.health
        self.ping = player_update_data.ping
        self.perk = player_update_data.perk

        self._update_session()

    @db_connector
    def _historic_session_sum(self, col, conn):
        sql = """
            SELECT
                COALESCE(SUM(s.{}), 0) AS {}
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
    def _update_session(self, conn):
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

    @property
    def op(self):
        return self._op

    @op.setter
    @db_connector
    def op(self, state, conn):
        self._op = state

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
            username: {}
            total dosh: {}
            total time: {}
            total kills: {}
            country: {}
        """.format(self.username, self.total_dosh, self.total_time, self.total_kills, self.country)