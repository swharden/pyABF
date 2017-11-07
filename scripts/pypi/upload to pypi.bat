:: THIS SCRIPT PACKAGES/UPLOADS THE PROJECT TO PYPI
:: you must change the version in __init__.py manually

:: navigate to the source folder
cd ../../src/

:: assemble the package and upload it
python setup.py sdist upload

:: launch the webpage in the browser
explorer http://pypi.python.org/pypi/pyabf

:: wait for the user to manually close the console
pause