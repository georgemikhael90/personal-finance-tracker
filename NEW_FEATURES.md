# Personal Finance Tracker - New Features v1.1

## 🎨 NEW FEATURES ADDED!

### 1. Theme Support (3 Themes)

**Access**: View Menu → Theme

#### Available Themes:

**1. White (Light Mode)** - Default
- Clean, professional light theme
- High contrast for readability
- Blue accent colors
- Perfect for daytime use

**2. Night (Dark Mode)**
- Pure dark theme with purple accents
- Easy on the eyes in low light
- Black/dark gray backgrounds
- Purple (#bb86fc) highlights

**3. Night Blue**
- Dark blue theme with cyan accents
- Navy blue backgrounds (#0d1b2a)
- Cyan (#4fc3f7) highlights
- Professional dark appearance

**Features:**
- ✅ Theme selection persists between sessions
- ✅ Instant theme switching
- ✅ All UI elements themed consistently
- ✅ Applies to all tabs and dialogs

**How to Use:**
1. Click **View** menu
2. Select **Theme**
3. Choose your preferred theme
4. Theme is applied immediately and saved

---

### 2. Save & Save As Functions

**Access**: File Menu → Save Report / Save Report As

#### Save Options:

**Save Report** (Ctrl+S)
- Quickly save to last used location
- Saves current data/report
- No dialog if location known

**Save Report As** (Ctrl+Shift+S)
- Choose new filename and location
- Multiple format options
- Smart default naming

#### Supported Formats:

**1. CSV Format (.csv)**
- Exports all transactions
- Compatible with Excel, Google Sheets
- Easy data portability
- Standard format: date, account, category, type, amount, description

**2. JSON Format (.json)**
- Complete data export
- Includes accounts, categories, and transactions
- Structured data format
- Easy to parse programmatically
- Contains export date metadata

**3. PDF Format (.pdf)**
- Saves current chart/report as PDF
- High quality (300 DPI)
- Perfect for printing
- Available from Reports tab
- Professional document output

**Features:**
- ✅ Smart file naming (includes date)
- ✅ Remember last save location
- ✅ Multiple export formats
- ✅ Full data backup in JSON
- ✅ Print-ready PDFs

**How to Use:**

**Quick Save:**
1. Work on a report or view data
2. Press Ctrl+S or File → Save Report
3. Saves to last location (or prompts if first time)

**Save As:**
1. File → Save Report As (or Ctrl+Shift+S)
2. Choose format (PDF/CSV/JSON)
3. Select location and filename
4. Click Save

**Use Cases:**
- Export transactions to CSV for external analysis
- Save full backup as JSON
- Print charts as PDF for presentations
- Archive monthly reports

---

### 3. Settings Persistence

**Automatically Saves:**
- Current theme selection
- Last save file location
- Window preferences

**Stored At:**
Windows Registry: `HKEY_CURRENT_USER\Software\PersonalFinanceTracker\Settings`

**Features:**
- ✅ Theme remembered between sessions
- ✅ No manual configuration needed
- ✅ Per-user settings

---

## 📋 Updated Menu Structure

### File Menu
```
File
├── Save Report...             (Ctrl+S)     ← NEW!
├── Save Report As...          (Ctrl+Shift+S)  ← NEW!
├── ──────────────────
├── Import from CSV...
├── Export to CSV...
├── ──────────────────
├── Create Backup...
├── Restore from Backup...
├── ──────────────────
└── Exit
```

### View Menu
```
View                                      ← NEW MENU!
└── Theme
    ├── ○ White (Light)                   ← NEW!
    ├── ○ Night (Dark)                    ← NEW!
    └── ○ Night Blue                      ← NEW!
```

### Help Menu
```
Help
└── About
```

---

## 🎯 Quick Reference

### Keyboard Shortcuts
- **Ctrl+S** - Save Report
- **Ctrl+Shift+S** - Save Report As
- **Alt** - Access menu bar

### Theme Switching
1. View → Theme → Select your theme
2. Theme applies instantly
3. Saved automatically

### Saving Reports
1. **CSV**: All transactions in spreadsheet format
2. **JSON**: Complete database export
3. **PDF**: Current chart/report (from Reports tab)

---

## 🔄 Upgrade Notes

### What's New in This Version

**Version 1.1** (Current)
- ✅ 3 beautiful themes
- ✅ Save/Save As functionality
- ✅ Settings persistence
- ✅ PDF export for charts
- ✅ JSON full data export
- ✅ Improved About dialog

**Version 1.0** (Previous)
- Initial release
- All core features

### Compatibility
- Settings from v1.0 are preserved
- Database format unchanged
- No data migration needed
- Fully backward compatible

---

## 💡 Usage Tips

### Theme Selection
- **Office/Daytime**: Use White theme
- **Evening/Night**: Use Night or Night Blue
- **Presentations**: Night Blue looks professional
- **Eye Strain**: Dark themes reduce eye fatigue

### Export Strategy
- **Daily backup**: Use JSON format
- **Spreadsheet analysis**: Use CSV format
- **Presentations/Printing**: Use PDF format
- **Archive reports**: Save monthly PDFs

### Best Practices
1. Set your preferred theme on first launch
2. Save reports regularly to different formats
3. Use Ctrl+S for quick saves
4. Export to JSON monthly for full backups

---

## 🔧 Technical Details

### Theme Implementation
- Pure CSS/Qt StyleSheets
- No external dependencies
- Instant switching
- Memory efficient

### File Formats

**CSV Structure:**
```csv
date,account,category,type,amount,description
2026-01-05,Checking Account,Groceries,expense,50.0,Weekly groceries
```

**JSON Structure:**
```json
{
  "accounts": [...],
  "categories": [...],
  "transactions": [...],
  "export_date": "2026-01-05"
}
```

**PDF Output:**
- Format: PDF 1.4
- DPI: 300
- Color Mode: RGB
- Compression: Enabled

### Settings Storage
- Backend: QSettings (Qt framework)
- Windows: Registry (HKCU)
- Per-user configuration
- Automatic persistence

---

## 📊 Feature Comparison

| Feature | v1.0 | v1.1 |
|---------|------|------|
| Accounts Management | ✅ | ✅ |
| Transactions | ✅ | ✅ |
| Reports & Charts | ✅ | ✅ |
| CSV Import | ✅ | ✅ |
| CSV Export | ✅ | ✅ |
| Backup/Restore | ✅ | ✅ |
| **Themes** | ❌ | ✅ NEW! |
| **Save/Save As** | ❌ | ✅ NEW! |
| **PDF Export** | ❌ | ✅ NEW! |
| **JSON Export** | ❌ | ✅ NEW! |
| **Settings Persistence** | ❌ | ✅ NEW! |

---

## 🎨 Theme Previews

### White Theme (Default)
- Background: White (#ffffff)
- Text: Black (#000000)
- Accent: Blue (#0078d4)
- Style: Clean, professional

### Night Theme
- Background: Dark Gray (#1e1e1e)
- Text: Light Gray (#e0e0e0)
- Accent: Purple (#bb86fc)
- Style: Modern, easy on eyes

### Night Blue Theme
- Background: Navy (#0d1b2a)
- Text: Light Blue (#e0e8f0)
- Accent: Cyan (#4fc3f7)
- Style: Professional, elegant

---

## 🚀 What's Next?

### Planned Features (Future)
- More theme options
- Custom theme editor
- Scheduled reports
- Automated backups
- Email export
- Cloud sync (optional)

---

## 📝 Release Info

**Version**: 1.1
**Release Date**: January 5, 2026
**Changes**: 3 major features added
**Compatibility**: Windows 10/11
**Upgrade**: Rebuild executable with new features

---

**All new features are production-ready and tested!** 🎉
