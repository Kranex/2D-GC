@echo off
if not defined INSTALL_LOCATION set INSTALL_LOCATION=.
set PYTHON_URL=https://www.python.org/ftp/python/3.7.3/python-3.7.3.exe
set NAME=2D-GC

::----------------
:begining
echo Checking if python3 is installed...
py -3 --version >NUL
if errorlevel 1 goto ipython

echo Checking if pip is installed...
py -3 -m pip -v >NUL
if errorlevel 1 goto ipip

echo Checking if pyinstaller is installed...
py -3 -m PyInstaller -v >NUL
if errorlevel 1 py -3 -m pip install git+https://github.com/pyinstaller/pyinstaller.git

echo Installing dependencies...
py -3 -m pip install -r requirements.txt

echo Creating portable %NAME%...
py -3 -m PyInstaller --onefile --noconfirm --name="%NAME%" -noconsole --distpath="%INSTALL_LOCATION%" gc2d\__main__.py

:: Offer to uninstall python if we installed it.
if defined INSTALLED_PYTHON goto upython

::----------------
:complete
echo Creation of portable %NAME% complete!
pause
exit
::---------------
:ipython
set /p yn=Download and install python ^(y/N^)^? 
if /I not "%yn%"=="y" goto npython
:: Download python if it hasn't been already...
echo downloading python...
if not exist python-installer.exe cscript WINDOWS_DOWNLOAD_PYTHON.vbs "%PYTHON_URL%" >NUL

:: Prompt user to install python3.
echo installing python3...
python-installer.exe PrependPath=1 SimpleInstall=1 SimpleInstallDescription="Install the complete python suite and add python to the PATH."
set INSTALLED_PYTHON=1
start "" "%0"
exit
::----------------
:upython
set /p yn=The installation is now complete and python3 is no longer required, would you like to uninstall it ^(y/N^)? 
if /I "%yn%"=="y" echo Uninstalling python3... & python-installer.exe /uninstall
goto :complete
::----------------
:npython
echo Error^: please install python3.
pause
exit
::----------------
:ipip
echo Your current install of python3 does not include pip. 
echo You can either install pip yourself, or this script can download and reinstall python%PYTHON_VERSION% for you.
:goto ipython
::----------------
