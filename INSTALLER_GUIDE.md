# Personal Finance Tracker - Installer Creation Guide

## 📦 Creating a Professional Windows Installer

### What We're Creating

A professional Windows installer (.exe) that will:
- ✅ Install PersonalFinanceTracker.exe to Program Files
- ✅ Create Start Menu shortcuts
- ✅ Optionally create Desktop shortcut
- ✅ Include documentation
- ✅ Provide uninstaller
- ✅ Show welcome and completion screens

---

## Step 1: Install Inno Setup

### Download Inno Setup

1. **Visit**: https://jrsoftware.org/isdl.php
2. **Download**: Inno Setup 6.x (latest version)
3. **File**: `innosetup-6.x.x.exe` (about 3 MB)

### Install Inno Setup

1. Run the downloaded installer
2. Accept the license agreement
3. Choose installation location (default is fine)
4. Select components:
   - ✅ Inno Setup Compiler (required)
   - ✅ Inno Setup Preprocessor (recommended)
   - ✅ Help Files (recommended)
5. Complete installation
6. No restart required

**Installation Location (Default):**
```
C:\Program Files (x86)\Inno Setup 6\
```

---

## Step 2: Review the Installer Script

The installer script is already created at:
```
C:\Users\georg\Desktop\Personal Financial Tracker\installer.iss
```

### What the Script Does:

**Installer Configuration:**
- App Name: Personal Finance Tracker
- Version: 1.0.0
- Publisher: Personal Finance Software
- Installation Folder: C:\Program Files\Personal Finance Tracker
- Compression: LZMA2 (best)
- Modern wizard style

**Files Included:**
- `PersonalFinanceTracker.exe` - Main application
- `README.md` - User manual
- `QUICKSTART.md` - Quick start guide
- `VISUAL_GUIDE.md` - UI guide
- `DISTRIBUTION_GUIDE.md` - Distribution info
- `app_icon.ico` - Application icon

**Shortcuts Created:**
- Start Menu folder with shortcuts:
  - Personal Finance Tracker (launches app)
  - Quick Start Guide
  - User Manual
  - Uninstall shortcut
- Desktop shortcut (optional - user chooses)
- Quick Launch (for Windows 7)

**Features:**
- Welcome message before installation
- Information about data location after installation
- Option to launch app after installation
- Professional uninstaller
- Requires Windows 10 or later
- 64-bit only

---

## Step 3: Compile the Installer

### Method 1: Using Inno Setup GUI

1. **Open Inno Setup**
   - Start Menu → Inno Setup → Inno Setup Compiler

2. **Open the Script**
   - File → Open
   - Navigate to: `C:\Users\georg\Desktop\Personal Financial Tracker\`
   - Select: `installer.iss`
   - Click Open

3. **Compile**
   - Build → Compile (or press Ctrl+F9)
   - Wait for compilation (takes 10-30 seconds)
   - Watch for "Successful compile" message

4. **Find the Installer**
   - Output location: `installer_output` folder
   - Filename: `PersonalFinanceTracker-Setup-v1.0.0.exe`

### Method 2: Using Command Line

Open Command Prompt and run:

```batch
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "C:\Users\georg\Desktop\Personal Financial Tracker\installer.iss"
```

**Expected Output:**
```
Inno Setup 6.x.x
Copyright (C) 1997-2024 Jordan Russell. All rights reserved.

Compiling...
...
Successful compile (X.XX sec). Resulting Setup program filename is:
C:\Users\georg\Desktop\Personal Financial Tracker\installer_output\PersonalFinanceTracker-Setup-v1.0.0.exe
```

---

## Step 4: Test the Installer

### Before Testing
- Close any running instances of PersonalFinanceTracker
- If you have a previous version installed, uninstall it first

### Testing Steps

1. **Run the Installer**
   ```
   Double-click: PersonalFinanceTracker-Setup-v1.0.0.exe
   ```

2. **Welcome Screen**
   - Read the welcome message
   - Click OK/Next

3. **License Agreement** (if you added one)
   - Review and accept

4. **Installation Location**
   - Default: `C:\Program Files\Personal Finance Tracker`
   - Change if desired or keep default

5. **Additional Options**
   - [ ] Create a desktop shortcut (optional)
   - Click Next

6. **Installation**
   - Watch progress bar
   - Files are copied and shortcuts created

7. **Information**
   - Read about data location
   - Click OK

8. **Completion**
   - [ ] Launch Personal Finance Tracker
   - Click Finish

### Verify Installation

**Check Files:**
```
C:\Program Files\Personal Finance Tracker\
├── PersonalFinanceTracker.exe
├── app_icon.ico
└── docs\
    ├── README.md
    ├── QUICKSTART.md
    ├── VISUAL_GUIDE.md
    └── DISTRIBUTION_GUIDE.md
```

**Check Shortcuts:**
- Start Menu → Personal Finance Tracker folder
  - Personal Finance Tracker
  - Quick Start Guide
  - User Manual
  - Uninstall

- Desktop (if selected)
  - Personal Finance Tracker icon

**Check Uninstaller:**
- Settings → Apps → Personal Finance Tracker
- Uninstall should be available

**Test the App:**
1. Launch from Start Menu
2. Verify it opens correctly
3. Check all features work
4. Verify themes work
5. Test Save/Save As

---

## Step 5: Distribute the Installer

### Installer Details

**Filename:** `PersonalFinanceTracker-Setup-v1.0.0.exe`
**Size:** ~150 MB (includes full application)
**Type:** Self-extracting installer
**Requirements:** Windows 10/11 (64-bit)

### Distribution Methods

**1. Direct Sharing**
- Copy installer to USB drive
- Share via network folder
- Email (if size allows)

**2. Cloud Storage**
- Upload to Google Drive
- Upload to Dropbox
- Upload to OneDrive
- Share download link

**3. Website Hosting**
- Upload to your website
- Create download page
- Add installation instructions

**4. GitHub Release**
- Create GitHub repository
- Create a release
- Upload installer as release asset
- Users download from Releases page

### What to Share

**Minimum:**
- `PersonalFinanceTracker-Setup-v1.0.0.exe`

**Recommended:**
- Installer file
- README.txt with installation instructions
- System requirements

**Example README.txt:**
```
Personal Finance Tracker v1.0 - Installer

SYSTEM REQUIREMENTS:
- Windows 10 or 11 (64-bit)
- 200 MB free disk space
- No other software needed!

INSTALLATION:
1. Double-click PersonalFinanceTracker-Setup-v1.0.0.exe
2. Follow the installation wizard
3. Launch from Start Menu

Your financial data will be stored at:
C:\Users\[YourName]\Documents\FinanceTracker\

For help, see the included documentation in:
Start Menu → Personal Finance Tracker → User Manual

Enjoy tracking your finances!
```

---

## Customization Options

### Update Version Number

Edit `installer.iss`, line 6:
```
#define MyAppVersion "1.0.0"
```

Change to:
```
#define MyAppVersion "1.1.0"
```

### Change Publisher Name

Edit `installer.iss`, line 7:
```
#define MyAppPublisher "Personal Finance Software"
```

### Add License File

1. Create `LICENSE.txt` in project folder
2. Uncomment in `installer.iss`, line 42:
   ```
   LicenseFile=LICENSE.txt
   ```

### Change Icon

Edit `installer.iss`, line 9:
```
#define MyAppIcon "resources\app_icon.ico"
```

Point to your custom icon file.

### Add More Documentation

Edit `installer.iss`, in the `[Files]` section:
```
Source: "YOUR_FILE.md"; DestDir: "{app}\docs"; Flags: ignoreversion
```

---

## Troubleshooting

### Compilation Errors

**Error: Cannot find file**
- Check all file paths in installer.iss
- Ensure PersonalFinanceTracker.exe exists in dist folder
- Verify documentation files exist

**Error: Permission denied**
- Run Inno Setup as Administrator
- Close the application if running
- Check folder permissions

### Installation Issues

**User Account Control Prompt**
- Normal behavior for installers
- Click "Yes" to allow installation

**Cannot install to Program Files**
- Choose different location
- Or run installer as Administrator

**Uninstaller not appearing**
- Restart computer
- Check Windows Registry
- Try reinstalling

---

## Advanced: Silent Installation

For automated/corporate deployment:

### Silent Install
```batch
PersonalFinanceTracker-Setup-v1.0.0.exe /SILENT
```

### Very Silent Install
```batch
PersonalFinanceTracker-Setup-v1.0.0.exe /VERYSILENT
```

### Silent Install with Desktop Icon
```batch
PersonalFinanceTracker-Setup-v1.0.0.exe /SILENT /TASKS="desktopicon"
```

### Silent Uninstall
```batch
"C:\Program Files\Personal Finance Tracker\unins000.exe" /SILENT
```

---

## Installer Script Reference

### Key Sections

**[Setup]** - Installer configuration
- App info, directories, compression settings

**[Files]** - Files to include
- Executable, documentation, resources

**[Icons]** - Shortcuts to create
- Start Menu, Desktop, Quick Launch

**[Run]** - Post-installation actions
- Option to launch app

**[Code]** - Custom Pascal scripts
- Welcome message, post-install info

---

## Build Automation (Optional)

### Create Build Script

`build_installer.bat`:
```batch
@echo off
echo Building installer...

REM Compile the installer
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "installer.iss"

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo Build successful!
echo Installer location: installer_output\PersonalFinanceTracker-Setup-v1.0.0.exe
pause
```

Make executable and run:
```batch
build_installer.bat
```

---

## Checklist

Before releasing the installer:

- [ ] Inno Setup installed
- [ ] Installer script reviewed
- [ ] Version number updated
- [ ] All documentation files present
- [ ] Executable exists in dist folder
- [ ] Installer compiled successfully
- [ ] Tested installation on clean machine
- [ ] Tested application launch
- [ ] Tested all features
- [ ] Tested uninstallation
- [ ] Installer file renamed if needed
- [ ] README created for distribution

---

## Support

### Inno Setup Documentation
- Website: https://jrsoftware.org/isinfo.php
- Help File: Included with installation
- Forum: https://www.jrsoftware.org/ishelp/

### Common Tasks

**Change Install Location:**
Edit `DefaultDirName` in [Setup] section

**Remove Desktop Shortcut Option:**
Remove the "desktopicon" task from [Tasks] section

**Add More Files:**
Add to [Files] section

**Customize Welcome Message:**
Edit the `InitializeSetup` function in [Code] section

---

## Next Steps

1. **Install Inno Setup** (5 minutes)
2. **Compile Installer** (30 seconds)
3. **Test Installer** (2 minutes)
4. **Share with Users!**

---

**Ready to create professional installers!** 📦🚀

Your installer will provide a polished, professional installation experience
for all users of Personal Finance Tracker!
