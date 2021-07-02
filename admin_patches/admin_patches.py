import argparse
import gettext
import os

from utils import die, find_data_file, info, warning
from utils.patcher import has_patch, install_original, patch_file

_ = gettext.gettext

PATCHES_PATH = "patches"
ORIGINAL_FILENAME = "original.tar.gz"

parser = argparse.ArgumentParser(
    description=_('Killing Floor 2 Admin Patches')
)
parser.add_argument(
    '-r', '--restore', action='store_true', help=_('Restore original file and retry if a patch fails')
)
parser.add_argument(
    '-o', '--restore-all', action='store_true', help=_('Restore webadmin to stock files without patching')
)
parser.add_argument(
    '-t', '--target', type=str, help=_('Specify server location')
)

args = parser.parse_args()
if not args.target:
    from tkinter import *
    from tkinter.filedialog import askdirectory
    Tk().withdraw()
NOGUI = True if args.target else False


def test_dir(d):
    if not d:
        return False

    test_file = os.path.join(d, _("KFGame/Web/ServerAdmin/current_rules.inc"))
    if not os.path.exists(test_file):
        return False
    else:
        return True


def ask_dir():
    return askdirectory(
        initialdir=".",
        title=_("Select Killing Floor 2 server location")
    )


def ask_install_orig(filename):
    if NOGUI:
        return False
    warning(_("A patch for '{}' cannot be applied").format(filename))
    reply = input(_("Restore original '{}' file? [Y/N]: ").format(filename))
    return reply in ["Y", "y", "Yes", "yes"]


def run():
    if NOGUI:
        server_path = args.target
    else:
        info(_("Please open your server's install folder in the file "
               "dialogue"))
        server_path = ask_dir()

    if not server_path:
        die(_("User cancelled installation"), pause=True)
    if not test_dir(server_path):
        die(_("Killing Floor 2 server not found in path:\n\t{}")
            .format(server_path), pause=True)

    target_path = os.path.join(server_path, "KFGame/Web/ServerAdmin")
    patches_path = find_data_file(PATCHES_PATH)
    original_filepath = find_data_file(ORIGINAL_FILENAME)

    patch_skipped = False

    if args.restore_all:
        for filename in os.listdir(target_path):
            install_original(
                os.path.join(target_path, filename), original_filepath
            )
            info(_("Restored '{}'").format(filename))
        return

    for filename in os.listdir(target_path):
        if not has_patch(filename, patches_path):
            continue

        if patch_file(os.path.join(target_path, filename), patches_path):
            info(_("Patched '{}'").format(filename))
            continue

        if not args.restore and not ask_install_orig(filename):
            patch_skipped = True
            warning("Patching '{}' failed, file skipped".format(filename))
            continue

        install_original(os.path.join(target_path, filename), original_filepath)
        if patch_file(os.path.join(target_path, filename), patches_path):
            info(_("Patched '{}'").format(filename))
        else:
            # Shouldn't be reachable
            patch_skipped = True
            warning(_("Patching '{}' failed, file skipped").format(filename))

    print()  # \n
    if patch_skipped:
        warning(_("One or more patches were not applied"))
    else:
        info(_("All patches installed successfully!\n"))


if __name__ == "__main__":
    run()
    die(pause=(not NOGUI))
