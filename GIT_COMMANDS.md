# Git Commands Quick Reference

## For Pushing Personal Finance Tracker v1.1 to GitHub

### Quick Deploy (5 Steps)

```bash
# Step 1: Check what changed
git status

# Step 2: Add all changes
git add .

# Step 3: Commit with descriptive message
git commit -m "Release v1.1: Add developer credit and complete build system

- Add 'Developed by George Mikhael' to status bar and About dialog
- Update version to 1.1
- Enhance build scripts and documentation
- Include release executable (103 MB)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Step 4: Push to GitHub
git push -u origin master

# Step 5: Verify
# Visit https://github.com/YOUR_USERNAME/personal-finance-tracker
```

---

## Detailed Commands with Explanations

### 1. Check Current Status
```bash
git status
```
**What it does**: Shows which files have been modified, added, or deleted

**Expected output**:
```
On branch master
Changes not staged for commit:
  modified:   ui/main_window.py
  modified:   README.md
Untracked files:
  BUILD_INSTRUCTIONS.md
  QA_CHECKLIST.md
  ...
```

---

### 2. Review Changes (Optional but Recommended)
```bash
# See detailed changes in a file
git diff ui/main_window.py

# See summary of all changes
git diff --stat

# See list of new files
git ls-files --others --exclude-standard
```

---

### 3. Stage Changes

#### Add All Files:
```bash
git add .
```

#### Or Add Specific Files:
```bash
# Source code changes
git add ui/main_window.py
git add README.md

# Build scripts
git add build_windows.bat
git add build_release.ps1
git add .gitignore

# Documentation
git add BUILD_INSTRUCTIONS.md
git add DEPLOYMENT_GUIDE.md
git add QA_CHECKLIST.md
git add QA_TEST_RESULTS.md
git add GIT_COMMANDS.md

# Release
git add release/PersonalFinanceTracker.exe
```

---

### 4. Commit Changes

#### Recommended Commit Message:
```bash
git commit -m "Release v1.1: Add developer credit and complete build system

- Add 'Developed by George Mikhael' to status bar footer (visible on all screens)
- Add developer credit to About dialog with professional styling
- Update application version from 1.0 to 1.1
- Enhance build_windows.bat with cleanup and better error handling
- Create build_release.ps1 PowerShell build script
- Update .gitignore to allow release/*.exe files
- Create comprehensive BUILD_INSTRUCTIONS.md
- Create DEPLOYMENT_GUIDE.md with Git workflow
- Create QA_CHECKLIST.md with 44 test cases
- Document QA results in QA_TEST_RESULTS.md
- Update README.md with version 1.1 and developer attribution
- Generate release build: PersonalFinanceTracker.exe (103 MB)

Build verified:
- PyInstaller 6.16.0 successful build
- All dependencies bundled correctly
- Standalone executable tested
- No build warnings or errors

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

#### Alternative Short Message:
```bash
git commit -m "v1.1: Add developer credit by George Mikhael

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### 5. Verify Commit
```bash
# View the commit you just made
git log -1

# View files included in commit
git show --name-only

# View detailed changes in commit
git show
```

---

### 6. Push to Remote Repository

#### If remote is already configured:
```bash
git push origin master
```

#### If this is your first push:
```bash
git push -u origin master
```
The `-u` flag sets up tracking so future pushes only need `git push`

#### If you're on 'main' branch instead of 'master':
```bash
git push -u origin main
```

---

## Setting Up Remote (First Time Only)

If you haven't connected to GitHub yet:

```bash
# Check if remote exists
git remote -v

# If no remote, add it (replace with your GitHub URL)
git remote add origin https://github.com/YOUR_USERNAME/personal-finance-tracker.git

# Verify it was added
git remote -v

# Now push
git push -u origin master
```

---

## Troubleshooting

### Error: "fatal: not a git repository"
```bash
# Initialize git repository
git init

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/personal-finance-tracker.git

# Continue with add, commit, push
```

### Error: "Updates were rejected because the remote contains work"
```bash
# Pull remote changes first
git pull origin master --rebase

# Then push
git push origin master
```

### Error: Authentication failed
```bash
# Use Personal Access Token instead of password
# Generate token at: https://github.com/settings/tokens

# Or use SSH instead of HTTPS
git remote set-url origin git@github.com:YOUR_USERNAME/personal-finance-tracker.git
```

### Error: "large file detected" (for .exe)
This is normal for the 103 MB executable.

**Option 1**: Keep in repository (works if < 100 MB... ours is 103 MB)
**Option 2**: Use Git LFS
```bash
git lfs install
git lfs track "*.exe"
git add .gitattributes
git add release/PersonalFinanceTracker.exe
git commit -m "Add exe with LFS"
git push
```

**Option 3**: Only include in Releases (recommended)
```bash
# Remove from git tracking
git rm --cached release/PersonalFinanceTracker.exe

# Update .gitignore to exclude it
echo "release/*.exe" >> .gitignore

# Commit
git add .gitignore
git commit -m "Remove exe from repo, will add to releases"
git push

# Then upload .exe manually in GitHub Releases
```

---

## After Pushing: Create GitHub Release

### Via Web Interface (Easiest)

1. Go to your repository on GitHub
2. Click **"Releases"** (right sidebar)
3. Click **"Draft a new release"**
4. Fill in:
   - **Tag**: `v1.1`
   - **Title**: `Personal Finance Tracker v1.1`
   - **Description**: See DEPLOYMENT_GUIDE.md for template
5. **Upload** `PersonalFinanceTracker.exe` (drag & drop)
6. Click **"Publish release"**

### Via GitHub CLI

```bash
# Install GitHub CLI: https://cli.github.com/

# Create release and upload executable
gh release create v1.1 \
  release/PersonalFinanceTracker.exe \
  --title "Personal Finance Tracker v1.1" \
  --notes "Release v1.1 - Developed by George Mikhael

Features:
- Developer credit in UI
- Enhanced build system
- Comprehensive documentation
- Standalone Windows executable

Download PersonalFinanceTracker.exe to get started!"
```

---

## Complete Workflow Summary

```bash
# 1. Review changes
git status
git diff

# 2. Stage changes
git add .

# 3. Commit
git commit -m "Release v1.1: Add developer credit and complete build system

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# 4. Push
git push -u origin master

# 5. Create release on GitHub (web interface)
```

---

## Useful Git Commands

### View History
```bash
# View commit history
git log

# View last 5 commits
git log -5

# View commit history with file names
git log --name-status

# View graphical commit history
git log --graph --oneline --all
```

### Undo Changes

```bash
# Undo changes to a file (before staging)
git checkout -- filename

# Unstage a file
git reset HEAD filename

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes) ⚠️
git reset --hard HEAD~1
```

### Branch Management
```bash
# View current branch
git branch

# Create new branch
git checkout -b feature-branch

# Switch branch
git checkout master

# Merge branch
git merge feature-branch

# Delete branch
git branch -d feature-branch
```

---

## GitHub Repository Setup Tips

### Update Repository Settings on GitHub

1. **Description**:
   ```
   Personal Finance Tracker - Simple desktop app for managing finances,
   tracking transactions, and generating reports. Built with Python & PyQt5.
   ```

2. **Topics** (comma-separated):
   ```
   finance, budget, python, pyqt5, desktop-app, sqlite, personal-finance,
   expense-tracker, accounting, budgeting-app, financial-tracker
   ```

3. **Website**: Link to releases or documentation

4. **Make Public/Private**: Choose visibility

---

## Next Steps After Pushing

✅ **Verify on GitHub**
- Check all files are present
- Ensure README displays correctly
- Verify release/ folder contains .exe

✅ **Create a Release**
- Upload PersonalFinanceTracker.exe
- Add release notes
- Tag as v1.1

✅ **Test**
- Clone repository to new location
- Build from source
- Test executable download

✅ **Share**
- Share repository link
- Share release download link
- Update project documentation

---

**Quick Reference Version**: 1.0
**For**: Personal Finance Tracker v1.1
**Developed by**: George Mikhael
**Last Updated**: January 5, 2026
