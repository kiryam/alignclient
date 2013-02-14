from cx_Freeze import setup, Executable

setup(
    name = "Traffic Aligner reloader",
    version = "0.1",
    description = "Traffic Aligner  reloader",
    executables = [Executable("reloader.py")])
