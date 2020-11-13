import gettext
import sqlite3
from os import path
import time

from utils import find_data_file
from database.schema import schema

_ = gettext.gettext
_sqlite_db_file = find_data_file("conf/storage.sqlite")


def _dict_row_factory(c, r):
    return dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])


def db_connector(func):
    def _with_connection(*args, **kwargs):
        conn = sqlite3.connect(
            _sqlite_db_file,
            check_same_thread=False,
            isolation_level=None,
        )
        conn.row_factory = _dict_row_factory
        kwargs['conn'] = conn

        try:
            ret = func(*args, **kwargs)
        except Exception:
            conn.rollback()
            #warning(_("SQLite error"))
            raise
        else:
            conn.commit()
        finally:
            conn.close()

        return ret
    return _with_connection


def db_init():
    if not path.exists(_sqlite_db_file):
        #info(_("Building new database..."))

        conn = sqlite3.connect(_sqlite_db_file, isolation_level=None)
        cur = conn.cursor()

        cur.executescript(schema)

        conn.commit()
        conn.close()

    _end_loose_matches()
    _end_loose_sessions()


@db_connector
def _end_loose_sessions(conn):
    sql = """
        UPDATE session SET
            end_date = ?,
            end_date_dirty = 1
        WHERE
            end_date IS NULL
    """

    conn.cursor().execute(sql, (int(time.time()),))


@db_connector
def _end_loose_matches(conn):
    sql = """
        UPDATE match SET
            end_date = ?,
            end_date_dirty = 1
        WHERE
            end_date IS NULL
    """

    conn.cursor().execute(sql, (int(time.time()),))


