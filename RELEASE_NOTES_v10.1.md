# AudioRadar v10.1 - Release Notes

## 📦 Release Package: AudioRadar_v10.1_CLEAN.zip

This is the official release package for AudioRadar v10.1 with audio testing tools and diagnostics.

### Package Contents

```
AudioRadar_v10.1_CLEAN/
├── START_HERE.bat           # Windows launcher (auto-installs dependencies)
├── README_PL.txt            # Complete Polish documentation (7.6 KB)
├── README.md                # English documentation
├── CHANGELOG.txt            # Version history
├── LICENSE.txt              # MIT License
├── requirements.txt         # Python dependencies
│
├── audio_radar/             # Main application
│   ├── __init__.py
│   ├── __main__.py          # Entry point
│   ├── main.py              # Main application logic
│   ├── visualization.py     # Pygame radar visualization
│   ├── audio_capture.py     # Audio input handling
│   ├── audio_test_window.py # NEW: Audio testing tool
│   ├── sound_analysis.py    # Event detection algorithms
│   ├── config.json          # Configuration file
│   └── VERSION.txt          # Version identifier
│
└── docs/
    ├── QUICK_START.txt      # Quick start guide (PL/EN)
    └── TROUBLESHOOTING.txt  # Problem-solving guide (9.1 KB)
```

### Installation

#### Option 1: Using START_HERE.bat (Recommended for Windows)

1. Extract the ZIP file
2. Double-click `START_HERE.bat`
3. The script will:
   - Check Python installation
   - Install dependencies automatically
   - Launch the application

#### Option 2: Manual Installation

```bash
# Extract ZIP
unzip AudioRadar_v10.1_CLEAN.zip
cd AudioRadar_v10.1_CLEAN

# Install dependencies
pip install -r requirements.txt

# Run application
cd audio_radar
python -m audio_radar
```

### Requirements

- **Python**: 3.8 or newer
- **OS**: Windows 11 (or Windows 10)
- **Audio Hardware**: Sound card with loopback capability (e.g., Sound Blaster Z SE)
- **Dependencies**: sounddevice, pygame, numpy (auto-installed)

### Quick Start

1. **Configure Audio Loopback**:
   - Open Windows Sound Settings
   - Enable "Stereo Mix" or "What U Hear"
   - Set as default recording device

2. **Test Audio** (Press `T`):
   - Launch application
   - Press `T` key
   - Play music/game LOUDLY
   - Check RMS/Peak levels

3. **Play**:
   - Close test window (ESC)
   - Start game
   - Green bars = Footsteps
   - Red bars = Gunshots

### Keyboard Controls

| Key | Action |
|-----|--------|
| `T` | Open audio test window |
| `D` | Toggle debug mode |
| `ESC` | Close program |
| `Z`/`X` | Adjust bar width |
| `C`/`V` | Adjust bar height |
| `B`/`N` | Adjust transparency |

### What's New in v10.1

#### Added Features
- ✅ **Audio Test Window** - Real-time RMS/Peak meters with diagnostics
- ✅ **VU Meter** - Live audio level display in main window
- ✅ **Latency Display** - Shows actual buffer latency (was 0.0 ms)
- ✅ **Debug Mode** - Live detection statistics

#### Fixed Issues
- ✅ Latency calculation now shows real values
- ✅ Better audio diagnostics
- ✅ Detection feedback improved

#### Documentation
- ✅ Complete Polish guide (README_PL.txt)
- ✅ Troubleshooting guide (12 scenarios)
- ✅ Quick start guide
- ✅ Change log

### Troubleshooting

**No audio detection?**
1. Press `T` to open test window
2. Play something LOUD
3. Check levels:
   - ✓ Peak > 0.1 = OK
   - ⚠ Peak 0.01-0.1 = Weak signal
   - ✗ Peak < 0.01 = No signal

See `docs/TROUBLESHOOTING.txt` for complete problem-solving guide.

### Support

- **GitHub**: https://github.com/arkadiuszpopiel-eng/AudioRadar
- **Issues**: Report bugs on GitHub Issues
- **Documentation**: See README_PL.txt for complete guide

### License

MIT License - See LICENSE.txt

### Credits

Created with assistance from OpenAI GPT based on user requirements.
Uses: sounddevice, pygame, numpy

---

**Version**: v10.1  
**Release Date**: 2025-11-09  
**Package Size**: ~34 KB (compressed)  
**Language**: Polish/English  
