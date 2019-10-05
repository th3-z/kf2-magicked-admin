import os
import sys

import certifi
from babel.messages import frontend as babel
from cx_Freeze import Executable, setup

VERSION = "0.1"

WIN_NT = os.name == "nt"

SRC_PATH = os.path.dirname(__file__)
ROOT_PATH = os.path.join(SRC_PATH, '..')
CERT_PATH = certifi.where()

if not CERT_PATH:
    print("Couldn't find cacert.pem for SSL requests.")
    sys.exit()

includefiles = [
    (os.path.join(SRC_PATH, 'database/schema.sql'), 'database/schema.sql'),
    (os.path.join(SRC_PATH, 'conf/scripts/example'), 'conf/scripts/example'),
    (os.path.join(SRC_PATH, 'conf/marquee/example'), 'conf/marquee/example'),
    (CERT_PATH, 'certifi/cacert.pem'),
]

target_name = "magicked_admin"
if WIN_NT:
    target_name += ".exe"

build_exe_options = {
    "packages": ["os", "queue", "idna", "lxml", "requests", "encodings"],
    "excludes": ["tkinter"],
    "includes": [],
    "include_files": includefiles,
    "include_msvcr": True,
    "optimize": 2,
    "build_exe": os.path.join(ROOT_PATH, 'bin/magicked_admin'),
    "zip_include_packages": "*",
    "zip_exclude_packages": ""
}
setup(
    name="Magicked Admin",
    version=VERSION + ".0",
    description="Scripted management, stats, and bot for KF2-Server",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(os.path.join(SRC_PATH, "magicked_admin.py"),
                   base=None,
                   targetName=target_name,
                   icon=os.path.join(SRC_PATH, "icon.ico")
                   )
    ],
    cmdclass={
        'compile_catalog': babel.compile_catalog,
        'extract_messages': babel.extract_messages,
        'init_catalog': babel.init_catalog,
        'update_catalog': babel.update_catalog
    }
)
