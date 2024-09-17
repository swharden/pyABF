import sys
import pathlib

try:
    PATH_HERE = pathlib.Path(__file__).parent
    PATH_ABFS = PATH_HERE.joinpath("../../data/abfs/").resolve()
    PATH_SRC = PATH_HERE.joinpath("../../src/").resolve()
    print(PATH_SRC)
    sys.path.insert(0, str(PATH_SRC))
    import pyabf
except:
    raise EnvironmentError()
1

if __name__ == "__main__":
    abf = pyabf.ABF(R"C:\Users\swharden\Documents\Temp\24215056.abf")

    for abf_path in pathlib.Path(PATH_ABFS).glob("*.abf"):
        abf = pyabf.ABF(abf_path)