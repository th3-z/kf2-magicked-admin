import time

from database import db_connector

"""
TODO: This could be expanded into a class and absorb some functionality from
      the Player class, for now this is simple.
"""

@db_connector
def start_session(steam_id, match_id, conn):
    sql = """
        INSERT INTO session
            (steam_id, match_id, start_date)
        VALUES
            (?, ?, ?)
    """

    cur = conn.cursor()
    cur.execute(sql, (steam_id, match_id, int(time.time())))
    return cur.lastrowid


@db_connector
def close_session(session_id, conn):
    sql = """
        UPDATE session SET
            end_date = ?
        WHERE
            session_id = ?
    """

    conn.cursor().execute(sql, (int(time.time()), session_id))


