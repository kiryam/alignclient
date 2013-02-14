from cx_Freeze import setup, Executable

setup(
    name = "Traffic Aligner",
    version = "0.1",
    description = "Traffic Aligner",
    executables = [Executable("TrafficAligner.py")])
