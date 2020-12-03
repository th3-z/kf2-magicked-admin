from database import db_connector

"""
def noise_filter(arr):
    if not arr:
        return arr

    n = 50
    b = [1.0 / n] * n
    a = 1

    return lfilter(b, a, arr).tolist()
"""


@db_connector
def players_time(server_id, conn, period=7):
    sql = """
        SELECT
            date, players
        FROM
            server_players_date
        WHERE
            server_id = ?
            AND date >= CAST(strftime('%s', 'now') AS INT) - (60*60*24*{})
    """.format(period)

    cur = conn.cursor()
    cur.execute(sql, (server_id,))
    return cur.fetchall() or []


@db_connector
def kills_time(server_id, conn, period=7, interval=240):
    sql = """
        WITH RECURSIVE time_series(period) AS (
            SELECT
                CAST(strftime('%s', 'now') AS INT)
            UNION ALL
            SELECT
                period-{}
            FROM
                time_series
            WHERE
                period >= CAST(strftime('%s', 'now') AS INT) - (60*60*24*{})
        )

        SELECT
            ts.period AS `time`,
            COALESCE(SUM(s.kills), 0) AS kills
        FROM
            time_series ts
            LEFT JOIN session s ON
                s.start_date <= ts.period
            INNER JOIN match m ON
                s.match_id = m.match_id
                AND m.server_id = ?
        GROUP BY ts.period
    """.format(interval, period)

    cur = conn.cursor()
    cur.execute(sql, (server_id,))
    return cur.fetchall() or []
