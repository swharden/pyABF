"""
pyABF - A Python interface to files in the Axon Binary Format (ABF)
    by Scott Harden

Documentation and code examples, and more can be found at:
    https://github.com/swharden/pyABF
"""
__version__ = '2.3.7'

import sys
import os

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