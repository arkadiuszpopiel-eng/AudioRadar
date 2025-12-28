# Pre-Build Checklist - Radar Games ML v4.3.1-k0006

Before running `RUN_BUILD_Win.cmd`, verify all items below.

**Last Updated:** 2025-12-16
**Version:** 4.3.1-k0006

---

## ✅ MANDATORY CHECKS (DO NOT SKIP!)

### 1. Python Syntax Verification
```cmd
python -m py_compile app/core/logger.py
python -m py_compile app/core/paths.py
python -m py_compile app/core/log_aggregator.py
python -m py_compile app/utils/audio_device_monitor.py
python -m py_compile app/diagnostics/selftest.py
python -m py_compile app/ui/event_handlers.py
python -m py_compile app/version.py
```
**Expected:** No output = SUCCESS

---

### 2. Module Import Test
```cmd
python -c "import sys; sys.path.insert(0, 'app'); from core import logger, paths, log_aggregator; from utils import audio_device_monitor; print('✓ All imports OK')"
```
**Expected:** `✓ All imports OK`

---

### 3. Spec File Verification
```cmd
# Check hiddenimports include new modules
findstr /C:"log_aggregator" build_tools\radarsuite_windows.spec
findstr /C:"audio_device_monitor" build_tools\radarsuite_windows.spec
findstr /C:"paths" build_tools\radarsuite_windows.spec
```
**Expected:** All 3 should return matches

---

### 4. Dependencies Check
```cmd
python -m pip list | findstr /I "PyQt5 numpy sounddevice psutil PyInstaller"
```
**Expected:** All packages listed with versions

---

### 5. Version Consistency
```cmd
python -c "import sys; sys.path.insert(0, 'app'); from version import __version_full__; print(__version_full__)"
```
**Expected:** `4.3.1-k0006`

---

## ⚠️ RECOMMENDED CHECKS

### 6. Frozen Mode Compatibility
```cmd
# Verify frozen mode handling
findstr /C:"getattr.*frozen" app\core\logger.py
findstr /C:"getattr.*frozen" app\core\paths.py
```
**Expected:** Both should show frozen mode handling

---

### 7. Circular Import Prevention
```cmd
# Verify lazy imports in logger.py
findstr /C:"_get_log_file_path" app\core\logger.py
```
**Expected:** Should show lazy path computation function

---

### 8. Git Status Clean
```cmd
git status
```
**Expected:** "nothing to commit, working tree clean" OR only untracked files

---

## 🚀 BUILD EXECUTION

If all checks pass, run:

```cmd
RUN_BUILD_Win.cmd
```

### Expected Output:
```
[STEP 1/6] Checking Python...
   - Python version: 3.11.x
[STEP 2/6] Checking dependencies...
   - PyQt5: OK
   - numpy: OK
   - sounddevice: OK
   - ...
[STEP 3/6] Verifying installation...
   - All modules verified
[STEP 4/6] Building EXE with PyInstaller...
   - EXE built successfully!
BUILD COMPLETED SUCCESSFULLY!
```

### Build Artifacts:
```
dist/Radar_Games_ML/Radar_Games_ML.exe  ← Main executable
Radar_Games_ML.exe                      ← Copy in root (quick launch)
log/build_windows.log                   ← Build log
all_logs/build/build_windows.log        ← Log copy
```

---

## ❌ COMMON BUILD ERRORS & FIXES

### Error: "ModuleNotFoundError: No module named 'app.core.log_aggregator'"
**Cause:** spec file missing hiddenimport
**Fix:** Verify spec file has all modules (see Check #3)

### Error: "ImportError: DLL load failed"
**Cause:** Missing Visual C++ Redistributable
**Fix:** Install: https://aka.ms/vs/17/release/vc_redist.x64.exe

### Error: "FileNotFoundError: [WinError 2] main.py"
**Cause:** Wrong working directory
**Fix:** Run from project root: `cd /d Radar_Games_ML_v4.3`

### Error: "SyntaxError: invalid syntax"
**Cause:** Python file has syntax error
**Fix:** Run Check #1 to find broken file

### Error: "circular import detected"
**Cause:** Module imports at module level
**Fix:** Verify lazy imports (Check #7)

---

## 🧪 POST-BUILD TESTING

After successful build, test the EXE:

### 1. Launch Test
```cmd
Radar_Games_ML.exe
```
**Expected:** Main window opens without errors

### 2. Log Verification
```cmd
dir log\super_log.txt
type log\super_log.txt
```
**Expected:** Log file created with startup messages

### 3. Audio Device Test
```cmd
# In app: Tab 2 → Click "Rescan Devices"
```
**Expected:** Devices listed in dropdown

### 4. Self-Test
```cmd
# In app: Click "TEST" button (if available)
```
**Expected:** Self-test passes

### 5. Language Switch Test
```cmd
# In app: Click "EN/PL" button
```
**Expected:** All tab titles update instantly (no restart)

---

## 📊 BUILD VERIFICATION SUMMARY

| Check | Status | Critical |
|-------|--------|----------|
| Python syntax | ⬜ | ✅ YES |
| Module imports | ⬜ | ✅ YES |
| Spec file | ⬜ | ✅ YES |
| Dependencies | ⬜ | ✅ YES |
| Version | ⬜ | ⚠️ Recommended |
| Frozen mode | ⬜ | ⚠️ Recommended |
| Circular imports | ⬜ | ⚠️ Recommended |
| Git status | ⬜ | ⚠️ Recommended |

**Minimum Required:** All ✅ YES checks must pass

---

## 📞 IF BUILD FAILS

1. Check `log/build_windows.log` for errors
2. Copy last 50 lines: `powershell -Command "Get-Content log\build_windows.log -Tail 50"`
3. Look for error patterns:
   - "ModuleNotFoundError" → missing hiddenimport
   - "ImportError: DLL" → missing dependency
   - "SyntaxError" → broken Python file
   - "FileNotFoundError" → wrong directory

4. Verify all MANDATORY CHECKS passed
5. Check `docs/BUILD.md` for detailed troubleshooting

---

**Radar Games ML v4.3.1-k0006** - Pre-build verification checklist.
