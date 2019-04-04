from cx_Freeze import setup, Executable
import os

base = None

ROOT_PATH = os.path.dirname(__file__)

includefiles = [
    (os.path.join(ROOT_PATH, 'database/server_schema.sql'),'database/server_schema.sql'),
    ('/home/the_z/.local/lib/python3.5/site-packages/certifi/cacert.pem','certifi/cacert.pem'),
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
                     base=base,
                     targetName="magicked_admin.exe",
                     icon=os.path.join(ROOT_PATH, "icon.ico")
                     )
      ]
)

