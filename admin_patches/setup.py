import os

from cx_Freeze import Executable, setup

VERSION = "0.1"

WIN_NT = os.name == "nt"

SRC_PATH = os.path.dirname(__file__)
ROOT_PATH = os.path.join(SRC_PATH, '..')


includefiles = [
    (os.path.join(SRC_PATH, 'patches/something.patch'), 'patches/something.patch'),
]

target_name = "magicked_admin"
if WIN_NT:
    target_name += ".exe"

build_exe_options = {
    "packages": ["os", "queue", "idna", "encodings"],
    "excludes": [],
    "includes": [],
    "include_files": includefiles,
    "include_msvcr": True,
    "optimize": 2,
    "build_exe": os.path.join(ROOT_PATH, 'bin/'),
    "zip_include_packages": "*",
    "zip_exclude_packages": ""
}
setup(
    name="Magicked Admin Patcher",
    version=VERSION + ".0",
    description="Patches KF2's web admin panel",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(os.path.join(SRC_PATH, "admin_patches.py"),
                   base=None,
                   targetName=target_name,
                   icon=os.path.join(SRC_PATH, "icon.ico")
                   )
    ]
)
