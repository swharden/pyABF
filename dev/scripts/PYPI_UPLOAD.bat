:: this upload script when Anaconda is installed in the user folder.

:: to use twine I had to first set it up
:: conda install twine
:: conda update pip setuptools twine

:: activate anaconda
set root=C:\%HOMEPATH%\Anaconda3
call %root%\Scripts\activate.bat %root%

:: navigate to the source folder
cd ../../../src/

:: create your distribution
python setup.py sdist bdist_wheel

:: upload to the test server
twine upload --username swharden --repository-url https://test.pypi.org/legacy/ dist/*
explorer https://test.pypi.org/project/pyabf/
pause

echo CONTINUE TO UPLOAD TO REAL PYPI
pause
twine upload --username swharden dist/*
pause