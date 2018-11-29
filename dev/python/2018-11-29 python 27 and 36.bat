:: this script tests running the same file with both python 2.7 and 3.6
@ echo off

set python_file = ".\dev\python\2018-11-29 python 27 and 36.py"

echo.
echo TESTING WITH PYTHON 2.7
"C:\Users\scott\Anaconda3\envs\Anaconda27\python.exe" %python_file %

echo.
echo TESTING WITH PYTHON 3.6
"C:\Users\scott\Anaconda3\python.exe" %python_file %

echo.