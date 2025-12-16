# Recovery & Backup Guide - Radar Games ML v4.3.1-k0006

Complete guide for backing up and recovering Radar Games ML project.

**Last Updated:** 2025-12-16
**Version:** 4.3.1-k0006

---

## Table of Contents

1. [Critical Files & Directories](#critical-files--directories)
2. [Full Project Backup](#full-project-backup)
3. [Configuration Backup](#configuration-backup)
4. [Recovery from Backup](#recovery-from-backup)
5. [Module-by-Module Rebuild Guide](#module-by-module-rebuild-guide)
6. [UI Structure Documentation](#ui-structure-documentation)
7. [Known Issues & Fixes](#known-issues--fixes)

---

## Critical Files & Directories

### ✅ MUST BACKUP (Core Application)

```
Radar_Games_ML_v4.3/
├── app/                          # ❗ CRITICAL - All application code
│   ├── core/                     # Configuration, logger, paths, DI
│   ├── audio/                    # Audio engine, processing
│   ├── detection/                # Footstep, shot, machine detection
│   ├── tracking/                 # Target tracking, threat assessment
│   ├── ui/                       # UI builder, event handlers
│   ├── widgets/                  # Radar, LED, panels
│   ├── utils/                    # Game detector, audio scanner
│   ├── ml/                       # ML training pipeline
│   ├── diagnostics/              # Self-test system
│   └── main.py                   # ❗ MAIN ENTRY POINT
│
├── docs/                         # ❗ Documentation
│   ├── ARCHITECTURE.md
│   ├── MODULES.md
│   ├── USAGE.md
│   ├── API.md
│   ├── KNOWN_ISSUES.md
│   └── CHANGELOG.md
│
├── build_tools/                  # ❗ PyInstaller specs
│   └── radarsuite_windows.spec
│
├── RUN_BUILD_Win.cmd             # ❗ Build scripts
├── RUN_BUILD_ALL_Win.cmd
├── RUN_BUILD_FIXED.cmd
├── SYNC_ALL_LOGS.cmd             # Log synchronization
│
├── README_V4.3.md                # ❗ Main README
├── .gitignore
└── requirements.txt              # Python dependencies
```

### ⚠️ BACKUP IF MODIFIED (User Data)

```
├── Data/                         # ML training sessions
├── Models/                       # Trained ML models
├── log/                          # Runtime logs (can regenerate)
├── raport/                       # Test reports (can regenerate)
└── all_logs/                     # Log copies (can regenerate)
```

### ❌ DO NOT BACKUP (Auto-generated)

```
├── __pycache__/                  # Python cache
├── build/                        # PyInstaller temp
├── dist/                         # PyInstaller output
├── *.pyc, *.pyo                  # Compiled Python
└── Radar_Games_ML.exe            # Built executable
```

---

## Full Project Backup

### Method 1: Git Repository (RECOMMENDED)

```bash
# Clone from remote
git clone <your-repo-url> Radar_Games_ML_v4.3_backup

# Or create archive
git archive -o Radar_Games_ML_v4.3_k0006_backup.zip HEAD
```

### Method 2: Manual Archive

**Windows:**
```cmd
# Create timestamped backup
powershell Compress-Archive -Path "Radar_Games_ML_v4.3" -DestinationPath "Radar_Games_ML_v4.3_backup_%date:~-4%%date:~3,2%%date:~0,2%.zip"
```

**Linux/Mac:**
```bash
# Create timestamped tar.gz
tar -czf "Radar_Games_ML_v4.3_backup_$(date +%Y%m%d).tar.gz" Radar_Games_ML_v4.3/
```

### What to Include

**Minimal Backup** (Code only - ~50MB):
```
✓ app/
✓ docs/
✓ build_tools/
✓ *.cmd (build scripts)
✓ README_V4.3.md
✓ requirements.txt
✓ .gitignore
```

**Full Backup** (Code + Data - ~500MB+):
```
✓ Everything from Minimal
✓ Data/ (ML sessions)
✓ Models/ (trained models)
✓ log/ (if you want logs)
✓ raport/ (if you want reports)
```

---

## Configuration Backup

### User Configuration File

**Location:**
```
Windows: %APPDATA%\Radar Games ML\config.json
Linux: ~/.config/Radar_Games_ML/config.json
```

**Backup Command (Windows):**
```cmd
copy "%APPDATA%\Radar Games ML\config.json" "config_backup_%date:~-4%%date:~3,2%%date:~0,2%.json"
```

**Configuration Contents:**
- Audio device settings
- Detection thresholds
- UI preferences (language, theme)
- Window positions
- ML model paths

---

## Recovery from Backup

### Full Recovery Steps

1. **Extract Backup:**
   ```cmd
   # Windows
   powershell Expand-Archive -Path "backup.zip" -DestinationPath "C:\Projects\"

   # Linux
   tar -xzf backup.tar.gz -C /home/user/
   ```

2. **Install Python Dependencies:**
   ```cmd
   cd Radar_Games_ML_v4.3
   python -m pip install -r requirements.txt
   ```

3. **Verify Structure:**
   ```cmd
   python app/main.py
   ```

4. **Restore Configuration (Optional):**
   ```cmd
   copy config_backup.json "%APPDATA%\Radar Games ML\config.json"
   ```

5. **Run Self-Test:**
   ```cmd
   # In app, click "TEST" button
   # Or run: python -c "from app.diagnostics.selftest import SelfTestRunner; SelfTestRunner().run_quick()"
   ```

---

## Module-by-Module Rebuild Guide

If you need to rebuild from scratch, follow this dependency order:

### Phase 1: Core Foundation
```
1. app/core/constants.py       # Constants first
2. app/core/paths.py            # Path management
3. app/core/logger.py           # Logging system
4. app/core/config.py           # Configuration
5. app/core/di.py               # Dependency injection
6. app/version.py               # Version management
```

### Phase 2: Audio System
```
7. app/audio/engine.py          # Audio engine
8. app/audio/processor.py       # Audio processing
9. app/audio/fft.py             # FFT analysis
```

### Phase 3: Detection & Classification
```
10. app/detection/footstep.py   # Footstep detection
11. app/detection/shot.py       # Shot detection
12. app/detection/machine.py    # Machine detection
13. app/detection/classifier.py # Sound classifier
```

### Phase 4: Tracking
```
14. app/tracking/target.py      # Target tracking
15. app/tracking/threat.py      # Threat assessment
```

### Phase 5: UI
```
16. app/ui/builder.py           # UI builder
17. app/ui/event_handlers.py    # Event handling
18. app/widgets/*               # All widgets
19. app/main.py                 # Main window
```

### Phase 6: Utilities
```
20. app/utils/*                 # Game detector, audio scanner
21. app/ml/*                    # ML training (optional)
22. app/diagnostics/*           # Self-test (optional)
```

---

## UI Structure Documentation

### Main Window Structure

```python
MainWindow (QMainWindow)
├── Toolbar
│   ├── START/STOP button
│   ├── REC button (record ML sessions)
│   ├── Language toggle (EN/PL)
│   ├── Detach Radar button
│   └── Detach LED button
│
├── Main Tabs (QTabWidget: main_tabs)
│   ├── Tab 0: Radar View
│   │   └── Sub-tabs (QTabWidget: radar_tabs)
│   │       ├── Sub-tab 0: Military HUD (2D radar)
│   │       └── Sub-tab 1: 3D Wallhack (3D radar)
│   │
│   ├── Tab 1: Detection & Audio
│   │   ├── DevicePanel (device selection)
│   │   ├── DetectionPanel (waveform, spectrum)
│   │   └── Controls (thresholds, filters)
│   │
│   ├── Tab 2: Game Detection
│   │   ├── Game selector dropdown
│   │   ├── Auto-detection checkbox
│   │   └── Status indicators
│   │
│   ├── Tab 3: Analysis
│   │   ├── Target history table
│   │   ├── Event log
│   │   └── Statistics charts
│   │
│   └── Tab 4: ML Training
│       ├── Session recorder
│       ├── Model manager
│       └── Training controls
│
└── Status Bar
    ├── Status message
    ├── FPS counter
    └── Target count
```

### Widget Classes Reference

| Widget | File | Purpose |
|--------|------|---------|
| `MilitaryHUDRadar` | `widgets/military_hud.py` | 2D circular radar |
| `Military3DRadar` | `widgets/military_3d.py` | 3D perspective radar |
| `LEDOverlay` | `widgets/led.py` | Directional LED indicator |
| `DevicePanel` | `widgets/device_panel.py` | Audio device selection |
| `DetectionPanel` | `widgets/detection_panel.py` | Waveform/spectrum display |
| `MLTrainingPanel` | `widgets/ml_training_panel.py` | ML training UI |

### Translation Keys

All UI text uses translation system. Key patterns:

```python
# Tabs
tr('tab_radar_view')         # "Radar View" / "Widok Radaru"
tr('tab_detection_audio')    # "Detection & Audio"
tr('tab_game_detection')     # "Game Detection"
tr('tab_analysis')           # "Analysis" / "Analiza"
tr('tab_ml_training')        # "ML Training" / "Trening ML"

# Sub-tabs
tr('military_hud')           # "Military HUD"
tr('3d_wallhack')            # "3D Wallhack"

# See: app/core/translations.py for complete list
```

---

## Known Issues & Fixes

### Issue: Logs Not Writing
**Fix:** See `docs/KNOWN_ISSUES.md` - Fixed in k0004 (circular import)

### Issue: UI Freeze on Button Press
**Fix:** See `docs/KNOWN_ISSUES.md` - Fixed in k0002 (non-blocking detection)

### Issue: Language Switch Requires Restart
**Fix:** See `docs/KNOWN_ISSUES.md` - Fixed in k0006 (dynamic updates)

### Issue: Bluetooth Audio Switching
**Fix:** See `docs/KNOWN_ISSUES.md` - Fixed in k0005 (auto-reconnect)

---

## Emergency Recovery Checklist

If project is corrupted, follow this checklist:

- [ ] Extract backup to clean directory
- [ ] Install Python 3.11+ (required)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Verify directory structure matches above
- [ ] Check `app/main.py` exists and is readable
- [ ] Run self-test: Click "TEST" button or run selftest.py
- [ ] Check logs in `all_logs/` for errors
- [ ] Restore user config from `%APPDATA%\Radar Games ML\config.json`
- [ ] Rebuild EXE: Run `RUN_BUILD_Win.cmd`

---

## Additional Resources

- **Architecture:** `docs/ARCHITECTURE.md`
- **API Reference:** `docs/API.md`
- **Module Reference:** `docs/MODULES.md`
- **User Guide:** `docs/USAGE.md`
- **Build Instructions:** `docs/BUILD.md`
- **Known Issues:** `docs/KNOWN_ISSUES.md`
- **Changelog:** `docs/CHANGELOG.md`

---

**Radar Games ML v4.3.1-k0006** - Complete recovery and backup documentation.
