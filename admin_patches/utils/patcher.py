import os
from hashlib import md5

from checksums import ORIG_MD5
from utils import find_data_file, info
from utils.patch import fromfile


def md5sum(fname):
    hash_md5 = md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def validate_files(target_path):
    check_files = ORIG_MD5.keys()

    for filename in os.listdir(target_path):
        if filename in check_files:
            checksum = md5sum(os.path.join(target_path, filename))

            if checksum != ORIG_MD5[filename]:
                return False
    return True


def patch_files(target_path, patches_path):
    for filename in os.listdir(target_path):
        if filename not in ORIG_MD5.keys():
            continue
        patch_path = find_data_file(
            os.path.join(patches_path, filename + ".patch")
        )

        info("Applying {}".format(filename + ".patch"))

        patch = fromfile(patch_path)
        patch.apply(0, target_path)
    return True
