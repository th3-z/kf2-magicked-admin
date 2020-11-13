import os
import sys

import certifi
from babel.messages import frontend as babel
from cx_Freeze import Executable, setup, build

VERSION = "0.2.0"

WIN_NT = os.name == "nt"

SRC_PATH = os.path.dirname(__file__)
ROOT_PATH = os.path.join(SRC_PATH, '..')
CERT_PATH = certifi.where()

if not CERT_PATH:
    print(" [!] Couldn't find cacert.pem for SSL requests.")
    sys.exit()


class BuildWithCompile(build):
    def run(self):
        compiler = babel.compile_catalog(self.distribution)
        compiler.domain = ["magicked_admin"]
        compiler.directory = "magicked_admin/locale"
        compiler.run()
        super().run()


def list_mo_files(folder, domain):
    mo_files = []
    for locale in os.listdir(os.path.join(domain, folder)):
        if os.path.isdir(os.path.join(domain, folder, locale)):
            mo_files.append(os.path.join(folder, locale, "LC_MESSAGES", domain + ".mo"))
    return mo_files


includefiles = [
    (os.path.join(SRC_PATH, 'conf/scripts/example'), 'conf/scripts/example'),
    (os.path.join(SRC_PATH, 'conf/scripts/greeter'), 'conf/scripts/greeter'),
    (os.path.join(SRC_PATH, 'conf/marquee/example'), 'conf/marquee/example'),
    (os.path.join(SRC_PATH, 'lua_bridge/init.lua'), 'lua_bridge/init.lua'),
    (CERT_PATH, 'certifi/cacert.pem'),
]

for mo_file in list_mo_files("locale", "magicked_admin"):
    includefiles.append(
        (os.path.join(SRC_PATH, mo_file), mo_file),
    )

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
    version=VERSION,
    description="Scripted management, stats, and bot for KF2-Server",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            os.path.join(SRC_PATH, "magicked_admin.py"),
            base=None,
            targetName=target_name,
            icon=os.path.join(SRC_PATH, "icon.ico")
        )
    ],
    cmdclass={
        'build': BuildWithCompile,
        'compile_catalog': babel.compile_catalog,
        'extract_messages': babel.extract_messages,
        'init_catalog': babel.init_catalog,
        'update_catalog': babel.update_catalog
    }
)
