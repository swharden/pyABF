def getDigitizerName(digitizerNumber):
    digitizers = {
        0: "Unknown",
        1: "Demo",
        2: "MiniDigi",
        3: "DD132X",
        4: "OPUS",
        5: "PATCH",
        6: "Digidata 1440",
        7: "MINIDIGI2",
        8: "Digidata 1550"
    }

    if (digitizerNumber in digitizers.keys()):
        return digitizers[digitizerNumber]
    else:
        return "Unknown"


def getTelegraphName(telegraphNumber):
    telegraphs = {
        0: "Unknown instrument (manual or user defined telegraph table).",
        1: "Axopatch-1 with CV-4-1/100",
        2: "Axopatch-1 with CV-4-0.1/100",
        3: "Axopatch-1B(inv.) CV-4-1/100",
        4: "Axopatch-1B(inv) CV-4-0.1/100",
        5: "Axopatch 200 with CV 201",
        6: "Axopatch 200 with CV 202",
        7: "GeneClamp",
        8: "Dagan 3900",
        9: "Dagan 3900A",
        10: "Dagan CA-1  Im=0.1",
        11: "Dagan CA-1  Im=1.0",
        12: "Dagan CA-1  Im=10",
        13: "Warner OC-725",
        14: "Warner OC-725",
        15: "Axopatch 200B",
        16: "Dagan PC-ONE  Im=0.1",
        17: "Dagan PC-ONE  Im=1.0",
        18: "Dagan PC-ONE  Im=10",
        19: "Dagan PC-ONE  Im=100",
        20: "Warner BC-525C",
        21: "Warner PC-505",
        22: "Warner PC-501",
        23: "Dagan CA-1  Im=0.05",
        24: "MultiClamp 700",
        25: "Turbo Tec",
        26: "OpusXpress 6000A",
        27: "Axoclamp 900"
    }

    if (telegraphNumber in telegraphs.keys()):
        return telegraphs[telegraphNumber]
    else:
        return "Unknown"


def getUserListParameterName(paramNumber, epochCount=50):
    """
    Given an epoch paramater number return a human readable description
    of what it's supposed to modify in the epoch table.
    Based on: ABFHEADR.H#L530-L549
    """
    if paramNumber == 0:
        return "CONDITNUMPULSES"
    if paramNumber == 1:
        return "CONDITBASELINEDURATION"
    if paramNumber == 2:
        return "CONDITBASELINELEVEL"
    if paramNumber == 3:
        return "CONDITSTEPDURATION"
    if paramNumber == 4:
        return "CONDITSTEPLEVEL"
    if paramNumber == 5:
        return "CONDITPOSTTRAINDURATION"
    if paramNumber == 6:
        return "CONDITPOSTTRAINLEVEL"
    if paramNumber == 7:
        return "EPISODESTARTTOSTART"
    if paramNumber == 8:
        return "INACTIVEHOLDING"
    if paramNumber == 9:
        return "DIGITALHOLDING"
    if paramNumber == 10:
        return "PNNUMPULSES"
    if paramNumber == 11:
        return "PARALLELVALUE"
    paramRemainder = paramNumber - 11

    if (paramRemainder < epochCount):
        return f"EPOCHINITLEVEL"
    paramRemainder -= epochCount

    if (paramRemainder < epochCount):
        return f"EPOCHINITDURATION"
    paramRemainder -= epochCount

    if (paramRemainder < epochCount):
        return f"EPOCHTRAINPERIOD"
    paramRemainder -= epochCount

    if (paramRemainder < epochCount):
        return f"EPOCHTRAINPULSEWIDTH"
    paramRemainder -= epochCount

    if (paramRemainder < epochCount):
        return f"EPOCHINITDURATION"
    paramRemainder -= epochCount

    return f"UNKNOWN {paramNumber}"
