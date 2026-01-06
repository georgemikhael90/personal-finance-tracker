# Personal Finance Tracker - PowerShell Build Script
# Builds a Release version of PersonalFinanceTracker.exe

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Personal Finance Tracker - Release Build Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking for Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.10 or higher from python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Clean previous build artifacts
Write-Host ""
Write-Host "Cleaning previous build artifacts..." -ForegroundColor Yellow
if (Test-Path "build") {
    Remove-Item -Path "build" -Recurse -Force
    Write-Host "Removed build/ directory" -ForegroundColor Green
}
if (Test-Path "dist") {
    Remove-Item -Path "dist" -Recurse -Force
    Write-Host "Removed dist/ directory" -ForegroundColor Green
}
if (Test-Path "PersonalFinanceTracker.spec") {
    Remove-Item -Path "PersonalFinanceTracker.spec" -Force
    Write-Host "Removed PersonalFinanceTracker.spec" -ForegroundColor Green
}

# Install/upgrade dependencies
Write-Host ""
Write-Host "Installing/upgrading dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to upgrade pip" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "Dependencies installed successfully" -ForegroundColor Green

# Build executable with PyInstaller
Write-Host ""
Write-Host "Building executable with PyInstaller..." -ForegroundColor Yellow
Write-Host "This may take several minutes..." -ForegroundColor Yellow

pyinstaller --name="PersonalFinanceTracker" `
    --onefile `
    --windowed `
    --add-data "database;database" `
    --hidden-import PyQt5 `
    --hidden-import matplotlib `
    --hidden-import pandas `
    --icon=resources/app_icon.ico `
    --clean `
    main.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Build failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Verify executable was created
if (Test-Path "dist\PersonalFinanceTracker.exe") {
    $exeSize = (Get-Item "dist\PersonalFinanceTracker.exe").Length / 1MB
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "Build completed successfully!" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Executable: dist\PersonalFinanceTracker.exe" -ForegroundColor Cyan
    Write-Host "Size: $([math]::Round($exeSize, 2)) MB" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "The application will create a database at:" -ForegroundColor Yellow
    Write-Host "$env:USERPROFILE\Documents\FinanceTracker\finance.db" -ForegroundColor Yellow
    Write-Host "on first run." -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "ERROR: Executable was not created" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Read-Host "Press Enter to exit"
