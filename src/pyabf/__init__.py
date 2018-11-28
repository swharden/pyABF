"""
PyABF - A Python interface to files in the Axon Binary Format (ABF)
    by Scott Harden

Documentation and code examples, and more can be found at:
    https://github.com/swharden/pyABF
"""

import sys
if sys.version_info < (3, 6):
    print("ERROR: pyABF requires Python 3.6 or later\n")
    exit(1)

from ._version import __version__
from ._version import versionAtLeast
from ._version import info
from ._version import help
from pyabf.abf import ABF
from pyabf.atf import ATF
from pyabf import stats
from pyabf import filter
from pyabf import plot
import pyabf.ap
import pyabf.memtest