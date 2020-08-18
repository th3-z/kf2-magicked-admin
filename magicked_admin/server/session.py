import time

from database import db_connector

"""
TODO: This could be expanded into a class and absorb some functionality from
      the Player class, for now this is simple.
"""

@db_connector
def start_session(conn, steam_id):
    sql = """
        INSERT INTO session
            (steam_id, start_date)
        VALUES
            (?, ?)
    """

    cur = conn.cursor()
    cur.execute(sql, (steam_id, time.time()))
    return cur.lastrowid


@db_connector
def end_session(conn, session_id):
    sql = """
        UPDATE session SET
            end_date = ?
        WHERE
            session_id = ?
    """

    conn.cursor().execute(sql, (time.time(), session_id))


@db_connector
def end_loose_sessions(self):
    sql = """
        UPDATE session SET
            end_date = ?,
            end_date_dirty = 1
        WHERE
            end_date IS NULL
    """

    self.cur.execute(sql, (time.time(),))
