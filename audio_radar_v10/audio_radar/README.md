# Audio Radar

Audio Radar is a proof‑of‑concept Python application that monitors audio
from your PC in real time, detects specific sound events (footsteps and
gunshots) and displays a directional overlay to help you locate the
source of these sounds. It is primarily designed for players with
hearing impairments or anyone who wants an additional visual cue while
gaming.

## Features

* **Real‑time audio capture** using the `sounddevice` library and your
  sound card’s loopback interface (e.g. “Stereo Mix” on Sound Blaster
  cards).
* **Sound event detection** via simple amplitude heuristics – you can
  customise thresholds in `sound_analysis.py` to suit your game.
* **Visual overlay** with eight radial bars drawn using `pygame` that
  light up when a footstep or shot is detected. Bars fade after half a
  second and are colour‑coded (green for steps, red for shots).
* **Configurable bar sizes and transparency** via keyboard controls
  (Z/X to change width, C/V to change height, B/N to change opacity).
* **Custom audio device selection** through `config.json`; run
  `python main.py --list-devices` to discover available devices.
* **Logging** to a versioned `log_<version>.txt` file (e.g. `log_v10.txt`) so you can troubleshoot audio problems or
  unexpected behaviour.

### v10.2 New Features

* **PyQt5 Control Panel GUI** with intuitive controls for all settings
* **Input Gain Control** (0.1x - 10.0x amplification) for weak audio signals
* **Adjustable Detection Threshold** (0.001 - 0.200) for fine-tuning sensitivity
* **Signal Strength Indicator** with color-coded feedback (red/orange/green)
* **Auto-Calibration** feature that analyzes background noise and sets optimal threshold
* **Pre-Amplifier** checkbox for quick x5 boost when signals are very weak
* **Real-time Visual Feedback** showing signal strength during operation

## Prerequisites

This project targets Windows 11 but should work on other platforms with
minor adjustments. You will need:

* Python 3.8 or newer
* `sounddevice` for audio capture
* `pygame` for the graphical interface
* `numpy` for basic signal processing
* `PyQt5` for the control panel GUI (v10.2+)

Because the container environment used to generate this archive cannot
install packages, please install the required libraries yourself. You
can use the included batch script `RUN_BUILD_ALL.cmd` to install
dependencies on Windows using `pip`.

## Installation and Usage

1. **Extract** the archive to a convenient folder.
2. Open a **PowerShell or Command Prompt** in that folder.
3. Uruchom `RUN_BUILD_ALL.cmd`. Skrypt ten zainstaluje brakujące
   biblioteki i uruchomi aplikację. Zainstalowane pakiety wypisuje
   na konsolę (nie przekierowuje ich do pliku), a sama aplikacja
   tworzy plik logu w folderze `audio_radar`. Nazwa pliku logu zawiera
   numer wersji, np. `log_v10.txt`. W pliku tym zapisana jest
   informacja o wersji programu i użytej konfiguracji.
4. Możesz uruchomić program również ręcznie: wejdź do folderu
   `audio_radar` i wywołaj:

   **With GUI (v10.2+, recommended):**
   ```
   python run_gui.py
   ```

   **Classic mode (Pygame only):**
   ```
   python main.py
   ```

5. Gdy pojawi się okno programu, zobaczysz pusty radar. Włącz
   your favourite game and ensure its audio is routed to a loopback
   device (e.g. enable “Stereo Mix” on your Sound Blaster Z SE and set
   it as the default recording device in Windows). Footsteps should
   trigger a green bar at the top of the radar and gunshots should
   trigger a red bar at the bottom.
6. Adjust the bar sizes and transparency with the keyboard controls:
   * Z/X – decrease/increase bar width
   * C/V – decrease/increase bar height
   * N/B – decrease/increase transparency
7. To select a specific audio device open `config.json` in a text
   editor and set `input_device` to the index of your loopback device.
   You can obtain the index by running `python main.py --list-devices`.

## Limitations

* The detection algorithms are simple heuristics and may produce
  false positives or miss events in noisy games. Feel free to
  experiment with the thresholds defined in `sound_analysis.py`.
* Bars are mapped to two directions only (front for footsteps,
  back for shots). You can map different events to different
  directions by editing `Visualizer.trigger_event`.
* The program currently does not support audio output; it
  consumes input only. The `output_device` field in the configuration
  file is reserved for future use.

## Troubleshooting

If you encounter issues:

* Ensure that `sounddevice`, `pygame`, `numpy` and `PyQt5` are installed and that
  your audio loopback device is enabled. You can verify installation
  by running `python -c "import sounddevice, pygame, numpy, PyQt5"`.
* Po uruchomieniu program wypisuje w konsoli ścieżkę, do której zapisywany jest plik logu (np. `log_v10.txt` w folderze `audio_radar`). Jeśli szukasz logu w niewłaściwym miejscu, może wydawać się, że się nie tworzy. Sprawdź lokalizację podaną w komunikacie `[AudioRadar v10] Logging to …`.
* Use `--list-devices` to confirm that your loopback device is
  recognised by the program.

### Weak Audio Signal (v10.2)

**Problem:** Radar does not detect footsteps/gunshots even though audio is playing.

**Symptom:** Signal Strength indicator shows red (< 1%) or orange (1-5%).

**Solution:**

1. **Increase Input Gain:**
   - Open the GUI with `python run_gui.py`
   - Move the "Input Gain" slider to the right
   - Start with 2.0x and increase until Signal Strength shows green (> 5%)
   - Watch the Signal Strength bar for real-time feedback

2. **Lower Detection Threshold:**
   - Move the "Detection Threshold" slider to the left
   - Start at 0.025 and decrease until detection works
   - Warning: Too low = many false positives

3. **Use Auto-Calibration (RECOMMENDED):**
   - Click "🎯 Auto-Calibrate Threshold"
   - Turn off all game audio and music
   - Wait 10 seconds while program analyzes background noise
   - Program will automatically set optimal threshold

4. **Enable Pre-Amplifier:**
   - Check "Enable Pre-Amplifier" for quick x5 boost
   - Use for very weak signals

**Signal Strength Indicator:**
- 🔴 Red (< 1%): Signal too weak - increase gain
- 🟡 Orange (1-5%): Weak signal - may need adjustment  
- 🟢 Green (> 5%): Good signal strength

## Credits

This project was generated by OpenAI’s ChatGPT based on user
requirements for a simple yet extensible audio radar. Feel free to
modify and expand it to suit your needs.