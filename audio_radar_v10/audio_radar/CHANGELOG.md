# Changelog

All notable changes to Audio Radar will be documented in this file.

## [v10.2] - 2025-11-09

### Added
- **PyQt5 Control Panel GUI** - New graphical interface for easy configuration
- **Input Gain Slider** - Amplify audio signal from 0.1x to 10.0x
- **Adjustable Threshold Slider** - Fine-tune detection sensitivity (0.001 - 0.200)
- **Auto-Calibration Button** - Automatically analyze background noise and set optimal threshold
- **Signal Strength Indicator** - Real-time visual feedback with color coding
  - 🔴 Red: Signal too weak (< 1%)
  - 🟡 Orange: Weak signal (1-5%)
  - 🟢 Green: Good signal (> 5%)
- **Pre-Amplifier Checkbox** - Quick x5 boost for very weak signals
- **Device Selection** - Choose audio input device from GUI dropdown
- **Visual Feedback** - Color-coded gain and threshold indicators

### Fixed
- Weak audio signals now detectable through software amplification
- Users can adjust sensitivity without changing system volume
- Better feedback on signal quality

### Improved
- No need to edit config files or source code to adjust sensitivity
- Software-based gain control for different audio setups
- Adaptive to various hardware configurations

### Target Issue
- User reported Peak = 0.005 (too low for default threshold 0.05)
- Now users can amplify signal x10 to reach Peak = 0.05
- Or lower threshold to 0.005 to match weak signal levels
- Provides both solutions for maximum flexibility

## [v10] - Previous Release

Initial release with:
- Real-time audio capture
- Sound event detection (footsteps and gunshots)
- Pygame visualization with radial bars
- Configurable bar sizes and transparency
- Custom audio device selection via config.json
- Versioned logging
