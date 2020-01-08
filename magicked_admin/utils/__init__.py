import os
import sys
import gettext
import logging
import logging.handlers
from colorama import init
from termcolor import colored

_ = gettext.gettext
init()

# __debug__ is always true when building w/ cx_freeze, no known solution
# TODO: Switch to Nuitka for compilation
DEBUG = __debug__ and not hasattr(sys, 'frozen')

VERSION = "0.1.5"
BANNER_URL = "https://th3-z.xyz/kf2-ma"


def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.join(
            os.path.dirname(__file__), ".."
        )

    return os.path.join(datadir, filename)


# TODO: logging module
logger = logging.getLogger("kf2-magicked-admin")
handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", find_data_file("conf/magicked_admin.log"))
)
formatter = logging.Formatter(
    "[%(asctime)s %(levelname)s] %(message)s",
    "%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def banner():
    version_text = colored("<<", 'magenta')
    version_text += colored(VERSION, 'magenta')
    if DEBUG:
        version_text += colored("#DEBUG", 'red')
    version_text += colored(">>", 'magenta')

    # figlet -f rectangles "example"
    lines = [
        colored("               _     _         _\n", 'blue'),
        colored(" _____ ___ ___|_|___| |_ ___ _| |\n", 'blue'),
        colored("|     | .'| . | |  _| '_| -_| . |\n", 'blue'),
        colored("|_|_|_|__,|_  |_|___|_,_|___|___|\n", 'blue'),
        colored("        _ |___| _ \n", 'blue'),
        colored("  ___ _| |_____|_|___", 'blue'),
        colored(" | .'| . |     | |   |", 'blue'),
        colored(" |__,|___|_|_|_|_|_|_|\n", 'blue')
    ]

    lines[5] += "   {}\n".format(version_text)
    lines[6] += colored("  " + BANNER_URL + "\n", 'magenta')

    print(str.join('', lines))


def warning(mesg, log=True, display=True):
    if display:
        print(
            colored(' [!] ', 'yellow')
            + mesg.encode("utf-8").decode(sys.stdout.encoding)
        )
    if log:
        logger.warning(mesg.encode("utf-8").decode(sys.stdout.encoding))


def debug(mesg, log=True, display=True):
    if DEBUG and display:
        print(colored(
            ' [#] ' + mesg.encode("utf-8").decode(sys.stdout.encoding), 'red'
        ))
    if log:
        logger.debug(mesg.encode("utf-8").decode(sys.stdout.encoding))


def info(mesg, log=True, display=True):
    if display:
        print(
            colored(' [*] ', 'green')
            + mesg.encode("utf-8").decode(sys.stdout.encoding)
        )
    if log:
        logger.info(mesg.encode("utf-8").decode(sys.stdout.encoding))


def fatal(mesg, log=True, display=True):
    if display:
        print(
            colored(' [!] ', 'red')
            + mesg.encode("utf-8").decode(sys.stdout.encoding))
    if log:
        logger.fatal(mesg.encode("utf-8").decode(sys.stdout.encoding))


def die(mesg=None, pause=False):
    if mesg:
        fatal(mesg, log=True)
    if pause:
        input(_("\nPress enter to exit..."))
    sys.exit(0)
