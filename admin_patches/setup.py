import os

from babel.messages import frontend as babel
from cx_Freeze import Executable, build, setup

VERSION = "0.1"

WIN_NT = os.name == "nt"

SRC_PATH = os.path.dirname(__file__)
ROOT_PATH = os.path.join(SRC_PATH, '..')


class BuildWithCompile(build):
    def run(self):
        compiler = babel.compile_catalog(self.distribution)
        compiler.domain = ["admin_patches"]
        compiler.directory = "admin_patches/locale"
        compiler.run()
        super().run()


def list_mo_files(folder, domain):
    mo_files = []
    for locale in os.listdir(os.path.join(domain, folder)):
        if os.path.isdir(os.path.join(domain, folder, locale)):
            mo_files.append(os.path.join(folder, locale, "LC_MESSAGES", domain + ".mo"))
    return mo_files


includefiles = [
    (os.path.join(SRC_PATH, 'patches/current_rules.inc.patch'),
     'patches/current_rules.inc.patch'),
    (os.path.join(SRC_PATH, 'patches/gamesummary.inc.patch'),
     'patches/gamesummary.inc.patch'),
    (os.path.join(SRC_PATH, 'patches/header_base.inc.patch'),
     'patches/header_base.inc.patch'),
]

for mo_file in list_mo_files("locale", "admin_patches"):
    includefiles.append(
        (os.path.join(SRC_PATH, mo_file), mo_file),
    )

target_name = "admin_patches"
if WIN_NT:
    target_name += ".exe"

build_exe_options = {
    "packages": ["os", "queue", "idna", "encodings", "tkinter"],
    "excludes": [],
    "includes": ["tkinter"],
    "include_files": includefiles,
    "include_msvcr": True,
    "optimize": 2,
    "build_exe": os.path.join(ROOT_PATH, 'bin/admin_patches'),
    "zip_include_packages": "*",
    "zip_exclude_packages": ""
}
setup(
    name="Magicked Admin Patcher",
    version=VERSION,
    description="Patches KF2's web admin panel",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            os.path.join(SRC_PATH, "admin_patches.py"),
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
