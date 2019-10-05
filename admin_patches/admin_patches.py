from os import path
import argparse
import gettext

from utils import find_data_file, die, info
from utils.patcher import validate_files, patch_files

_ = gettext.gettext

PATCHES_PATH = "patches"

parser = argparse.ArgumentParser(
    description=_('Killing Floor 2 Admin Patches')
)
parser.add_argument(
    '-t', '--target', type=str, help=_('Specify server location')
)
args = parser.parse_args()
if not args.target:
    from tkinter import *
    from tkinter.filedialog import askdirectory
    Tk().withdraw()


def test_dir(d):
    if not d:
        return False

    test_file = path.join(d, _("KFGame/Web/ServerAdmin/current_rules.inc"))
    if not path.exists(test_file):
        return False
    else:
        return True


def ask_dir():
    return askdirectory(
        initialdir=".",
        title=_("Select Killing Floor 2 server location")
    )


def run(target=None):
    if args.target or target:
        server_path = args.target or target
    else:
        info(_("Please open your server's install folder in the file "
               "dialogue"))
        server_path = ask_dir()

    if not server_path:
        die(_("User cancelled installation"))
    if not test_dir(server_path):
        die(_("Killing Floor 2 server not found in path:\n\t{}")
            .format(server_path), pause=True)

    info(_("Validating files..."))
    target_path = path.join(server_path, "KFGame/Web/ServerAdmin")
    if not validate_files(target_path):
        die(_("Server file validation failed, possible reasons:"
              "\n\t - Game update"
              "\n\t - User mods"
              "\n\t - Patches already applied"))

    info(_("Patching files..."))
    patches_path = find_data_file(PATCHES_PATH)

    if not patch_files(target_path, patches_path):
        die(_("Patching failed"))
    else:
        print()  # \n
        info(_("Patches installed successfully!\n"))


if __name__ == "__main__":
    run()
