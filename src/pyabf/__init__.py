"""
PyABF - A Python interface to files in the Axon Binary Format (ABF)
    by Scott Harden

Documentation and code examples, and more can be found at:
    https://github.com/swharden/pyABF
"""

import sys

if sys.version_info >= (3, 6):
    from ._version import __version__
    from ._version import versionAtLeast
    from ._version import info
    from ._version import help
    from pyabf.abf import ABF
    from pyabf.atf import ATF
    from pyabf import plot
    from pyabf import filter
else:
    print("WARNING: pyABF is only partially supported on Python versions <3.6")
    from pyabf.abf import ABF