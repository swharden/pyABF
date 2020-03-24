"""
Invent a better (truly unique) GUID system
"""

import pyabf
import glob
import os
import sys
import matplotlib.pyplot as plt
import uuid
import datetime
import time
import hashlib

try:
    PATH_HERE = os.path.abspath(os.path.dirname(__file__))
    PATH_DATA = os.path.abspath(PATH_HERE+"../../../data/abfs/")
    PATH_SRC = os.path.abspath(PATH_HERE+"../../../src/")
    DATA_FOLDER = os.path.join(PATH_SRC, "../data/abfs/")
    sys.path.insert(0, PATH_SRC)
    import pyabf
except:
    raise EnvironmentError()


def GetUserList(abf):
    """
    Return the ABF user list as a list of values, 
    or return None if the ABF has no user list.
    """
    assert isinstance(abf, pyabf.ABF)
    if not hasattr(abf, '_stringsSection'):
        return None
    firstBlock = abf._stringsSection.strings[0]
    firstBlockStrings = firstBlock.split(b'\x00')
    userList = firstBlockStrings[-2].decode("utf-8")
    userList = userList.split(",")
    try:
        return [float(x) for x in userList if x]
    except:
        return None


if __name__ == "__main__":

    print("ABF | User List")
    print("----|----------")
    for abfFilePath in glob.glob(PATH_DATA+"/*.abf"):
        abf = pyabf.ABF(abfFilePath)
        userList = GetUserList(abf)
        if (userList):
            print(f"{abf.abfID}|`{userList}`")
