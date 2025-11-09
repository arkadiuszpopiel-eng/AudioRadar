# AudioRadar v10.1 - PyQt5 GUI Edition

AudioRadar is a modern Python application with a **PyQt5 graphical interface** that monitors audio from your PC in real time. It provides audio level testing, device management, and performance monitoring. This version is designed for easy testing and configuration of audio input devices.

## 🎯 What's New in v10.1

* **Complete PyQt5 GUI** - Modern dark-themed interface (NO pygame!)
* **Audio Test Dialog** - Real-time audio level testing with visual feedback
* **Device Management** - Easy selection and configuration of audio devices
* **Performance Monitor** - Live CPU, latency, and memory statistics
* **Keyboard Shortcuts** - SPACE to start/stop, F5 to refresh devices
* **Status Bar** - Connection status, latency, and CPU usage at a glance

## ✨ Features

* **Modern PyQt5 Interface** with dark theme and cyan accents
* **Real-time audio capture** using `sounddevice` library
* **Audio Level Testing** - Test dialog shows RMS and Peak levels
* **Device Selection** - Easy dropdown to choose input devices
* **Performance Monitoring** - Real-time CPU and latency tracking
* **Keyboard Shortcuts**:
  - `SPACE` - Start/Stop audio capture
  - `F5` - Refresh device list
* **Status Indicators** - Visual connection status, latency, and CPU usage

## 📋 Prerequisites

This project targets Windows 11 but works on other platforms with Python support. You will need:

* **Python 3.8 or newer**
* **PyQt5** - For the graphical interface
* **sounddevice** - For audio capture
* **numpy** - For signal processing
* **psutil** (optional) - For CPU/memory monitoring

## 🚀 Quick Start

### Method 1: Using START_HERE.bat (Windows - Recommended)

1. **Extract** the archive to a folder
2. **Double-click** `START_HERE.bat`
3. The script will:
   - Check for Python
   - Install all required dependencies
   - Launch the PyQt5 GUI

### Method 2: Using RUN_BUILD_ALL.cmd (Windows)

1. **Extract** the archive to a folder
2. **Open Command Prompt** in the audio_radar folder
3. **Run**: `RUN_BUILD_ALL.cmd`
4. The GUI will launch automatically

### Method 3: Manual Installation (All Platforms)

1. **Install dependencies**:
   ```bash
   pip install PyQt5 sounddevice numpy scipy psutil pyaudiowpatch
   ```

2. **Navigate to the audio_radar folder**:
   ```bash
   cd audio_radar
   ```

3. **Run the application**:
   ```bash
   python __main__.py
   ```

## 🎮 Using the Application

### Main Window

When you launch AudioRadar, you'll see:

```
┌─── AudioRadar v10.1 - Optimized Core ───┐
│ [Control] [Radar]                       │
├─────────────────────────────────────────┤
│ Urządzenia audio wejściowe:            │
│ [▼ Mikrofon (Realtek)               ]  │
│                                         │
│ [▶ START] [■ STOP] [🔊 TEST Audio]   │
│                                         │
│ Input Level: [▓▓▓░░░░░] 25%           │
├─────────────────────────────────────────┤
│ 🟢 Connected | Latency: 5.3ms | CPU: 8%│
└─────────────────────────────────────────┘
```

### Control Tab

* **Device Dropdown** - Select your audio input device
* **START Button** - Begin audio capture and monitoring
* **STOP Button** - Stop audio capture
* **TEST Audio Button** - Open audio test dialog
* **Input Level Bar** - Shows current audio input level

### Audio Test Dialog

Click the "🔊 TEST Audio" button to:

1. See real-time RMS and Peak audio levels
2. Verify your microphone is working
3. Check if audio signal is coming through
4. Test different input devices

### Status Bar

Shows three important indicators:

* **🟢/🔴 LED** - Connection status (green = connected, red = disconnected)
* **Latency** - Audio latency in milliseconds
* **CPU** - Current CPU usage percentage

### Keyboard Shortcuts

* **SPACE** - Toggle START/STOP
* **F5** - Refresh audio devices
* **ESC** - Close dialogs

## 🔧 Configuration

The application stores configuration in `config.json`. You can manually edit this file to set default values:

```json
{
  "input_device": null,
  "output_device": null,
  "bar_width": 40,
  "bar_height": 200,
  "transparency": 180
}
```

* `input_device` - Device index (null = default device)
* `output_device` - Reserved for future use
* Other settings - Reserved for future radar visualization

## ❓ Troubleshooting

### PyQt5 Not Found

If you see "PyQt5 not found!", install it:

```bash
pip install PyQt5
```

### No Audio Devices

If no audio devices appear:

1. Check that your microphone is connected
2. Verify audio drivers are installed
3. Try restarting the application
4. Press F5 to refresh the device list

### Audio Test Shows Zero Levels

If the audio test shows 0.000:

1. Make sure the correct device is selected
2. Check that your microphone isn't muted
3. Verify microphone permissions (Windows Privacy Settings)
4. Try speaking louder or making noise near the microphone

### Application Won't Start

1. Ensure Python 3.8+ is installed: `python --version`
2. Verify all dependencies are installed
3. Run from command line to see error messages:
   ```bash
   cd audio_radar
   python __main__.py
   ```

## 📁 File Structure

```
audio_radar/
├── __init__.py              - Package initialization
├── __main__.py              - Main entry point (PyQt5 launcher)
├── gui.py                   - Main PyQt5 window
├── audio_test_dialog.py     - Audio testing dialog
├── theme_manager.py         - Dark theme styling
├── audio_backends.py        - Audio device management
├── performance_monitor.py   - CPU/latency monitoring
├── audio_capture.py         - Audio stream handling
├── sound_analysis.py        - Audio analysis functions
├── config.json              - Configuration file
├── START_HERE.bat           - Quick launcher (Windows)
├── RUN_BUILD_ALL.cmd        - Installation script (Windows)
└── README.md                - This file
```

## 🎨 Theme

The application uses a dark theme with cyan accents:

* **Background**: Dark gray (#353535)
* **Text**: White
* **Accents**: Cyan (#00ffff)
* **Buttons**: Color-coded (green=start, red=stop, blue=test)

## 🔄 Version History

### v10.1 (Current)
* ✅ Complete migration to PyQt5 GUI
* ✅ Removed all Pygame dependencies
* ✅ Added Audio Test Dialog
* ✅ Added Performance Monitor
* ✅ Implemented dark theme
* ✅ Added keyboard shortcuts
* ✅ Improved error handling

### v10.0
* Legacy Pygame version (deprecated)

## 📝 License

This project was generated with assistance from AI. Feel free to modify and expand it to suit your needs.

## 🆘 Support

For issues or questions:

1. Check the Troubleshooting section above
2. Verify all dependencies are installed correctly
3. Run from command line to see detailed error messages
4. Check that you're using Python 3.8 or newer

## 🚀 Future Enhancements

Planned features for future versions:

* Real-time radar visualization (replacing the Radar tab placeholder)
* Audio event detection (footsteps, gunshots)
* Directional sound indicators
* Recording and playback capabilities
* Advanced audio filters and processing
* Custom keybindings
* Multi-language support

---

**AudioRadar v10.1** - Modern PyQt5 GUI Edition  
No Pygame. Pure PyQt5. Clean Interface. 🎯
