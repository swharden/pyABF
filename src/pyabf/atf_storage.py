import os
import sys
import pprint

from pyabf.atf_reader import ATFReader


class ATFStorage():
    """
    A cache for ATFReader objects

    This object can be bassed into pyABF.ABF to avoid having to repeatedly
    reparse ATF files.
    """

    def __init__(self, basefolder=None):
        """
        The basefolder parameter allows to pass in a known folder location on
        disc which holds ATF files.
        """

        self._cache = {}
        self._basefolder = None

        if basefolder != None:
            if not os.path.isdir(basefolder):
                raise ValueError(f"The string {basefolder} does not refer to an existing directory.")

            self._basefolder = os.path.abspath(basefolder)

    def _load(self, file_path):
        """
        The ATF file is searched in the following locations (in that order):
          - absolute location `file_path`
          - basefolder given in the constructor
          - current directory

        Return an ATFReader instance
        """

        # absolute path
        location = file_path
        if os.path.isabs(file_path):
            try:
                return ATFReader(file_path)
            except ValueError:
                pass

        # basefolder
        if self._basefolder != None:
            basename = os.path.basename(file_path)
            location = os.path.join(self._basefolder, basename)

            try:
                return ATFReader(location)
            except ValueError:
                pass

        # current directory
        location = os.path.abspath(basename)

        try:
            return ATFReader(location)
        except ValueError:
            pass

        raise ValueError(f"Could not find the file {file_path}.")

    def get(self, file_path):
        """
        Return the cached ATFReader instance for the given file_path or create
        the object, cache it and return it.
        """

        if self._cache.get(file_path) == None:
            self._cache[file_path] = self._load(file_path)

        return self._cache[file_path]

    def __str__(self):
        return ("Basefolder {}\n"
                "Cache: {}").format(self._basefolder, self._cache)
