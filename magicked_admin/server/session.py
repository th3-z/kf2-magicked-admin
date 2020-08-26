import time

from database import db_connector

"""
TODO: This could be expanded into a class and absorb some functionality from
      the Player class, for now this is simple.
"""

@db_connector
def start_session(steam_id, conn):
    sql = """
        INSERT INTO session
            (steam_id, start_date)
        VALUES
            (?, ?)
    """

    cur = conn.cursor()
    cur.execute(sql, (steam_id, int(time.time())))
    return cur.lastrowid


@db_connector
def end_session(session_id, conn):
    sql = """
        UPDATE session SET
            end_date = ?
        WHERE
            session_id = ?
    """

    conn.cursor().execute(sql, (int(time.time()), session_id))


@db_connector
def end_loose_sessions(conn):
    sql = """
        UPDATE session SET
            end_date = ?,
            end_date_dirty = 1
        WHERE
            end_date IS NULL
    """

    conn.cursor().execute(sql, (int(time.time()),))
