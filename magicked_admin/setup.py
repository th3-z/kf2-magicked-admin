import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None

includefiles = [
    ('database/server_schema.sql','database/server_schema.sql'),
    ('config/magicked_admin.conf.example','magicked_admin.conf'),
    ('config/server_one.init.example','server_one.init'),
    ('config/server_one.motd.example','server_one.motd')
]

# "FuzzyWuzzy"
build_exe_options={
    "packages": ["os", "queue", "idna", "lxml", "requests", "encodings"],
    "excludes": ["tkinter"],
    "includes": [],
    "include_files": includefiles,
    "include_msvcr": True,
    "zip_include_packages": "*",
    "zip_exclude_packages": ""
}
setup(  name = "Magicked Administrator",
        version = "0.0.1",
        description = "Scripted management, stats, and bot for KF2-Server",
        options = {"build_exe": build_exe_options},
        executables = [
            Executable("main.py",
                base=base,
                targetName="magicked_admin.exe",
                icon="icon.ico"
            )
        ]
)
