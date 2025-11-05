# Changelog

All notable changes to Audio Radar will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.10.1] - 2024-11-05

### Added
- **Calibration Tool**: Interactive `calibrate.py` utility for finding optimal detection thresholds
  - Real-time audio statistics display
  - Automatic threshold recommendations
  - One-click config.json updates
- **Enhanced Detection Algorithms**:
  - Bandpass filtering for footsteps (2-8 kHz) and gunshots (0.2-12 kHz)
  - Background noise adaptation with exponential smoothing
  - Distance estimation based on amplitude
  - Full directional detection with multi-channel support (stereo, 5.1, 7.1)
- **Comprehensive Documentation**:
  - Detailed USER_GUIDE.md with game-specific configurations
  - Step-by-step INSTALL.md
  - Updated README.md with features and usage
  - In-code documentation improvements
- **Testing Infrastructure**:
  - Unit test suite for sound_analysis module
  - Tests for detection, filtering, and distance estimation
- **Project Infrastructure**:
  - .gitignore for clean repository
  - requirements.txt for dependency management
  - setup.py for proper package installation
  - MIT LICENSE
  - QUICKSTART.cmd for Windows users
- **Configuration Enhancements**:
  - Extended config.json with detection, audio, and visualization sections
  - Configurable frequency ranges for filtering
  - Customizable fade duration and colors

### Changed
- Enhanced `sound_analysis.py` with scipy-based filtering
- Updated `main.py` to support directional detection
- Improved `visualization.py` to accept direction and distance parameters
- Config loading now supports nested dictionaries with deep merge

### Fixed
- Import handling for both module and script execution modes
- Configuration validation and error handling

## [0.10.0] - 2024-10

### Added
- Initial public release
- Basic real-time audio capture via WASAPI loopback
- Simple heuristic detection for footsteps and gunshots
- 8-way radar visualization with pygame
- Keyboard controls for adjusting display (Z/X/C/V/B/N)
- Configuration file support (config.json)
- Device listing with --list-devices flag

### Features
- Stereo audio support
- RMS and peak-based detection
- Configurable bar width, height, and transparency
- Logging to versioned log files
- Cross-platform Python support (Windows focus)

---

## Version History

### v10 (Current)
- Enhanced detection with filtering and multi-channel support
- Calibration tool and comprehensive documentation
- Test suite and improved project structure

### v9
- Previous iteration with basic functionality
- Simple detection algorithms
- Basic visualization

### Earlier Versions
- Concept development and prototypes
- Various test packages and iterations

---

For older version details, see the repository history and test packages in the archive folders.
