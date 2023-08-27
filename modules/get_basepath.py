import sys
from os.path import dirname, join

def get_basepath(filename):
    if hasattr(sys, "_MEIPASS"):
        # Running from PyInstaller executable
        basedir = join(sys._MEIPASS, "modules")
    else:
        # Running as a script
        basedir = dirname(__file__)
    return join(basedir, filename)