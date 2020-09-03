import time
from database import db_connector

@db_connector
def top_by_col(col, conn, period=None, limit=None):
    sql = """
        SELECT
            COALESCE(p.username, "Unnamed") AS username,
            p.steam_id AS steam_id,
            SUM(s.{}) AS score
        FROM
            player p
            LEFT JOIN session s ON
                s.steam_id = p.steam_id
                AND ? - s.start_date <= ?
        GROUP BY p.steam_id
        ORDER BY score DESC
        LIMIT ?
    """.format(col)

    cur = conn.cursor()
    cur.execute(sql, (time.time(), period or time.time(), limit or -1))
    return cur.fetchall() or []

    