╔══════════════════════════════════════════════════════════════════════════════╗
║                      RadarSuite Final v2.3.1-Claude-001                        ║
║            Advanced Audio Radar and Detection System for Gaming                ║
╚══════════════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════════
  VERSION INFO
═══════════════════════════════════════════════════════════════════════════════

Version: v2.3.1-Claude-001
Release Date: 2024-11-16
Build: Production

NEW IN v2.3.1-Claude-001:
  ✓ Independent Radar window (works when main window minimized)
  ✓ Independent LED window (works when main window minimized)
  ✓ Independent opacity controls for Radar and LED
  ✓ Frameless window mode (for both Radar and LED)
  ✓ Language switcher: English / Polish (EN/PL button)
  ✓ Drag support for frameless windows
  ✓ Complete translation system
  ✓ Version naming with Claude designation

═══════════════════════════════════════════════════════════════════════════════
  DESCRIPTION
═══════════════════════════════════════════════════════════════════════════════

RadarSuite Final is a professional audio radar and detection system designed
for gaming. It captures audio from your sound card (loopback) or microphone,
analyzes it in real-time, and visualizes sound events on a radar display with
directional LED edge alerts.

Optimized for:
  - ARC Raiders (PC)
  - Sound Blaster Z SE
  - HyperX Cloud II

═══════════════════════════════════════════════════════════════════════════════
  KEY FEATURES
═══════════════════════════════════════════════════════════════════════════════

✓ AUDIO CAPTURE
  - sounddevice backend (microphone/line-in)
  - soundcard backend (loopback from speaker output)
  - Support for stereo, 5.1, 7.1 configurations
  - Sample rates: 44100, 48000, 96000 Hz
  - Adjustable block sizes: 512-4096 samples

✓ DETECTION MODES
  - WALK Detection (20-200 Hz, low frequency footsteps)
  - RUN Detection (200-1500 Hz, mid frequency, faster steps)
  - SHOT Detection (1500-6000 Hz, high frequency, sharp transients)
  - Individual sensitivity controls (1-100)
  - Enable/disable each detection type independently

✓ RADAR VISUALIZATION (pyqtgraph)
  - 360° sweep radar with distance rings (25m, 50m, 75m, 100m)
  - Radial lines every 45 degrees
  - Target echo with position and pseudo-distance
  - Real-time sweep animation
  - **DETACHABLE WINDOW** - works independently
  - **FRAMELESS MODE** - no window borders
  - **INDEPENDENT OPACITY** control (0-100%)
  - Drag support for repositioning

✓ SPECTRUM ANALYZER
  - Live FFT spectrum (20 Hz - 10 kHz)
  - Current spectrum (green) and averaged (yellow)
  - dB scale power display
  - 30-frame moving average

✓ WATERFALL DISPLAY
  - Spectrogram over time (scrolling)
  - Viridis colormap
  - Frequency on X-axis, time on Y-axis

✓ LED EDGE ALERT
  - Colored bars on screen edges
  - Direction-aware (left/right/center)
  - Walk/Run: green → yellow → red gradient
  - Shot: blue color
  - Smooth fade-out with intensity decay
  - **DETACHABLE WINDOW** - works independently
  - **FRAMELESS MODE** - no window borders
  - **INDEPENDENT OPACITY** control (0-100%)
  - Drag support for repositioning

✓ LANGUAGE SUPPORT
  - English (EN)
  - Polish (PL)
  - Toggle with EN/PL button in toolbar
  - All UI elements translated

✓ SYNTHETIC TEST MODE
  - Internal test signal generator
  - Simulates walk (80 Hz), run (420 Hz), shot (2200 Hz)
  - No audio device needed for testing

✓ PROFILES
  - Universal
  - ARC Raiders (PC)
  - ARC Raiders + SB Z SE + Cloud II
  - One-click preset application

═══════════════════════════════════════════════════════════════════════════════
  SYSTEM REQUIREMENTS
═══════════════════════════════════════════════════════════════════════════════

Minimum:
  - Windows 7/10/11 (64-bit)
  - Python 3.11 (for building)
  - 2 GB RAM
  - Sound card
  - Dual-core processor 2.0 GHz

Recommended:
  - Windows 10/11 (64-bit)
  - Python 3.11
  - 4 GB RAM
  - Sound Blaster Z SE or similar
  - Quad-core processor 3.0 GHz
  - HyperX Cloud II or gaming headset

═══════════════════════════════════════════════════════════════════════════════
  BUILDING THE EXE
═══════════════════════════════════════════════════════════════════════════════

Prerequisites:
  1. Install Python 3.11 from https://www.python.org/
  2. Make sure "Add Python to PATH" is checked during installation

Build Steps:
  1. Double-click: RUN_BUILD_ALL.cmd
  2. Wait for build to complete (~5-10 minutes)
  3. Find EXE in: dist\RadarSuite_Final\RadarSuite_Final.exe
  4. Optionally, extract the generated ZIP file

The build script will:
  - Create virtual environment (.venv)
  - Install all requirements
  - Build EXE with PyInstaller
  - Create ZIP archive with timestamp
  - Log everything to super_log.txt

═══════════════════════════════════════════════════════════════════════════════
  RUNNING THE APPLICATION
═══════════════════════════════════════════════════════════════════════════════

Option 1: Run Built EXE
  1. Navigate to: dist\RadarSuite_Final\
  2. Double-click: RadarSuite_Final.exe

Option 2: Run from Python (Development)
  1. Activate venv: .venv\Scripts\activate.bat
  2. Run: python app\main.py

═══════════════════════════════════════════════════════════════════════════════
  CONFIGURATION GUIDE
═══════════════════════════════════════════════════════════════════════════════

1. AUDIO DEVICE SETUP

   For Loopback (recommended for games):
   a) Open Windows Sound Settings
   b) Enable "Stereo Mix" or "What U Hear" for your sound card
   c) In RadarSuite:
      - Check "Loopback (soundcard)" checkbox
      - Select your sound card from device list
      - Click "Start"

   For Microphone:
   a) Select your microphone from device list
   b) Uncheck "Loopback (soundcard)"
   c) Click "Start"

2. SOUND BLASTER Z SE SETUP

   a) Click "SB Z SE + Cloud II" preset button
   b) This sets:
      - Sample Rate: 48000 Hz
      - Block Size: 2048 samples
      - Channels: 2 (Stereo)
   c) Make sure SB Z SE is selected in device list
   d) Enable "Loopback (soundcard)" for game audio

3. DETECTION TUNING

   - Sensitivity sliders (1-100):
     * Lower = more sensitive, more detections
     * Higher = less sensitive, fewer false positives

   - Recommended starting values:
     * Walk: 55
     * Run: 55
     * Shot: 65

   - Enable/disable detection types as needed

4. RADAR AND LED SETTINGS

   - Radar Alpha: Transparency of radar window (0-100%)
   - LED Alpha: Opacity of LED bars (0-100%)
   - Detach Radar: Creates independent radar window
   - Detach LED: Creates independent LED window
   - Frameless Mode: Removes window borders (drag with left mouse button)

═══════════════════════════════════════════════════════════════════════════════
  USAGE GUIDE
═══════════════════════════════════════════════════════════════════════════════

1. START DETECTION
   - Configure audio device (see Configuration Guide)
   - Click "Start" button in toolbar
   - Radar sweep should start rotating
   - Play game or make test sounds

2. LANGUAGE SWITCHING
   - Click "EN/PL" button in toolbar to toggle language
   - All UI elements will update immediately
   - Detached windows will also update

3. DETACH RADAR/LED
   - Click "Detach Radar" button to create independent radar window
   - Click "Detach LED" button to create independent LED window
   - These windows work even when main window is minimized
   - Each has independent opacity control
   - Each can be set to frameless mode

4. FRAMELESS MODE
   - Check "Frameless Mode" checkbox for Radar or LED
   - Window borders will be removed
   - Drag window with left mouse button to reposition
   - Useful for overlay on game screen

5. SYNTHETIC TEST MODE
   - Check "Synthetic Test Mode" in Device panel
   - Click "Start"
   - You should see:
     * Radar showing targets
     * Spectrum showing test frequencies
     * Detection labels lighting up
     * LED bars activating

6. INTERPRETING THE DISPLAY

   Radar:
   - Green rotating line = sweep
   - Red dot = detected target
   - Rings = distance (25m, 50m, 75m, 100m)
   - Position based on L/R balance and energy

   Spectrum Analyzer:
   - Green line = current spectrum
   - Yellow line = averaged spectrum
   - Shows frequency content of audio

   Waterfall:
   - Scrolling spectrogram
   - Bright colors = high energy
   - Dark colors = low energy

   Detection Panel:
   - "WALK: DETECTED" (green) = footsteps detected
   - "RUN: DETECTED" (orange) = running detected
   - "SHOT: DETECTED" (red) = gunshot detected
   - Polish: "CHÓD: WYKRYTO", "BIEG: WYKRYTO", "STRZAŁ: WYKRYTO"

   LED Edge Alert:
   - Top bars (G1, G2, G3) = general/front
   - Bottom bars (D1, D2, D3) = general/back
   - Left bars (L1, L2) = sound from left
   - Right bars (P1, P2) = sound from right
   - Colors:
     * Green → Yellow → Red = Walk/Run intensity
     * Blue = Shot

═══════════════════════════════════════════════════════════════════════════════
  FILE STRUCTURE
═══════════════════════════════════════════════════════════════════════════════

RadarSuite_Final/
├── app/
│   └── main.py              # Main application code (all-in-one, 1630 lines)
├── build_tools/
│   └── radarsuite.spec      # PyInstaller specification file
├── requirements.txt         # Python dependencies
├── RUN_BUILD_ALL.cmd        # Automated build script
├── super_log.txt            # Build and runtime log (created automatically)
├── README.txt               # This file
└── .venv/                   # Virtual environment (created by build script)

After building:
├── build/                   # PyInstaller build artifacts
├── dist/
│   ├── RadarSuite_Final/    # Standalone application folder
│   │   ├── RadarSuite_Final.exe
│   │   └── ... (dependencies)
│   └── RadarSuite_Final_v2.3.1-Claude-001_win64_*.zip  # Packaged archive

═══════════════════════════════════════════════════════════════════════════════
  TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════════

Problem: No audio devices shown
Solution:
  - Click "Refresh Devices" button
  - Check if sound card drivers are installed
  - Try running as Administrator

Problem: Loopback not working
Solution:
  - Enable "Stereo Mix" in Windows Sound Settings
  - For SB Z SE, use Creative software to enable recording mix
  - Try selecting different loopback device

Problem: No detections happening
Solution:
  - Lower sensitivity sliders (try 30-40)
  - Check audio level (RMS should show activity)
  - Try Synthetic Test Mode first
  - Verify audio device is capturing (check spectrum)

Problem: Too many false detections
Solution:
  - Increase sensitivity sliders (try 70-80)
  - Disable detection types you don't need
  - Check for background noise in spectrum

Problem: Detached window not showing
Solution:
  - Check if window is off-screen (alt+space, move)
  - Uncheck and recheck "Detach" button
  - Close and restart application

Problem: Frameless window stuck
Solution:
  - Uncheck "Frameless Mode"
  - Window will get title bar back
  - Move window back to visible area

Problem: Build failed
Solution:
  - Check super_log.txt for error details
  - Ensure Python 3.11 is installed correctly
  - Run as Administrator
  - Delete .venv folder and try again

Problem: EXE won't start
Solution:
  - Check super_log.txt in EXE directory
  - Run from command line to see errors
  - Reinstall Visual C++ Redistributables
  - Try running from Python instead: python app\main.py

═══════════════════════════════════════════════════════════════════════════════
  TECHNICAL DETAILS
═══════════════════════════════════════════════════════════════════════════════

Detection Algorithm:
  1. Capture audio block (default: 2048 samples @ 48kHz)
  2. Convert to mono (average channels)
  3. Apply Hanning window
  4. Compute FFT (Fast Fourier Transform)
  5. Separate into frequency bands:
     - Low: 20-200 Hz (walk)
     - Mid: 200-1500 Hz (run)
     - High: 1500-6000 Hz (shot)
  6. Calculate band ratios relative to total power
  7. Apply sensitivity thresholds
  8. Output detection events

Direction Estimation:
  - Compute RMS energy for left and right channels
  - Balance = (RMS_R - RMS_L) / (RMS_R + RMS_L)
  - Balance range: -1 (left) to +1 (right)
  - Map to radar angle: 90° + balance * 75°

Distance Estimation:
  - Total energy = (RMS_L + RMS_R) / 2
  - Pseudo-distance = energy * 4000
  - Clamped to 10-100 meters
  - NOT real-world distance, relative indicator only

Update Rate:
  - Main timer: 50ms (20 Hz)
  - Audio blocks: depends on sample rate and block size
  - At 48kHz, 2048 samples = ~42ms per block

Translation System:
  - Dictionary-based translations
  - Runtime language switching
  - All UI elements supported
  - Currently: English, Polish

═══════════════════════════════════════════════════════════════════════════════
  DEPENDENCIES
═══════════════════════════════════════════════════════════════════════════════

Required Python packages (installed automatically by build script):
  - PyQt5 >= 5.15.0        # GUI framework
  - pyqtgraph >= 0.13.0    # Scientific graphics and GUI
  - numpy >= 1.21.0        # Numerical computing
  - scipy >= 1.7.0         # Scientific computing
  - sounddevice >= 0.4.0   # Audio I/O (portaudio)
  - soundcard >= 0.4.0     # Audio loopback (Windows)
  - psutil >= 5.9.0        # System information
  - pyinstaller >= 5.0.0   # Build tool (EXE creation)

═══════════════════════════════════════════════════════════════════════════════
  VERSION HISTORY
═══════════════════════════════════════════════════════════════════════════════

v2.3.1-Claude-001 (2024-11-16)
  - NEW: Independent Radar window (Qt.Window with WindowStaysOnTopHint)
  - NEW: Independent LED window (Qt.Window with WindowStaysOnTopHint)
  - NEW: Independent opacity controls for Radar (0-100%)
  - NEW: Independent opacity controls for LED (0-100%)
  - NEW: Frameless window mode (Qt.FramelessWindowHint)
  - NEW: Drag support for frameless windows (mousePressEvent/mouseMoveEvent)
  - NEW: Language switcher EN/PL (button in toolbar)
  - NEW: Complete translation system (TRANSLATIONS dictionary)
  - NEW: Version naming with Claude designation
  - Works when main window is minimized
  - Both windows update in real-time
  - All UI elements translated on language switch

v2.3.0 (2024-11-15)
  - Initial RadarSuite Final release
  - PyQt5 GUI with docked panels
  - pyqtgraph radar, spectrum, waterfall
  - sounddevice and soundcard support
  - Walk/Run/Shot detection with band analysis
  - LED Edge Alert system
  - Synthetic test mode
  - PyInstaller EXE build
  - Profile presets (SB Z SE + Cloud II)

═══════════════════════════════════════════════════════════════════════════════
  LICENSE & CREDITS
═══════════════════════════════════════════════════════════════════════════════

RadarSuite Final v2.3.1-Claude-001
Copyright © 2024 RadarSuite Project

Built with:
  - Python 3.11
  - PyQt5
  - pyqtgraph
  - NumPy & SciPy
  - sounddevice & soundcard
  - PyInstaller

═══════════════════════════════════════════════════════════════════════════════
  SUPPORT
═══════════════════════════════════════════════════════════════════════════════

For issues:
  1. Check super_log.txt for errors
  2. Review Troubleshooting section above
  3. Try Synthetic Test Mode to isolate problems

All logs are saved to super_log.txt with timestamps and full details.

═══════════════════════════════════════════════════════════════════════════════

            Thank you for using RadarSuite Final v2.3.1-Claude-001!

═══════════════════════════════════════════════════════════════════════════════
