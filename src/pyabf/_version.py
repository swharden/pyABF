__version__ = '2.0.17'

import warnings

def _versionTuple(versionString):
    """
    Return a version string in 'x.x.x' format as a tuple of integers.
    Version numbers in this format can be compared using if statements.
    """
    if not isinstance(versionString, str):
        raise ValueError("version must be a string")
    if not versionString.count(".") == 2:
        raise ValueError("version string must be 'x.x.x' format")
    versionParts = versionString.split(".")
    versionParts = [int(x) for x in versionParts]
    return tuple(versionParts)


def versionAtLeast(versionNeeded, warn=True, halt=False):
    """Return True if the pyABF version is at least a given version."""

    vThis = _versionTuple(__version__)
    vNeed = _versionTuple(versionNeeded)

    if vThis >= vNeed:
        return True
    else:
        errMsg = f"pyABF version {__version__} < required {versionNeeded}"
        if halt:
            raise NotImplementedError(errMsg)
        if warn:
            warnings.warn(errMsg)
        return False

def info():
    """display information about the pyabf package."""
    import os
    _pyabfFolder = os.path.abspath(os.path.dirname(__file__))
    print("pyabf %s was imported from %s" % (__version__, _pyabfFolder))


def help():
    """launch the pyABF project page in a browser."""
    import webbrowser
    webbrowser.open("http://github.com/swharden/pyABF")