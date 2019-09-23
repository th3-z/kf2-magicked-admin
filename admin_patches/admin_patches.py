from os import path
from tkinter import *
from tkinter.filedialog import askdirectory

from utils import find_data_file, die, info
from utils.patcher import validate_files, patch_files

PATCHES_PATH = "patches"


def test_dir(d):
    if not d:
        return False

    test_file = path.join(d, "KFGame/Web/ServerAdmin/current_rules.inc")
    if not path.exists(test_file):
        return False
    else:
        return True


def ask_dir():
    return askdirectory(
        initialdir=".",
        title="Select Killing Floor 2 server location"
    )


def run():
    info("Please open your server's install folder in the file dialogue")
    server_path = ask_dir()
    if not server_path:
        die("User cancelled installation")
    if not test_dir(server_path):
        die("Killing Floor 2 server not found in path:\n\t{}"
            .format(server_path), pause=True)

    info("Validating files...")
    target_path = path.join(server_path, "KFGame/Web/ServerAdmin/")
    if not validate_files(target_path):
        die("Server file validation failed, possible reasons:"
            "\n\t - Game update"
            "\n\t - User mods")

    info("Patching files...")
    patches_path = find_data_file(PATCHES_PATH)
    if not patch_files(target_path, patches_path):
        die("Patching failed")
    else:
        print()  # \n
        info("Patches installed successfully!\n")


if __name__ == "__main__":
    Tk().withdraw()
    run()
