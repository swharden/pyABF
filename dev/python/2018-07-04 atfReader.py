from imports import *

if __name__ == "__main__":

    sweep = 0
    channel = 0

    # load ABF data with pyABF
    abf = pyabf.ABF(PATH_DATA+"/model_vc_step.abf")
    abf.setSweep(sweep, channel)

    # load ABF data which was converted to ATF
    atfFname = abf.abfFilePath.replace(".abf",".atf")
    assert (os.path.exists(atfFname))
    atf = np.loadtxt(atfFname, skiprows = 3, comments='"')
    atf = np.rot90(atf)
    

    # display sweep info
    print("sweep length, first point, last point")
    print("ABF:", len(abf.sweepY), abf.sweepY[0], abf.sweepY[-1])
    print("ATF:", len(atf[0]), atf[0][0], atf[0][-1])

    # plot the stuff
    plt.plot(atf[channel], label="ATF")
    plt.plot(abf.sweepY, label="pyABF")
    plt.legend()
    plt.show()

    # assertions
    assert (abf.sweepPointCount == len(abf.sweepY))

    print("DONE")
