# AudioRadar v10.2 - GUI Features Documentation

## Overview

AudioRadar v10.2 introduces a comprehensive PyQt5-based control panel GUI that solves the critical issue of weak audio signals not being detected. This allows users to amplify weak signals and adjust sensitivity without changing system volume settings.

## Problem Statement

**User Issue:** Audio signal too weak for detection
- System volume: 100% ✓
- Playback volume: 100% ✓
- Peak values: 0.005 (only 0.5%)
- Default threshold: 0.05 (5%)
- **Result:** Footsteps not detected ✗

**User cannot increase volume any more - need SOFTWARE solution!**

## Solution: Software-Based Gain & Threshold Control

### GUI Control Panel

```
┌─────────────────────────────────────────────────────────────┐
│         Audio Radar v10.2 - Control Panel                   │
├─────────────────────────────────────────────────────────────┤
│  [Controls] [Info]                                          │
│                                                              │
│  Audio Radar v10.2                                          │
│  ═══════════════════════                                    │
│                                                              │
│  Audio Input Device:                                        │
│  [▼ Device Dropdown                        ] [🔄 Refresh]  │
│                                                              │
│  Input Gain (Amplification):                                │
│  [━━━━━━━━●━━━━━━━━━━━━━━━━━━━━━━━━] [1.0x]              │
│   0.1x                               10.0x                  │
│                                                              │
│  Detection Threshold:                                       │
│  [━━━━━━━━━━━━●━━━━━━━━━━━━━━━━━━━━] [0.050]             │
│   0.001                             0.200                   │
│                                                              │
│  ☐ Enable Pre-Amplifier (x5 boost for weak signals)        │
│                                                              │
│  Signal Strength:                                           │
│  [████████                                    ] 8%          │
│                                                              │
│  [🎯 Auto-Calibrate Threshold]                             │
│                                                              │
│  [▶ START Detection]                                       │
│                                                              │
│  Status: Ready                                              │
└─────────────────────────────────────────────────────────────┘
```

## Features

### 1. Input Gain Control
- **Range:** 0.1x to 10.0x amplification
- **Default:** 1.0x (no amplification)
- **Purpose:** Amplify weak audio signals in software
- **Color Coding:**
  - Gray: < 1.0x (attenuation)
  - Cyan: 1.0x (normal)
  - Green: 1.0x - 3.0x (boosted)
  - Orange: > 3.0x (high boost)

**How it works:**
```python
# Original weak signal
peak_original = 0.005  # Only 0.5%

# Apply 10x gain
peak_amplified = 0.005 × 10.0 = 0.05  # Now 5%!

# Detection now works! ✓
```

### 2. Adjustable Detection Threshold
- **Range:** 0.001 to 0.200
- **Default:** 0.050 (5%)
- **Purpose:** Fine-tune detection sensitivity
- **Color Coding:**
  - Red: < 0.010 (very sensitive - more false positives)
  - Orange: 0.010 - 0.050 (sensitive)
  - Green: > 0.050 (normal)

**Alternative solution:**
```python
# Instead of amplifying signal
peak = 0.005  # Weak signal

# Lower threshold to match
threshold = 0.003  # Below signal level

# Detection works! ✓
```

### 3. Signal Strength Indicator
- **Real-time visual feedback**
- **Progress bar: 0-100%**
- **Color-coded status:**
  - 🔴 **Red (< 1%):** Signal too weak - increase gain!
  - 🟡 **Orange (1-5%):** Weak signal - may need adjustment
  - 🟢 **Green (> 5%):** Good signal strength

### 4. Auto-Calibration
- **Button:** 🎯 Auto-Calibrate Threshold
- **Process:**
  1. Records 10 seconds of background noise
  2. Analyzes RMS and peak levels
  3. Calculates optimal threshold (2× background peak)
  4. Automatically applies setting
- **When to use:** Before starting detection to optimize for your environment

### 5. Pre-Amplifier Quick Boost
- **Checkbox:** Enable Pre-Amplifier (x5 boost)
- **Effect:** Instantly sets gain to 5.0x
- **Use case:** Very weak signals that need immediate boost

### 6. Device Selection
- **Dropdown:** Choose audio input device
- **Refresh button:** Re-scan available devices
- **Displays:** Device index and name

## Usage Scenarios

### Scenario 1: Weak Signal (Peak = 0.005)
**Problem:** Default threshold 0.050, signal only reaches 0.005
**Solution A - Amplify Signal:**
1. Move "Input Gain" slider to 10.0x
2. Signal becomes: 0.005 × 10 = 0.050
3. Detection works! ✓

**Solution B - Lower Threshold:**
1. Move "Detection Threshold" to 0.003
2. Threshold now below signal level
3. Detection works! ✓

### Scenario 2: Unknown Signal Strength
**Use Auto-Calibration:**
1. Click "🎯 Auto-Calibrate Threshold"
2. Turn off all game audio
3. Wait 10 seconds
4. Program analyzes background: Peak = 0.002
5. Sets threshold = 0.004 (2× background)
6. Start game audio
7. Detection optimized! ✓

### Scenario 3: Very Weak Signal
**Use Pre-Amplifier:**
1. Check "Enable Pre-Amplifier"
2. Gain automatically set to 5.0x
3. Monitor Signal Strength indicator
4. Adjust threshold if needed
5. Detection works! ✓

## Technical Details

### Audio Processing Pipeline

```
Input Audio → Apply Gain → Convert to Mono → Analyze
                ↓                              ↓
        amplified = audio × gain          peak = max(abs(audio))
                                          std = std(audio)
                                              ↓
                                    Compare to Threshold
                                              ↓
                                    Trigger Event (footstep/shot)
```

### Gain Application

```python
def process_audio(self, audio_data):
    """Process audio with gain applied"""
    # Apply gain amplification
    if hasattr(self, 'current_gain'):
        audio_data = audio_data * self.current_gain
    
    # Continue with normal processing
    rms = np.sqrt(np.mean(audio_data**2))
    peak = np.max(np.abs(audio_data))
    # ...
```

### Custom Threshold Detection

```python
def detect_event_with_threshold(self, samples, threshold):
    """Detect event using custom threshold"""
    # Convert to mono
    mono = samples.mean(axis=1) if samples.ndim == 2 else samples
    
    # Calculate statistics
    peak = np.max(np.abs(mono))
    std = np.std(mono)
    
    # Gunshot: very loud (hardcoded threshold 0.6)
    if peak > 0.6:
        return 'shot'
    
    # Footstep: use custom threshold
    if std > threshold:
        return 'footstep'
    
    return None
```

## Running the GUI

### Method 1: Launcher Script
```bash
cd audio_radar_v10/audio_radar
python run_gui.py
```

### Method 2: Direct Import
```bash
cd audio_radar_v10/audio_radar
python -m gui
```

### Method 3: Classic Mode (Pygame only - no GUI)
```bash
cd audio_radar_v10/audio_radar
python main.py
```

## Requirements

```
Python 3.8+
PyQt5 (for GUI)
sounddevice (for audio capture)
numpy (for signal processing)
pygame (for visualization)
```

Install with:
```bash
pip install PyQt5 sounddevice numpy pygame
```

## Keyboard Shortcuts (Visualization Window)

- **Z/X:** Increase/decrease bar width
- **C/V:** Increase/decrease bar height
- **B/N:** Increase/decrease bar transparency

## Troubleshooting

### Issue: "PyQt5 not available"
**Solution:** Install PyQt5
```bash
pip install PyQt5
```

### Issue: Signal Strength always red
**Solution:** 
1. Increase Input Gain to 2.0x+
2. Or lower Detection Threshold
3. Or use Auto-Calibration

### Issue: Too many false detections
**Solution:**
1. Increase Detection Threshold
2. Decrease Input Gain
3. Check Signal Strength is green (> 5%)

### Issue: No audio devices shown
**Solution:**
1. Click "🔄 Refresh Devices"
2. Check audio loopback is enabled (e.g., "Stereo Mix")
3. Verify sounddevice installation

## Version History

### v10.2 (2025-11-09)
- ✨ Added PyQt5 GUI control panel
- ✨ Added Input Gain control (0.1x - 10.0x)
- ✨ Added Adjustable Threshold (0.001 - 0.200)
- ✨ Added Signal Strength indicator
- ✨ Added Auto-Calibration feature
- ✨ Added Pre-Amplifier checkbox
- 🐛 Fixed weak signal detection issue
- 📝 Updated documentation

### v10 (Previous)
- Initial release with Pygame visualization
- Basic event detection
- Config file support

## Credits

Developed to solve real user needs - users with weak audio hardware can now use AudioRadar effectively without needing to change system settings or buy new audio equipment.
