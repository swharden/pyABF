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


if __name__ == "__main__":
    for abf_path in pathlib.Path(PATH_ABFS).glob("*.abf"):
        print(abf_path)
        abf = pyabf.ABF(abf_path)
        pathlib.Path(f"test-{abf.abfID}.txt").write_text(abf.headerText)
        pathlib.Path(f"test-{abf.abfID}.html").write_text(abf.headerHTML)
