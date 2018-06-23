import os
import sys
import struct
import numpy as np
import matplotlib.pyplot as plt
def readStruct(f, structFormat, seekTo):
  f.seek(seekTo)
  byteCount = struct.calcsize(structFormat)
  byteString = f.read(byteCount)
  value = struct.unpack(structFormat, byteString)
  return list(value)

def setupPaths():
    """Enter the folder of demo ABFs"""
    abdDataPath = os.path.abspath(__file__+"/.."*6+"/data/abfs/")
    os.chdir(abdDataPath)

def go():
    f = open("14o08011_ic_pair.abf", 'rb')
    DataSection = readStruct(f, "IIl", 236)
    ADCSection = readStruct(f, "IIl", 92)
    channelCount = ADCSection[2]
    f.seek(DataSection[0]*512)
    data = np.fromfile(f, dtype=np.int16, count=DataSection[2])
    data = np.reshape(data, (int(len(data)/channelCount), channelCount))
    data = np.rot90(data)[::-1]
    f.close()
    print(data)

    import matplotlib.pyplot as plt
    plt.figure(figsize=(12,3))
    for channel in range(channelCount):
        plt.plot(data[channel], label=f"channel {channel}", alpha=.7)
    plt.margins(0,0)
    plt.tight_layout()
    plt.axis([250_000, 425_000, -2300, 1700])
    plt.legend()
    plt.savefig(R"C:\Users\scott\Desktop\01.png")
    plt.show()
    

if __name__=="__main__":
    setupPaths()
    go()
