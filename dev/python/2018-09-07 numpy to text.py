'''
str(np.ndarray(stuff)) returns a different string depending on numpy version.
develop a standard way to print arrays and multidimensional arrays which
will never change.
'''

import numpy as np


def standardNumpyText(data):
    """return a numpy array as a standard string regardless of numpy version."""
    if isinstance(data, np.ndarray):
        out = "array (%dd) with values like: "%(len(data.shape))
        data = data.flatten()
        if len(data) < 10:
            data = ["%.05f" % x for x in data]
            data = ", ".join(data)
            out += f"{data}"
        else:
            dataFirst = ["%.05f" % x for x in data[:3]]
            dataFirst = ", ".join(dataFirst)
            dataLast = ["%.05f" % x for x in data[-3:]]
            dataLast = ", ".join(dataLast)
            out += f"{dataFirst}, ..., {dataLast}"
    else:
        out = str(out)
    return out




if __name__ == "__main__":
    array1d = np.random.random_sample(10000)*1000-500
    nRows = int(len(array1d)/50)
    nCols = int(len(array1d)/nRows)
    array2d = np.reshape(array1d, (nRows, nCols))
    print(standardNumpyText(array1d))
    print(standardNumpyText(array2d))
