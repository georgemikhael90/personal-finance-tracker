# Build Instructions

This document provides comprehensive instructions for building the Personal Finance Tracker executable from source.

## Prerequisites

### Required Software
- **Python 3.10 or higher** ([Download](https://python.org/downloads/))
  - During installation, ensure "Add Python to PATH" is checked
- **Git** (for cloning the repository)
- **Windows 10/11** (primary target platform)

### Verify Installation
```batch
python --version
pip --version
git --version
```

## Building the Executable

### Method 1: Using Batch Script (Recommended for Windows)

1. **Open Command Prompt** in the project directory:
   ```batch
   cd C:\Users\georg\OneDrive\Documents\GitHub\personal-finance-tracker
   ```

2. **Run the build script**:
   ```batch
   build_windows.bat
   ```

3. **Wait for completion** (typically 2-5 minutes)

4. **Find the executable**:
   ```
   dist\PersonalFinanceTracker.exe
   ```

### Method 2: Using PowerShell Script

1. **Open PowerShell** in the project directory:
   ```powershell
   cd C:\Users\georg\OneDrive\Documents\GitHub\personal-finance-tracker
   ```

2. **Allow script execution** (if needed):
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Run the build script**:
   ```powershell
   .\build_release.ps1
   ```

4. **Wait for completion** and find the executable in `dist\`

### Method 3: Manual Build (Advanced)

1. **Install dependencies**:
   ```batch
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Run PyInstaller**:
   ```batch
   pyinstaller --name="PersonalFinanceTracker" ^
       --onefile ^
       --windowed ^
       --add-data "database;database" ^
       --hidden-import PyQt5 ^
       --hidden-import matplotlib ^
       --hidden-import pandas ^
       --icon=resources/app_icon.ico ^
       --clean ^
       main.py
   ```

3. **Locate the executable**:
   ```
   dist\PersonalFinanceTracker.exe
   ```

## Build Output

### Directory Structure After Build
```
personal-finance-tracker/
├── build/                          # PyInstaller temp files (can be deleted)
├── dist/
│   └── PersonalFinanceTracker.exe  # Final executable (~40-50 MB)
├── PersonalFinanceTracker.spec     # PyInstaller configuration
└── ... (source files)
```

### Executable Details
- **File**: PersonalFinanceTracker.exe
- **Size**: ~40-50 MB (includes Python runtime and all dependencies)
- **Type**: Standalone Windows executable
- **Dependencies**: None (fully self-contained)
- **Data Storage**: Creates database at `%USERPROFILE%\Documents\FinanceTracker\finance.db`

## Build Configuration

### PyInstaller Options Explained
- `--name="PersonalFinanceTracker"`: Output executable name
- `--onefile`: Bundle everything into a single .exe
- `--windowed`: GUI application (no console window)
- `--add-data "database;database"`: Include database schema files
- `--hidden-import PyQt5`: Ensure PyQt5 is fully included
- `--hidden-import matplotlib`: Include matplotlib for charts
- `--hidden-import pandas`: Include pandas for CSV handling
- `--icon=resources/app_icon.ico`: Application icon
- `--clean`: Clean cache before building

### Included Dependencies
See `requirements.txt` for full list:
- PyQt5 >= 5.15.10 (GUI framework)
- matplotlib >= 3.8.0 (Charts)
- pandas >= 2.2.0 (CSV handling)
- numpy >= 1.26.0 (Required by pandas)
- pyinstaller >= 6.0.0 (Build tool)

## Creating a Release Build

### Step 1: Build the Executable
```batch
build_windows.bat
```

### Step 2: Create Release Directory
```batch
mkdir release
copy dist\PersonalFinanceTracker.exe release\
```

### Step 3: Test the Executable
1. Navigate to `release\` directory
2. Double-click `PersonalFinanceTracker.exe`
3. Verify application launches successfully
4. Test basic functionality (add account, transaction, etc.)

### Step 4: Prepare Distribution Package
The release package should include:
- `PersonalFinanceTracker.exe` - The application
- `README.md` - User documentation
- `LICENSE` - License file

## Troubleshooting

### Build Fails: "Python not found"
**Solution**: Install Python 3.10+ and ensure it's in PATH
```batch
python --version
```
If this fails, reinstall Python and check "Add Python to PATH"

### Build Fails: "pip not found"
**Solution**: Reinstall Python or run:
```batch
python -m ensurepip --upgrade
```

### Build Fails: "PyInstaller not found"
**Solution**: Install PyInstaller:
```batch
pip install pyinstaller
```

### Build Fails: Module Import Errors
**Solution**: Ensure all dependencies are installed:
```batch
pip install -r requirements.txt --force-reinstall
```

### Executable Too Large
**Normal**: The executable is 40-50 MB because it includes:
- Complete Python runtime
- PyQt5 (large GUI framework)
- matplotlib (visualization library)
- All other dependencies

### Executable Fails to Run
**Check**:
1. Windows Defender/Antivirus isn't blocking it
2. Run from Command Prompt to see error messages:
   ```batch
   cd dist
   PersonalFinanceTracker.exe
   ```
3. Ensure you have write permissions to `%USERPROFILE%\Documents\`

### "VCRUNTIME140.dll not found"
**Solution**: Install Microsoft Visual C++ Redistributable:
- [Download from Microsoft](https://aka.ms/vs/17/release/vc_redist.x64.exe)

## Clean Build

To perform a completely clean build:

```batch
# Delete all build artifacts
rmdir /s /q build
rmdir /s /q dist
del PersonalFinanceTracker.spec

# Rebuild
build_windows.bat
```

## Version Information

- **Application Version**: 1.1
- **Python Version**: 3.10+
- **Target Platform**: Windows 10/11 (64-bit)
- **Build Tool**: PyInstaller 6.0+

## Distribution Notes

### For End Users
- The `.exe` file is fully standalone
- No Python installation required
- No additional dependencies needed
- Works on any Windows 10/11 PC

### For Developers
- Source code is in the repository
- Build from source using scripts provided
- All dependencies listed in `requirements.txt`

## Security Notes

### Antivirus False Positives
PyInstaller executables sometimes trigger antivirus warnings because:
1. They are self-extracting archives
2. They modify the filesystem (create database)
3. PyInstaller is commonly used (legitimate and malicious software)

**If flagged**:
- Add exception in antivirus software
- Build from source yourself to verify safety
- The source code is fully auditable

### Code Signing (Optional)
For production distribution, consider:
1. Obtaining a code signing certificate
2. Signing the executable with `signtool`
3. This reduces antivirus false positives

## Continuous Integration (Future)

For automated builds, consider setting up:
- GitHub Actions workflow
- Automated testing before build
- Automatic release creation
- Version number management

## Build Verification Checklist

After building, verify:
- [ ] Executable exists in `dist\` directory
- [ ] File size is ~40-50 MB
- [ ] Double-clicking launches the application
- [ ] Main window appears correctly
- [ ] Can create an account
- [ ] Can add a transaction
- [ ] Can view reports
- [ ] Database is created in Documents folder
- [ ] Application closes cleanly

## Support

For build issues:
1. Check this document's troubleshooting section
2. Verify all prerequisites are met
3. Try a clean build
4. Check PyInstaller logs in `build\` directory

---

**Last Updated**: January 2026
**Developed by**: George Mikhael
