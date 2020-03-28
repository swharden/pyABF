"""
pyABF - A Python interface to files in the Axon Binary Format (ABF)
    by Scott Harden

Documentation and code examples, and more can be found at:
    https://github.com/swharden/pyABF
"""

import sys
import os

dirname = os.path.abspath(os.path.dirname(__file__))
version_path = os.path.join(dirname, "version.txt")
with open(version_path) as version_file:
    __version__ = version_file.read().strip()

if sys.version_info < (3, 6):
    sys.stdout.write("ERROR: pyabf "+__version__+" requires Python 3.6 or newer.\n")
    sys.stdout.write("pyabf 2.1.10 was the last version to support Python 2.7 and Python 3.5\n")
    sys.exit(1)

from pyabf.abf import ABF
from pyabf.atf import ATF

def info():
    """display information about the pyabf package."""
    import platform
    import numpy
    print()
    print("### pyABF Information ###")
    print("Python", sys.version)
    print("System:", platform.system(), platform.release())
    print("numpy version:", numpy.__version__)
    print("pyabf version:", __version__)
    print("pyabf path:" , os.path.abspath(os.path.dirname(__file__)))
    print()
    
def showInfo():
    info()

def help():
    """launch the pyABF project page in a browser."""
    import webbrowser
    webbrowser.open("http://github.com/swharden/pyABF")