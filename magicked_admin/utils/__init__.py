import os
import sys


def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.join(
            os.path.dirname(__file__), ".."
        )

    return os.path.join(datadir, filename)
