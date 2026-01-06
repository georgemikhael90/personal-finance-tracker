@echo off
echo ================================================
echo Personal Finance Tracker - Setup Script
echo ================================================
echo.

echo Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.10 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

python --version
echo.

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Creating application icon...
python create_icon.py
if errorlevel 1 (
    echo WARNING: Failed to create icon (application will still work)
)

echo.
echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo You can now run the application in two ways:
echo.
echo 1. Run directly:
echo    python main.py
echo.
echo 2. Build executable (run build_windows.bat):
echo    build_windows.bat
echo    Then run: dist\PersonalFinanceTracker.exe
echo.
echo For quick start instructions, see QUICKSTART.md
echo For full documentation, see README.md
echo.
pause
