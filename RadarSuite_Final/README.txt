╔══════════════════════════════════════════════════════════════════════════════╗
║                      RadarSuite Final v3.0.5-Claude-001                        ║
║    Advanced 3D Audio Radar with Multi-Target Tracking & Human Detection       ║
╚══════════════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════════
  VERSION INFO
═══════════════════════════════════════════════════════════════════════════════

Version: v3.0.5-Claude-001 - "3D TACTICAL AWARENESS"
Release Date: 2025-11-16
Build: Production - Major Update (Modules 5/16 Complete)

🚀 NEW IN v3.0.5 - MULTI-TARGET TRACKING (MODULE 5):
  ✨ SIMULTANEOUS TARGET TRACKING
    - Track up to 3 targets at once
    - Intelligent target matching and merging
    - Confidence-based persistence (targets fade over time)
    - Color-coded by type: Green=footsteps, Cyan=voice, Red=shots
    - Movement history tracking (10 positions per target)

🌐 NEW IN v3.0.4 - 3D SPHERE RADAR (MODULE 4):
  ✨ FULL 3D SPATIAL AWARENESS
    - Interactive 3D OpenGL radar visualization
    - Spherical distance grid (25m, 50m, 75m, 100m)
    - Elevation tracking: -45° to +45°
    - Color-coded axes: Red=X, Green=Y, Blue=Z
    - Frequency-based elevation estimation
    - Camera rotation and zoom controls
    - Tab switching between 2D and 3D radar

🎮 NEW IN v3.0.3 - GAME & AUDIO DETECTION (MODULE 3):
  ✨ AUTOMATIC GAME PROCESS DETECTION
    - Detects Unreal Engine 5, Unity, Source Engine, CryEngine
    - Specific games: ARC Raiders, Tarkov, CS2, Valorant, Apex, PUBG
    - Real-time audio source monitoring
    - Active/Inactive source visualization (green/red)
    - Scans every 2-5 seconds

🎨 NEW IN v3.0.2 - RADAR-FOCUSED INTERFACE REDESIGN:
  ✨ OPTIMIZED LAYOUT FOR MAXIMUM RADAR VISIBILITY
    - Radar as MAIN CENTRAL WIDGET (70%+ screen space)
    - Previously: Radar was a dock widget (limited space)
    - Now: Radar dominates the interface - best visualization
    - Professional tactical display design

  ✨ COMPACT PANELS & DOCKS
    - Spectrum & Waterfall: Bottom dock, max 180px height (previously central)
    - Device Panel: Left dock, 280px width (compact controls)
    - Detection Panel: Right dock, 320px width (all analysis info)
    - LED Alert: Bottom dock, 120px height (non-intrusive)

  ✨ SCREEN SPACE ALLOCATION
    ┌─────────────────────────────────────────────────────┐
    │  Toolbar (Start, Language, Controls)               │
    ├────────┬─────────────────────────────┬──────────────┤
    │ Device │                             │  Detection   │
    │ Panel  │         RADAR              │  Panel       │
    │ 280px  │      (MAIN/LARGEST)         │  320px       │
    │        │                             │              │
    ├────────┴──────────────┬──────────────┴──────────────┤
    │ Spectrum/Waterfall    │  LED Alert                  │
    │ 180px height          │  120px height               │
    └───────────────────────┴─────────────────────────────┘

  ✨ BENEFITS
    - Maximum radar visualization quality
    - Easier threat spotting (largest display area)
    - Spectrum/Waterfall still accessible but not dominating
    - All detection info visible in side panels
    - Professional tactical interface

🎯 NEW IN v3.0.1 - HUMAN VOICE DETECTION (FORMANT ANALYSIS):
  ✨ FORMANT FREQUENCY ANALYSIS
    - F1 detection (300-1000 Hz): jaw opening
    - F2 detection (800-2500 Hz): tongue position
    - F3 detection (2000-3500 Hz): lip rounding
    - Peak detection in each formant range
    - Formant strength analysis vs. total power

  ✨ PITCH DETECTION & CLASSIFICATION
    - Male voice: 85-180 Hz
    - Female voice: 165-255 Hz
    - Child voice: 250-400 Hz
    - Automatic gender/age classification
    - Fundamental frequency extraction

  ✨ VOICE INTENSITY DETECTION
    - WHISPER: < -35 dB (quiet, stealthy)
    - NORMAL: -35 to -15 dB (regular speech)
    - SHOUT: > -15 dB (yelling, commands, panic)
    - Real-time intensity classification

  ✨ BREATHING PATTERN RECOGNITION
    - Heavy breathing detection (100-300 Hz modulation)
    - Distinguishes breathing from voice
    - Indicates player running/exertion
    - Independent detection when not talking

  ✨ COMMUNICATION PATTERN DETECTION
    - Sustained speech detection (> 1 second continuous)
    - Differentiates single sounds vs. conversation
    - Voice activity rate (detections per minute)
    - Speech duration tracking

  📊 NEW UI PANEL: "Human Voice Analysis (v3.0)"
    - Confidence percentage (formant-based scoring)
    - Voice type (male/female/child with icons)
    - Pitch frequency (Hz)
    - Intensity level (whisper/normal/shout)
    - Communication status (TALKING indicator)
    - Breathing detection (heavy breathing alert)

🎯 FROM v3.0.0 - HUMAN FOOTSTEP PATTERN RECOGNITION:
  ✨ TEMPORAL CADENCE ANALYSIS
    - Detects human walking rhythm (1.5-2.5 steps per second)
    - Detects human running rhythm (3.0-4.5 steps per second)
    - Real-time step interval tracking
    - Pattern regularity scoring

  ✨ L-R PATTERN DETECTION
    - Left-Right-Left-Right foot classification
    - Stereo channel analysis for weight distribution
    - Automatic foot identification (Left/Right/Center)
    - Pattern consistency verification

  ✨ SURFACE TYPE DETECTION
    - HARD surfaces: concrete, metal (high detail frequencies)
    - MEDIUM surfaces: wood, tile (moderate detail)
    - SOFT surfaces: carpet, grass, dirt (low detail)
    - Frequency signature analysis

  ✨ DISTANCE ESTIMATION
    - Audio loudness-based distance calculation
    - Range: 1m - 100m
    - Real-time distance updates
    - Rough approximation (improves with calibration)

  ✨ CONFIDENCE SCORING
    - 0-100% confidence based on pattern regularity
    - Higher score = more certain it's a human
    - Green (75-100%), Orange (50-75%), Yellow (0-50%)

  ✨ GAIT CLASSIFICATION
    - WALK: slower, regular rhythm
    - RUN: faster, higher intensity
    - Real-time classification

  📊 NEW UI PANEL: "Human Footstep Analysis (v3.0)"
    - Live confidence percentage
    - Cadence display (steps/second)
    - Foot indicator (L/R with icons)
    - Surface type
    - Distance estimate
    - Gait type (walk/run icons)

FIXES FROM v2.3.2-Claude-001:
  ✓ Complete translation system (EN/PL)
  ✓ Radar target clearing on detection events only

FEATURES FROM v2.3.x:
  ✓ Independent Radar/LED windows
  ✓ Frameless window mode
  ✓ Language switcher EN/PL
  ✓ Opacity controls

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
     - Make sure "Add Python to PATH" is checked during installation

  2. Install Microsoft Visual C++ Redistributable (REQUIRED!)
     - Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe
     - Required for PortAudio (sounddevice/soundcard audio backend)
     - Without this, you'll get "cannot load library" error 0xce

  3. Disable Antivirus temporarily (optional but recommended)
     - Some antivirus software may block PortAudio DLL during build
     - Windows Defender SmartScreen may also interfere
     - Re-enable after build completes

Build Steps:
  1. Double-click: RUN_BUILD_ALL.cmd
  2. Wait for build to complete (~5-10 minutes)
  3. Find EXE in: dist\RadarSuite_Final\RadarSuite_Final.exe

Troubleshooting Build Errors:
  - ERROR "No module named 'OpenGL'"
    → The build script now auto-installs PyOpenGL
    → If still failing, manually install: pip install PyOpenGL PyOpenGL_accelerate
    → Required for 3D radar visualization (Module 4)

  - ERROR "cannot load library libportaudio64bit.dll error 0xce"
    → Install Visual C++ Redistributable (see Prerequisites #2)
    → Try running RUN_BUILD_ALL.cmd as Administrator
    → Disable Windows Defender / Antivirus temporarily

  - ERROR "Module verification failed"
    → Check super_log.txt for details
    → Ensure Python 3.11 is installed correctly
    → Try deleting .venv folder and rebuild
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
