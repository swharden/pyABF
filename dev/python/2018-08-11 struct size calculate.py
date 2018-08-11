CODEBLOCK = """


            self.nEpochNum[i] = readStruct(fb, "h")
            self.nDACNum[i] = readStruct(fb, "h")
            self.nEpochType[i] = readStruct(fb, "h")
            self.fEpochInitLevel[i] = readStruct(fb, "f")
            self.fEpochLevelInc[i] = readStruct(fb, "f")
            self.lEpochInitDuration[i] = readStruct(fb, "i")
            self.lEpochDurationInc[i] = readStruct(fb, "i")
            self.lEpochPulsePeriod[i] = readStruct(fb, "i")
            self.lEpochPulseWidth[i] = readStruct(fb, "i")


            """
import struct

cumulativeOffset = 0
for line in CODEBLOCK.split("\n"):
    line = line.strip()
    if len(line) < 3:
        continue
    if len(line.split('"')) != 3:
        print("ERROR WITH LINE:")
        print(line)

    print(f"{line} # OFFSET = {cumulativeOffset}")
    #print(f"{line[:-1]}, firstByte+{cumulativeOffset})")

    structFormat = line.split('"')[1]
    varSize = struct.calcsize(structFormat)
    cumulativeOffset += varSize
