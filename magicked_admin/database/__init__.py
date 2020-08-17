import sqlite3
import gettext
from os import path

from utils import find_data_file, warning, info
from database.schema import schema

_ = gettext.gettext
_sqlite_db_file = find_data_file("conf/storage.sqlite")


def _dict_row_factory(c, r):
    dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])


def db_connector(func):
    def with_connection_(*args, **kwargs):
        conn = sqlite3.connect(
            _sqlite_db_file,
            check_same_thread=False,
            isolation_level=None,
        )
        conn.row_factory = _dict_row_factory

        try:
            ret = func(conn, *args, **kwargs)
        except Exception:
            conn.rollback()
            warning(_("SQLite connection error"))
            raise
        else:
            conn.commit()
        finally:
            conn.close()

        return ret
    return with_connection_


def db_init():
    if not path.exists(_sqlite_db_file):
        info(_("Building new database..."))

        conn = sqlite3.connect(_sqlite_db_file, isolation_level=None)
        cur = conn.cursor()

        cur.executescript(schema)

        conn.commit()
        conn.close()
