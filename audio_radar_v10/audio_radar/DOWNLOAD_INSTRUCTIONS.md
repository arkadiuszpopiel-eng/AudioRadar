# AudioRadar v10.2 - Download and Installation Instructions

## 📦 ZIP Package Download

### Main Package - AudioRadar v10.2 FULL

**File:** `AudioRadar_v10.2_FULL.zip`

**Contents:**
- Complete AudioRadar v10.2 source code
- All Python modules (gui.py, main.py, audio_capture.py, etc.)
- Full documentation (README.md, CHANGELOG.md, GUI_FEATURES.md)
- Installation script (RUN_BUILD_ALL.cmd)
- Release notes (RELEASE_NOTES_v10.2.md)
- Before/After guide (BEFORE_AFTER.md)

**Size:** ~34 KB (compressed)

---

## 🔗 Download Links

### Option 1: GitHub Releases (Recommended)

```
https://github.com/arkadiuszpopiel-eng/AudioRadar/releases/tag/v10.2
```

Download the `AudioRadar_v10.2_FULL.zip` file from the Assets section.

### Option 2: GitHub Repository (Source Code)

```
https://github.com/arkadiuszpopiel-eng/AudioRadar
```

**Clone entire repository:**
```bash
git clone https://github.com/arkadiuszpopiel-eng/AudioRadar.git
cd AudioRadar/audio_radar_v10/audio_radar
```

**Or download as ZIP:**
- Click the green "Code" button
- Select "Download ZIP"
- Extract and navigate to `audio_radar_v10/audio_radar/`

### Option 3: Direct Branch Link

```
https://github.com/arkadiuszpopiel-eng/AudioRadar/archive/refs/heads/copilot/add-gain-threshold-controls.zip
```

This downloads the latest version from the branch with v10.2 features.

---

## 📋 System Requirements

### Minimum:
- **OS:** Windows 10/11 (64-bit)
- **Python:** 3.8 or newer
- **RAM:** 2 GB
- **Disk Space:** 100 MB

### Recommended:
- **OS:** Windows 11 (64-bit)
- **Python:** 3.10 or newer
- **RAM:** 4 GB
- **Sound Card:** With loopback capability (e.g., Sound Blaster Z SE, Stereo Mix)

---

## 🚀 Step-by-Step Installation

### Step 1: Download Package

Choose one of the options above and download the ZIP file.

### Step 2: Extract

```
Right-click → Extract All → Choose location
```

Recommended location: `C:\AudioRadar\`

### Step 3: Install Python (if not installed)

Download from: https://www.python.org/downloads/

**Important:** Check "Add Python to PATH" during installation!

### Step 4: Open Terminal

```
Windows + R → type "cmd" → Enter
```

Navigate to folder:
```bash
cd C:\AudioRadar\audio_radar_v10\audio_radar
```

### Step 5: Install Dependencies

**Automatic (Windows):**
```bash
RUN_BUILD_ALL.cmd
```

**Manual:**
```bash
pip install PyQt5 sounddevice numpy pygame
```

### Step 6: Run Program

**With GUI (Recommended - v10.2):**
```bash
python run_gui.py
```

**Classic mode (Pygame only):**
```bash
python main.py
```

---

## 📚 Full Documentation

After extracting the package, you'll find:

### README.md
Main documentation with feature descriptions and troubleshooting.

### CHANGELOG.md
Version history and new features in each release.

### GUI_FEATURES.md
Detailed guide to all GUI features (8,700+ lines).

### BEFORE_AFTER.md
Visual before/after comparison with usage examples.

### RELEASE_NOTES_v10.2.md
Complete v10.2 release notes.

---

## 🎯 Quick Start - First Launch

### 1. After Installation

```bash
cd C:\AudioRadar\audio_radar_v10\audio_radar
python run_gui.py
```

### 2. You'll See the GUI Window

```
┌─────────────────────────────────────┐
│ Audio Radar v10.2 - Control Panel   │
├─────────────────────────────────────┤
│  [Controls] [Info]                  │
│                                     │
│  Input Gain:     [──●──]  1.0x     │
│  Threshold:      [──●──]  0.050    │
│  Signal Strength: [     ]  0%      │
│                                     │
│  [🎯 Auto-Calibrate Threshold]     │
│  [▶ START Detection]               │
└─────────────────────────────────────┘
```

### 3. Audio Setup

1. Select input device (e.g., "Stereo Mix")
2. Click "🔄 Refresh" if you don't see devices

### 4. Calibration (Recommended)

1. Turn off all games/music
2. Click "🎯 Auto-Calibrate Threshold"
3. Wait 10 seconds
4. Program will set optimal threshold

### 5. Testing

1. Start audio (game, music)
2. Watch "Signal Strength"
3. If red/orange → increase "Input Gain"
4. Click "▶ START Detection"

---

## 🔧 Troubleshooting

### Problem: "PyQt5 not found"

**Solution:**
```bash
pip install PyQt5
```

### Problem: "sounddevice library not found"

**Solution:**
```bash
pip install sounddevice
```

If still not working:
```bash
# Install PortAudio
pip install --upgrade sounddevice
```

### Problem: No audio devices

**Solution:**
1. Enable "Stereo Mix" in Windows settings:
   - Right-click speaker icon → Sounds
   - Recording tab
   - Right-click → Show Disabled Devices
   - Enable "Stereo Mix"

### Problem: Signal too weak (red bar)

**Solution:**
1. Increase "Input Gain" to 5.0x - 10.0x
2. Or use "Enable Pre-Amplifier"
3. Or lower "Detection Threshold" to 0.010-0.025

---

## 📞 Help and Support

### GitHub Issues
```
https://github.com/arkadiuszpopiel-eng/AudioRadar/issues
```

Report problems or ask for help.

### Online Documentation
```
https://github.com/arkadiuszpopiel-eng/AudioRadar/tree/copilot/add-gain-threshold-controls/audio_radar_v10/audio_radar
```

Read README.md and other documentation files online.

---

## 🆕 What's New in v10.2?

### Major Features

1. **Input Gain Control**
   - Range: 0.1x - 10.0x
   - Amplifies weak audio signals

2. **Adjustable Threshold**
   - Range: 0.001 - 0.200
   - Customize detection sensitivity

3. **Signal Strength Indicator**
   - Real-time progress bar
   - Color coding: 🔴 Red / 🟡 Orange / 🟢 Green

4. **Auto-Calibration**
   - 10s background noise analysis
   - Automatic optimal threshold setting

5. **Pre-Amplifier**
   - Quick x5 boost
   - For very weak signals

6. **PyQt5 GUI Interface**
   - Modern control panel
   - Polish tooltips
   - Two tabs: Controls + Info

### Problem Solved

**Before v10.2:**
- Signal peak: 0.005 (0.5%)
- Default threshold: 0.050 (5%)
- Result: NOT DETECTED ❌

**After v10.2:**
- Peak × 10 gain = 0.050 (5%)
- Or threshold lowered to 0.003
- Result: DETECTED ✓

---

## 📦 Package Structure

```
AudioRadar_v10.2_FULL.zip
└── audio_radar_v10/
    └── audio_radar/
        ├── gui.py                    # PyQt5 GUI (660 lines)
        ├── run_gui.py                # GUI launcher
        ├── main.py                   # Classic mode
        ├── audio_capture.py          # Audio capture
        ├── sound_analysis.py         # Sound analysis
        ├── visualization.py          # Pygame visualization
        ├── config.json               # Configuration
        ├── RUN_BUILD_ALL.cmd         # Windows installer
        │
        ├── README.md                 # Main documentation
        ├── CHANGELOG.md              # Change history
        ├── VERSION.txt               # Version (v10.2)
        ├── RELEASE_NOTES_v10.2.md    # Release notes
        ├── GUI_FEATURES.md           # GUI guide
        ├── BEFORE_AFTER.md           # Comparison
        ├── DOWNLOAD_INSTRUCTIONS.md  # This file (English)
        └── DOWNLOAD_INSTRUCTIONS_PL.md  # Polish version
```

---

## ✅ Post-Installation Checklist

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (PyQt5, sounddevice, numpy, pygame)
- [ ] "Stereo Mix" or other loopback device enabled
- [ ] GUI launches without errors
- [ ] Audio device visible in dropdown
- [ ] Signal Strength bar responds to audio
- [ ] Auto-calibration works
- [ ] Detection picks up footsteps/gunshots

---

## 🎊 Ready!

You can now use AudioRadar v10.2 with full gain control and detection threshold adjustment!

**Weak signal problem? SOLVED!** ✓

Enjoy better audio detection without needing to buy new hardware!

---

**Version:** v10.2  
**Date:** 2025-11-09  
**Repository:** https://github.com/arkadiuszpopiel-eng/AudioRadar  
**Branch:** copilot/add-gain-threshold-controls
