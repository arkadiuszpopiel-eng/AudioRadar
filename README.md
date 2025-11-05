# Audio Radar

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🎯 Cel projektu / Project Goal

Audio Radar to aplikacja na Windows 11, która w czasie rzeczywistym przechwytuje dźwięk z gry (loopback z karty dźwiękowej), wykrywa w nim kroki oraz strzały przeciwników i wizualizuje kierunek, z którego dochodzą. Projekt ma wspierać graczy, w tym osoby niedosłyszące, w lepszej orientacji przestrzennej.

**English:** Audio Radar is a Windows 11 application that captures game audio in real-time (via sound card loopback), detects footsteps and gunshots, and visualizes the direction they're coming from. The project aims to support gamers, including those with hearing impairments, in improving spatial awareness.

## ✨ Features / Funkcje

- 🎧 **Real-time audio capture** using WASAPI loopback
- 🎯 **Sound event detection** - footsteps and gunshots
- 🧭 **Directional visualization** with 8-way radar display
- 🔊 **Multi-channel support** - Stereo, 5.1, and 7.1 surround sound
- ⚙️ **Configurable thresholds** via JSON configuration
- 🎨 **Customizable visualization** - adjustable colors, sizes, and transparency
- 🔍 **Distance estimation** based on audio amplitude
- 🎛️ **Bandpass filtering** for improved detection accuracy
- 📊 **Background noise adaptation** for better detection in various environments

## 📋 Requirements / Wymagania

- **Operating System**: Windows 11 (or Windows 10)
- **Python**: 3.8 or newer
- **Sound Card**: With loopback support (e.g., Sound Blaster Z SE, or Stereo Mix enabled)
- **Audio Setup**: Headphones or speakers (5.1/7.1 configuration recommended for best directional accuracy)

## 🚀 Quick Start / Szybki start

### Installation / Instalacja

1. **Clone the repository**:
```bash
git clone https://github.com/arkadiuszpopiel-eng/AudioRadar.git
cd AudioRadar
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

Or using the provided batch script on Windows:
```bash
cd audio_radar_v10\audio_radar
RUN_BUILD_ALL.cmd
```

### Usage / Użycie

1. **Enable audio loopback** on your system:
   - **For Sound Blaster cards**: Enable "What U Hear" or "Stereo Mix" in the Sound Blaster Control Panel
   - **For Windows built-in**: 
     - Right-click the speaker icon in system tray
     - Select "Sounds" → "Recording" tab
     - Right-click in empty area → "Show Disabled Devices"
     - Enable "Stereo Mix" and set as default recording device

2. **List available audio devices** (to find your loopback device):
```bash
cd audio_radar_v10/audio_radar
python main.py --list-devices
```

3. **Configure the input device** (optional):
   - Open `config.json`
   - Set `"input_device"` to the index of your loopback device from step 2

4. **Run Audio Radar**:
```bash
python main.py
```

5. **Adjust settings in real-time** using keyboard controls:
   - `Z`/`X` - Decrease/increase bar width
   - `C`/`V` - Decrease/increase bar height  
   - `B`/`N` - Decrease/increase transparency

## ⚙️ Configuration / Konfiguracja

Edit `audio_radar_v10/audio_radar/config.json` to customize settings:

```json
{
  "input_device": null,
  "audio": {
    "samplerate": 48000,
    "blocksize": 1024,
    "channels": 2
  },
  "detection": {
    "shot_peak_threshold": 0.6,
    "footstep_std_threshold": 0.05,
    "enable_bandpass_filter": true,
    "footstep_freq_range": [2000, 8000],
    "shot_freq_range": [200, 12000]
  },
  "visualization": {
    "fade_duration": 0.5,
    "show_distance_indicator": true,
    "footstep_color": [0, 255, 0],
    "shot_color": [255, 0, 0]
  },
  "bar_width": 40,
  "bar_height": 200,
  "transparency": 180
}
```

### Key Configuration Parameters:

#### Audio Settings
- **samplerate**: Audio sampling rate (44100 or 48000 Hz recommended)
- **blocksize**: Audio buffer size (1024 = ~21ms latency at 48kHz)
- **channels**: Number of audio channels (auto-detected if not specified)

#### Detection Settings
- **shot_peak_threshold**: Amplitude threshold for gunshot detection (0.0-1.0, default: 0.6)
- **footstep_std_threshold**: Standard deviation threshold for footstep detection (default: 0.05)
- **enable_bandpass_filter**: Enable frequency filtering for better detection (default: true)
- **footstep_freq_range**: Frequency range for footstep detection in Hz (default: [2000, 8000])
- **shot_freq_range**: Frequency range for gunshot detection in Hz (default: [200, 12000])

#### Visualization Settings
- **fade_duration**: How long bars stay lit after detection in seconds (default: 0.5)
- **footstep_color**: RGB color for footstep indicators (default: green [0, 255, 0])
- **shot_color**: RGB color for gunshot indicators (default: red [255, 0, 0])
- **bar_width**: Width of directional bars in pixels (default: 40)
- **bar_height**: Height of directional bars in pixels (default: 200)
- **transparency**: Opacity of bars when active (0-255, default: 180)

## 🎮 How It Works / Jak to działa

### Architecture Overview

```
┌─────────────────┐
│   Game Audio    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Audio Capture  │  WASAPI Loopback
│  (sounddevice)  │  48kHz, 16-bit
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Signal Process  │  Bandpass filtering
│                 │  Noise reduction
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│Event Detection  │  Footstep/Shot
│  (Heuristics)   │  classification
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   Direction     │  Multi-channel
│   Analysis      │  energy analysis
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Visualization  │  8-way radar
│    (Pygame)     │  Real-time overlay
└─────────────────┘
```

### Detection Algorithm

1. **Audio Capture**: Captures audio via WASAPI loopback at 48kHz
2. **Preprocessing**: Applies bandpass filters:
   - Footsteps: 2-8 kHz (crisp footstep sounds)
   - Gunshots: 0.2-12 kHz (wide spectrum impacts)
3. **Event Detection**:
   - **Gunshots**: Detected by sharp amplitude peaks (>60% of max)
   - **Footsteps**: Detected by moderate variation in mid-frequencies
4. **Direction Calculation**:
   - **Stereo**: Left/right channel comparison
   - **5.1/7.1**: Energy distribution across all channels with vector averaging
5. **Distance Estimation**: Based on amplitude relative to background noise

## 🔧 Troubleshooting / Rozwiązywanie problemów

### No audio detected
- Ensure loopback device is enabled and set as default recording device
- Check that game audio is playing through the same device
- Try listing devices with `--list-devices` and setting the correct `input_device` in config

### False positives
- Increase `shot_peak_threshold` or `footstep_std_threshold` in config.json
- Enable bandpass filtering: `"enable_bandpass_filter": true`
- Adjust frequency ranges to match your game's audio profile

### Missing events
- Decrease detection thresholds
- Check that audio is reaching the program (monitor log file)
- Ensure game volume is not too low

### High CPU usage
- Increase `blocksize` in config (e.g., 2048 or 4096)
- Disable bandpass filtering if not needed
- Close other applications using audio

## 📚 Documentation / Dokumentacja

- [Koncepcja projektu](README_KONCEPCJA.md) - Original project concept (Polish)
- [Installation Guide](audio_radar_v10/audio_radar/README.md) - Detailed installation instructions
- [Keyboard Controls](audio_radar_v10/audio_radar/README.md#features) - Real-time adjustment controls

## 🛠️ Development / Rozwój

### Project Structure
```
AudioRadar/
├── audio_radar_v10/           # Latest stable version
│   └── audio_radar/
│       ├── main.py           # Entry point
│       ├── audio_capture.py  # WASAPI loopback handling
│       ├── sound_analysis.py # Event detection algorithms
│       ├── visualization.py  # Pygame radar display
│       └── config.json       # Configuration file
├── requirements.txt          # Python dependencies
├── setup.py                  # Package installation
└── README.md                 # This file
```

### Contributing
Contributions are welcome! Please feel free to submit pull requests or open issues for:
- New detection algorithms
- Machine learning models for event classification
- Support for additional audio devices
- Improved visualization options
- Bug fixes and performance improvements

## 📝 License / Licencja

This project is open source and available under the MIT License.

## 🙏 Acknowledgments / Podziękowania

- Concept inspired by hardware Audio Radar devices for gaming
- Built with Python, sounddevice, pygame, numpy, and scipy
- Created to improve gaming accessibility for players with hearing impairments

## 📧 Contact / Kontakt

For questions, suggestions, or issues, please:
- Open an issue on GitHub
- Check existing documentation in the repository
- Review the concept document for technical details

---

**Note**: This is an assistive tool designed to enhance gaming experience. It should not be considered a replacement for in-game audio cues, and users should check game-specific terms of service regarding third-party tools.
