:: this upload script when Anaconda is installed in the user folder.

:: to use twine I had to first set it up
:: conda install twine
:: conda update pip setuptools twine

:: make commands silent
@echo off

:: activate anaconda
set root=C:\%HOMEPATH%\Anaconda3
call %root%\Scripts\activate.bat %root%


:: navigate to the source folder
cd ../../src/
cmd.exe