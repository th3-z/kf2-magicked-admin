import sys, os

from colorama import init
from termcolor import colored

init()

# __debug__ is always true when building w/ cx_freeze, no known solution
DEBUG = __debug__ and not hasattr(sys, 'frozen')

VERSION_TEXT = "0.1.0"
if DEBUG:
    VERSION_TEXT += "#DEBUG"
BANNER_URL = "https://th3-z.xyz/kf2-ma"


def die(message=None):
    if message:
        print(colored(' [!] ', 'red') + message)
    sys.exit(0)


def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.join(
            os.path.dirname(__file__), ".."
        )

    return os.path.join(datadir, filename)


def banner():
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

    lines[5] += colored("   <<V{}>>\n".format(VERSION_TEXT), 'magenta')
    lines[6] += colored("  "+BANNER_URL+"\n", 'magenta')

    print(str.join('', lines))


def warning(mesg):
    print(colored(' [!] ', 'yellow') + mesg)


def debug(mesg):
    print(colored(' [#] ' + mesg, 'red'))


def info(mesg):
    print(colored(' [*] ', 'magenta') + mesg)
