import os, sys
import site

from os import path

from cx_Freeze import Executable, setup

ROOT_PATH = os.path.dirname(__file__)

CERT_PATH = None

sites = site.getsitepackages() + [site.getusersitepackages()]

for site in sites:
    if path.exists(path.join(site, 'certifi/cacert.pem')):
        CERT_PATH = path.join(site, 'certifi/cacert.pem')

if not CERT_PATH:
    print("Couldn't find cacert.pem for SSL requests.")
    sys.exit()


includefiles = [
    (os.path.join(ROOT_PATH, 'database/server_schema.sql'),'database/server_schema.sql'),
    (CERT_PATH,'certifi/cacert.pem'),
]

build_exe_options = {
    "packages": ["os", "queue", "idna", "lxml", "requests", "encodings"],
    "excludes": ["tkinter"],
    "includes": [],
    "include_files": includefiles,
    "include_msvcr": True,
    "optimize": 2,
    "zip_include_packages": "*",
    "zip_exclude_packages": ""
}
setup(name="Magicked Administrator",
      version="0.0.1",
      description="Scripted management, stats, and bot for KF2-Server",
      options = {"build_exe": build_exe_options},
      executables=[
          Executable(os.path.join(ROOT_PATH, "magicked_administrator.py"),
                     base=None,
                     targetName="magicked_admin.exe",
                     icon=os.path.join(ROOT_PATH, "icon.ico")
                     )
      ]
)
