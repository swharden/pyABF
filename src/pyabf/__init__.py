"""
pyabf - A Python package for reading and analyzing files in Axon Binary Format (ABF).
Documentation, code examples, and more can be found at: https://github.com/swharden/pyABF
"""

from pyabf.abf import ABF

__version__ = '2.0.1'

def info():
    """display information about the pyabf package."""
    import os
    _pyabfFolder=os.path.abspath(os.path.dirname(__file__))
    print("pyabf %s was imported from %s"%(__version__,_pyabfFolder))

def help():
    """launch the pyABF project page in a browser."""
    import webbrowser
    webbrowser.open("http://github.com/swharden/pyABF")

__all__ = ('ABF','info','help')