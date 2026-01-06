; Personal Finance Tracker - Inno Setup Installer Script
; Created: January 5, 2026

#define MyAppName "Personal Finance Tracker"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Personal Finance Software"
#define MyAppURL "https://github.com/yourusername/finance-tracker"
#define MyAppExeName "PersonalFinanceTracker.exe"
#define MyAppIcon "resources\app_icon.ico"

[Setup]
; App Information
AppId={{A8F9C2E1-5D4B-4A3C-9E7F-1B2D3E4F5A6B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Installation Directories
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Output
OutputDir=installer_output
OutputBaseFilename=PersonalFinanceTracker-Setup-v{#MyAppVersion}
SetupIconFile={#MyAppIcon}

; Compression
Compression=lzma2/max
SolidCompression=yes

; Windows Version
MinVersion=10.0
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Visual Appearance
WizardStyle=modern
; Using default wizard images
; WizardImageFile=compiler:WizModernImage-IS.bmp
; WizardSmallImageFile=compiler:WizModernSmallImage-IS.bmp

; Privileges
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; License (optional - uncomment if you create LICENSE.txt)
; LicenseFile=LICENSE.txt

; Uninstaller
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Main executable
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Documentation files
Source: "README.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "QUICKSTART.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "VISUAL_GUIDE.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "DISTRIBUTION_GUIDE.md"; DestDir: "{app}\docs"; Flags: ignoreversion

; Icon file
Source: "{#MyAppIcon}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu shortcuts
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\app_icon.ico"
Name: "{group}\Quick Start Guide"; Filename: "{app}\docs\QUICKSTART.md"
Name: "{group}\User Manual"; Filename: "{app}\docs\README.md"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"

; Desktop shortcut (optional - user selects during install)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\app_icon.ico"; Tasks: desktopicon

; Quick Launch shortcut (optional - for older Windows)
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
; Option to launch application after installation
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up any created files
Type: filesandordirs; Name: "{app}\docs"

[Code]
// Custom welcome message
function InitializeSetup(): Boolean;
begin
  Result := True;
  MsgBox('Welcome to Personal Finance Tracker Setup!' + #13#10 + #13#10 +
         'This will install a complete personal finance management application.' + #13#10 + #13#10 +
         'Features include:' + #13#10 +
         '  - Account management (debit & credit)' + #13#10 +
         '  - Transaction tracking' + #13#10 +
         '  - Financial reports & charts' + #13#10 +
         '  - CSV import/export' + #13#10 +
         '  - Backup & restore' + #13#10 + #13#10 +
         'Click OK to continue.',
         mbInformation, MB_OK);
end;

// Show information about data location after installation
procedure CurStepChanged(CurStep: TSetupStep);
var
  DataPath: String;
begin
  if CurStep = ssPostInstall then
  begin
    DataPath := ExpandConstant('{userdocs}\FinanceTracker');
    MsgBox('Installation complete!' + #13#10 + #13#10 +
           'Your financial data will be stored at:' + #13#10 +
           DataPath + #13#10 + #13#10 +
           'Tip: Backup this folder regularly to protect your data.',
           mbInformation, MB_OK);
  end;
end;
