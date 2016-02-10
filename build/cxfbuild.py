from cx_Freeze import setup, Executable
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
        name = "2c1t",
        version = "0.3",
        description = "2 cars, 1 table",
        executables = [Executable(
            script="game_ar.py",
            icon ="2c1t.ico",
            compress = True,
            targetName = "2c1t.exe",
            base = base,
            )])