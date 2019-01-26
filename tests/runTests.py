"""
Code here manages various tests which challenge the pyabf package.

This script fully regenerates all the data header pages, data thumbnails,
and quickstart documentation. Therefore, any code change which affects any 
header values or impacts graphing in any way will be detected immediately (as
git saying that a bunch of files have been changed).

Execution of this script deletes a lot of markdown files and graphs, then 
regenerates them right away. If code changes did not impact functionality,
the the regenerated content will be identical to the original and git won't
identify any changes. This is a sign that the code changes were invisible.

This script should be run before publishing a release.
"""

import os
import sys
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_PROJECT = os.path.abspath(PATH_HERE+"/../")
PATH_DATA = os.path.abspath(PATH_PROJECT+"/data/abfs/")
import importlib.util
import warnings
import glob

# clean old pyc files to prevent magic number errors
for pycFile in glob.glob(PATH_PROJECT+"/src/pyabf/*.pyc"):
    os.remove(pycFile)
for pycFile in glob.glob(PATH_PROJECT+"/src/pyabf/__pycache__/*.pyc"):
    os.remove(pycFile)

def runFunctionInFile(filename, functionName="go"):
    """
    If a specific python file contains a "go()" function, load that file
    as a python module and call the go() function.
    """
    assert os.path.exists(filename)
    spec = importlib.util.spec_from_file_location("tempModule", filename)
    theModule = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(theModule)
    if not functionName in dir(theModule):
        print("ERROR: %s has no %s() function" %
              (os.path.basename(filename), functionName))
    else:
        getattr(theModule, functionName)()


def testInterpreter(path_python):
    """Test pyABF against a specific python interpreter."""
    testFiles = []
    testFiles.append(os.path.dirname(__file__)+"/tests/py2and3.py")
    testFiles.append(os.path.dirname(__file__)+"/../src/setup.py")
    pyVer=3
    if "27" in path_python:
        pyVer=2
    for path_testScript in testFiles:
        bn = os.path.basename(path_testScript)
        print("Testing Python%d interpreter (%s) ... "%(pyVer, bn), end="")
        cmd = '"%s" "%s"'%(path_python, path_testScript)
        if "setup.py" in cmd:
            cmd+= " --name"
        result = os.popen(cmd).read()
        if "Traceback" in result:
            raise Exception("python interpreter error")
        else:
            print("OK")

if __name__ == "__main__":
    
    # set this to true and run this test right before releasing
    testing_for_release = True

    # run this when new ABF files are added to the data folder (slow)
    generate_data_for_new_abf_files = False
    if generate_data_for_new_abf_files or testing_for_release:
        runFunctionInFile(PATH_PROJECT+"/tests/tests/dataHeaders.py")
        runFunctionInFile(PATH_PROJECT+"/tests/tests/dataThumbnails.py")

    # regenerate all graphs for the getting started guide (slow)
    run_tests_involving_matplotlib = False
    if run_tests_involving_matplotlib or testing_for_release:
        runFunctionInFile(PATH_PROJECT+"/tests/tests/gettingStarted.py")

    # common tests: ensure ABF header, data, and core API did not change
    runFunctionInFile(PATH_PROJECT+"/tests/tests/api.py")
    runFunctionInFile(PATH_PROJECT+"/tests/tests/valueChecks.py")
    runFunctionInFile(PATH_PROJECT+"/tests/tests/testHeaders.py")
    runFunctionInFile(PATH_PROJECT+"/tests/tests/moduleTests.py")

    # test against python2 and python3
    testInterpreter(R"C:\Users\scott\Anaconda3\python.exe")
    testInterpreter(R"C:\Users\scott\Anaconda3\envs\Anaconda27\python.exe")

    print("\n\n### TESTS COMPLETED SUCCESSFULLY###\n")
