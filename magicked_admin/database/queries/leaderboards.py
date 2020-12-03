import time

from database import db_connector


@db_connector
def top_by_col(col, server_id, conn, period=None, limit=None):
    sql = """
        SELECT
            COALESCE(p.username, "Unnamed") AS username,
            p.player_id AS player_id,
            SUM(s.{}) AS score
        FROM
            player p
            LEFT JOIN session s ON
                s.player_id = p.player_id
                AND ? - s.start_date <= ?
        WHERE
            p.server_id = ?
        GROUP BY p.steam_id
        ORDER BY score DESC
        LIMIT ?
    """.format(col)

    cur = conn.cursor()
    cur.execute(sql, (time.time(), period or time.time(), server_id, limit or -1))
    return cur.fetchall() or []


@db_connector
def top_by_playtime(conn, server_id, period=None, limit=None):
    sql = """
        SELECT
            p.username AS username,
            p.steam_id AS steam_id,
            SUM(
                COALESCE(s.end_date, ?) - s.start_date
            ) AS playtime
        FROM
            player p
            LEFT JOIN session s ON
                s.steam_id = p.steam_id
                AND NOT s.end_date_dirty
                AND ? - s.start_date <= ?
        WHERE
            p.server_id = ?
        GROUP BY p.steam_id
        ORDER BY playtime DESC
        LIMIT ?
    """

    cur = conn.cursor()
    cur.execute(sql, (time.time(), time.time(), period or time.time(), server_id, limit or -1))
    return cur.fetchall() or []
