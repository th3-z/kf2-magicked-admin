import gettext
import os
import tarfile

from utils.patch import fromfile

_ = gettext.gettext


ORIGINAL_TEMP_PATH = "kf2ma-admin-patcher-originals"

def has_patch(filename, patch_path):
    patch_basenames = [file.split(".patch")[0] for file in os.listdir(patch_path)]
    return os.path.basename(filename) in patch_basenames


def patch_file(target_filepath, patches_path):
    target_basename = os.path.basename(target_filepath)
    patch_filepath = os.path.join(patches_path, target_basename + ".patch")

    patch = fromfile(patch_filepath)
    return patch.apply(0, os.path.dirname(target_filepath))


def install_original(target_filepath, original_filepath):
    tar = tarfile.open(original_filepath)
    reader = tar.extractfile(os.path.basename(target_filepath))

    with open(target_filepath, 'wb') as target_file:
        target_file.write(reader.read())

    reader.close()
