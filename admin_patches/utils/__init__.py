import os
import sys
import gettext

_ = gettext.gettext

# __debug__ is always true when building w/ cx_freeze, no known solution
# TODO: Switch to Nuitka for compilation
DEBUG = __debug__ and not hasattr(sys, 'frozen')

VERSION = "0.0.1"


def die(mesg, pause=False):
    if mesg:
        fatal(mesg)
    if pause:
        input(_("\nPress enter to exit..."))
    sys.exit(0)


def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.join(
            os.path.dirname(__file__), ".."
        )

    return os.path.join(datadir, filename)


def warning(mesg):
    print(' [!] ' + mesg)


def debug(mesg):
    if DEBUG:
        print(' [#] ' + mesg)


def info(mesg):
    print(' [*] ' + mesg)


def fatal(mesg):
    print(' [!] ' + mesg)
