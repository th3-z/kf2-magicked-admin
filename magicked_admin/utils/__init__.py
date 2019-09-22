import os
import sys

from colorama import init
from termcolor import colored

init()

# __debug__ is always true when building w/ cx_freeze, no known solution
# TODO: Switch to Nuitka for compilation
DEBUG = __debug__ and not hasattr(sys, 'frozen')

VERSION = "0.1.3"
BANNER_URL = "https://th3-z.xyz/kf2-ma"


def die(message=None, pause=False):
    if message:
        print(colored(' [!] ', 'red') + message)
    if pause:
        input("\nPress enter to exit...")
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


def warning(mesg):
    print(colored(' [!] ', 'yellow') + mesg)


def debug(mesg):
    if DEBUG:
        print(colored(' [#] ' + mesg, 'red'))


def info(mesg):
    print(colored(' [*] ', 'green') + mesg)


def fatal(mesg):
    print(colored(' [!] ', 'red') + mesg)
