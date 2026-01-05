@echo off
echo ================================================
echo Personal Finance Tracker - Windows Build Script
echo ================================================
echo.

echo Checking for Python...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from python.org
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Building executable with PyInstaller...
pyinstaller --name="PersonalFinanceTracker" ^
    --onefile ^
    --windowed ^
    --add-data "database;database" ^
    --hidden-import PyQt5 ^
    --hidden-import matplotlib ^
    --hidden-import pandas ^
    --icon=resources/app_icon.ico ^
    main.py

if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo ================================================
echo Build completed successfully!
echo ================================================
echo.
echo The executable can be found at:
echo dist\PersonalFinanceTracker.exe
echo.
echo Note: The application will create a database file at:
echo %USERPROFILE%\Documents\FinanceTracker\finance.db
echo on first run.
echo.
pause
