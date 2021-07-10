import sys
import pathlib

try:
    PATH_HERE = pathlib.Path(__file__).parent
    PATH_ABFS = PATH_HERE.joinpath("../../data/abfs/").resolve()
    PATH_SRC = PATH_HERE.joinpath("../../src/").resolve()
    print(PATH_SRC)
    sys.path.insert(0, str(PATH_SRC))
    import pyabf
    import pyabf.tools.memtest
except:
    raise EnvironmentError()


if __name__ == "__main__":
    abfPath = pathlib.Path(PATH_ABFS).joinpath("vc_drug_memtest.abf")
    abf = pyabf.ABF(abfPath)
    memtest = pyabf.tools.memtest.Memtest(abf)
    print(f"Ih: {memtest.Ih.values}")
    print(f"Rm: {memtest.Rm.values}")
    print(f"Ra: {memtest.Ra.values}")
    print(f"Cm: {memtest.CmStep.values}")
