import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.


# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"
build_exe_options={
    "packages": ["os", "queue", "idna", "lxml", "requests"],
    "excludes": ["tkinter"],
    "includes": [],
    "include_files": [],
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