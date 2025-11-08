# AudioRadar v11 - Modern GUI Edition

![Version](https://img.shields.io/badge/version-11.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## 🎯 What's New in v11

AudioRadar v11 is a complete rewrite featuring a **modern GUI interface** with:

- **✨ Modern GUI** - tkinter-based interface with professional controls
- **🎛️ Full Control Panel** - Sliders, buttons, and real-time adjustments
- **📊 Live Stats Dashboard** - Peak/RMS/Direction/Distance display
- **🔧 Advanced Configuration** - Save/load settings with JSON config
- **🪟 Window Controls** - Borderless mode, always-on-top, opacity control
- **🎵 Auto-Detection** - Automatic Stereo Mix discovery
- **📝 Comprehensive Logging** - Detailed logs with timestamps
- **🎮 Keyboard Shortcuts** - Quick access to all features

## 🚀 Quick Start

### Windows Quick Installation
```cmd
1. Download AudioRadar_v11_FULL.zip
2. Extract to your desired location
3. Run QUICKSTART_v11.cmd
```

### Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run AudioRadar v11
python -m audio_radar
# Or
python audio_radar_v11/audio_radar/__main__.py
```

## 🎛️ GUI Features

### Main Window
- **Borderless Mode**: Toggle for clean overlay appearance
- **Always-on-Top**: Keep radar visible over games
- **Opacity Control**: Slider from 0% to 100%
- **Draggable**: Click and drag anywhere to reposition

### Control Panel

**Detection Controls:**
- Volume Threshold slider (0.0 - 1.0)
- Sensitivity slider (0.0 - 1.0)
- Enable/Disable bandpass filter
- Auto-calibration toggle

**Action Buttons:**
- **Start/Stop Detection** - Begin/end audio monitoring
- **Calibrate** - Run calibration routine
- **Reset** - Reset to default settings
- **Save Config** - Save current configuration

### Stats Display
Real-time audio statistics overlay:
- Peak Amplitude (0.0 - 1.0)
- RMS (Root Mean Square) value
- Direction (0° - 360°)
- Distance estimation
- Last detected event type

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Start/Stop Detection |
| `C` | Run Calibration |
| `R` | Reset Settings |
| `S` | Save Configuration |
| `B` | Toggle Borderless Mode |
| `T` | Toggle Always-on-Top |
| `+/-` | Increase/Decrease Opacity |
| `F1` | Show Help |
| `Esc` | Exit Application |

## 🔧 Configuration

Settings are saved to `config_v11.json`:

```json
{
  "window": {
    "width": 800,
    "height": 600,
    "always_on_top": true,
    "borderless": false,
    "opacity": 0.95
  },
  "detection": {
    "volume_threshold": 0.3,
    "sensitivity": 0.5,
    "enable_filter": true,
    "auto_calibrate": false
  }
}
```

## 📊 Detection Features

**Audio Processing:**
- Multi-channel support (stereo, 5.1, 7.1)
- Bandpass filtering for accuracy
- Background noise adaptation
- Real-time frequency analysis

**Event Detection:**
- **Footsteps**: Green indicators, 2-8kHz range
- **Gunshots**: Red indicators, 200Hz-12kHz range
- Direction tracking (0-360°)
- Distance estimation

## 🔍 Troubleshooting

### No Audio Detection
1. Enable "Stereo Mix" in Windows Sound settings
2. Set Stereo Mix as default recording device
3. Check volume levels in calibration mode

### GUI Not Responding
- Check `audioradar_v11.log` for errors
- Ensure Python 3.11+ is installed
- Verify all dependencies are installed

### Performance Issues
- Reduce window opacity for better performance
- Lower sample rate in config (48000 → 44100)
- Disable bandpass filter if CPU limited

## 📝 Logging

Detailed logs are written to `audioradar_v11.log`:
- Application startup/shutdown
- Audio device detection
- Configuration changes
- Detection events with timestamps
- Error messages and warnings

## 🔄 Upgrading from v10.x

v11 is a complete rewrite and cannot directly import v10 settings. However:
- v10 and v11 can coexist
- v11 uses separate config file (`config_v11.json`)
- Detection algorithms are improved in v11

## 📦 What's Included

```
audio_radar_v11/
├── audio_radar/
│   ├── __init__.py
│   ├── __main__.py           # Entry point
│   ├── gui_main.py            # Main GUI application (553 lines)
│   ├── audio_capture.py       # Audio device management
│   ├── sound_analysis.py      # Detection algorithms
│   ├── config_v11.json        # Configuration file
│   └── audioradar_v11.log     # Log file (created at runtime)
├── README_v11.md              # This file
├── INSTALL_v11.md             # Installation guide
└── USER_GUIDE_v11.md          # Complete user manual
```

## 🎯 System Requirements

- **OS**: Windows 10/11, Linux, macOS
- **Python**: 3.11 or higher
- **RAM**: 2GB minimum
- **CPU**: Dual-core 2GHz+

**Required Packages:**
- tkinter (usually included with Python)
- pygame >= 2.5.0
- sounddevice >= 0.4.6
- numpy >= 1.24.0

## 🤝 Contributing

AudioRadar is open for contributions! See `CONTRIBUTING.md` for guidelines.

## 📄 License

MIT License - see `LICENSE` file for details.

## 🎮 Game Support

Tested and working with:
- CS:GO / CS2
- Valorant
- Call of Duty series
- Apex Legends
- PUBG
- Fortnite
- And many more!

## 🔗 Links

- [GitHub Repository](https://github.com/arkadiuszpopiel-eng/AudioRadar)
- [Issue Tracker](https://github.com/arkadiuszpopiel-eng/AudioRadar/issues)
- [Documentation](https://github.com/arkadiuszpopiel-eng/AudioRadar/wiki)

---

**AudioRadar v11** - Professional Audio Direction Detection
Made with ❤️ for gamers
