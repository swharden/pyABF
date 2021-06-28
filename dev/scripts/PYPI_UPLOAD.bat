:: To use this script: pip install twine
@echo off

:: python versionIncrease.py

:: navigate to the source folder and delete old builds
cd ../../src/
rmdir /S /q _build 2>nul
rmdir /S /q build 2>nul
rmdir /S /q dist 2>nul
rmdir /S /q pyabf.egg-info 2>nul
 
:: create the distribution
echo ### building distribution with setuptools...
python setup.py --quiet sdist

echo ### press ENTER 3 times to upload...
pause
pause
pause

twine upload --username swharden --repository-url https://upload.pypi.org/legacy/ dist/*
explorer https://pypi.org/project/pyabf/

echo COMPLETE
pause