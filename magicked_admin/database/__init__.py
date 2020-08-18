import sqlite3
import gettext
from os import path

from utils import find_data_file, warning, info
from database.schema import schema

_ = gettext.gettext
_sqlite_db_file = find_data_file("conf/storage.sqlite")


def _dict_row_factory(c, r):
    dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])


# TODO: move to database.py and import here
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
            warning(_("SQLite connection error"))
            raise
        else:
            conn.commit()
        finally:
            conn.close()

        return ret
    return _with_connection


# TODO: as above
def db_init():
    if not path.exists(_sqlite_db_file):
        info(_("Building new database..."))

        conn = sqlite3.connect(_sqlite_db_file, isolation_level=None)
        cur = conn.cursor()

        cur.executescript(schema)

        conn.commit()
        conn.close()
