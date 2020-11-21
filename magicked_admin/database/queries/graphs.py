from database import db_connector

@db_connector
def players_time(conn):
    sql = """
        WITH RECURSIVE time_series(period) AS (
            SELECT 
                MAX(
                    MIN(s.start_date),
                    CAST(strftime('%s', 'now') AS INT) - (60*60*24*30)
                )
            FROM
                session s
            UNION ALL
            SELECT
                period+300
            FROM
                time_series
            WHERE
                period <= CAST(strftime('%s', 'now') AS INT)
        )
        
        SELECT
            ts.period AS `time`,
            COUNT(s.session_id) AS players
        FROM
            time_series ts
            LEFT JOIN session s ON
                s.start_date <= ts.period
                AND s.end_date >= ts.period
                AND s.end_date_dirty != 1
        GROUP BY ts.period
    """

    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall() or []

@db_connector
def kills_time(conn):
    sql = """
        WITH RECURSIVE time_series(period) AS (
            SELECT 
                MAX(
                    MIN(s.start_date),
                    CAST(strftime('%s', 'now') AS INT) - (60*60*24*30)
                )
            FROM
                session s
            UNION ALL
            SELECT
                period+300
            FROM
                time_series
            WHERE
                period <= CAST(strftime('%s', 'now') AS INT)
        )
        
        SELECT
            ts.period AS `time`,
            SUM(s.kills) AS kills
        FROM
            time_series ts
            LEFT JOIN session s ON
                s.start_date <= ts.period
        GROUP BY ts.period
    """

    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall() or []
