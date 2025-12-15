# 🎯 Radar Games ML v4.3.1

**Real-time audio radar for tactical FPS games with ML-powered sound detection**

![Version](https://img.shields.io/badge/version-4.3.1--k0002-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-green)
![License](https://img.shields.io/badge/license-MIT-brightgreen)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)

---

## 📋 Overview

Radar Games ML to zaawansowana aplikacja analizy audio w czasie rzeczywistym, która wykrywa i wizualizuje źródła dźwięków w grach FPS (kroki, strzały, maszyny). System wykorzystuje WASAPI loopback, przetwarzanie sygnałów DSP oraz modele uczenia maszynowego do precyzyjnej lokalizacji 3D.

### ✨ Key Features

- **🎮 Real-time Audio Analysis** - 20 FPS processing with <50ms latency
- **🤖 ML-Powered Detection** - YAMNet + custom models for footstep/shot classification
- **📡 3D Spatial Localization** - 360° horizontal + elevation tracking
- **🎯 Multi-Target Tracking** - Up to 3 simultaneous targets with threat prioritization
- **🌐 Advanced Visualizations** - Military HUD radar, 3D wallhack view, spectrum analyzer
- **⚡ GPU Acceleration** - AMD Radeon RX 7900 GRE optimizations
- **🎨 Modern UI** - PyQt6-based interface with dark theme and detachable windows
- **📊 Profiling Dashboard** - Real-time performance monitoring

---

## 🚀 Quick Start

### Prerequisites

- **Windows 10/11** or **Linux** (Ubuntu 20.04+)
- **Python 3.11+**
- **Sound card** with loopback support (e.g., Sound Blaster Z SE, Virtual Audio Cable)
- **GPU** (optional): AMD Radeon for GPU-accelerated FFT

### Installation

```bash
# Clone repository
git clone https://github.com/arkadiuszpopiel-eng/AudioRadar.git
cd AudioRadar/Radar_Games_ML_v4.3

# Install dependencies
pip install -r requirements.txt

# Run application
python app/main.py
```

### First Launch

1. **Select Audio Source**
   - Choose loopback device in Settings → Device Panel
   - Recommended: Sound card with 5.1/7.1 support

2. **Start Detection**
   - Press **▶ START** button
   - Audio visualization should appear immediately

3. **Configure Detection**
   - Adjust thresholds in Settings → Detection Panel
   - Enable/disable specific sound types (footsteps, shots, machines)

---

## 📊 Version 4.3.1-k0002 Highlights

### 🔴 Critical UI Freeze Fix

**Problem:** Application froze when pressing buttons due to blocking `.result(timeout=1.0)` calls
**Solution:** Implemented non-blocking detection with result caching
**Impact:** **20 FPS** (was 0.5-1.0 FPS) - **2000% performance improvement!**

### ✅ Major Changes (POPRAWKI #1-5)

1. **Non-blocking Detection** - Fixed main.py:1019, 1073 blocking calls
2. **Cache Timeout Fallback** - Auto-reset stale results after 5s
3. **QA Test Improvements** - Widget detection for UIBuilder pattern
4. **Tick Performance Test** - Automatic blocking call detection
5. **MVC Documentation** - Complete architecture guide

### 🚀 New Features (ULEPSZENIA #1-5)

1. **AsyncDetectionPipeline** - Fully non-blocking detection queue
2. **GPU Benchmark** - FFT performance testing and optimization
3. **Adaptive Frame Skip** - Intelligent frame skipping under load
4. **Profiling Dashboard** - Real-time FPS, GPU, cache monitoring
5. **Unit Tests** - ApplicationController test coverage

### 📈 Quality Metrics

```
✓ 266/266 QA tests PASSED (100%)
✓ 0 compilation errors
✓ 0 warnings
✓ Main.py: +65 lines (non-blocking detection)
✓ New files: +95KB (code, docs, tests)
```

---

## 🏗️ Architecture

### MVC Pattern (v4.3.1)

```
┌─────────────────────────────────────────┐
│         ApplicationController           │ ← Controller
│  - Timer management (20 FPS)            │
│  - State synchronization                │
│  - Lifecycle coordination               │
└────────┬────────────────────────────────┘
         │
    ┌────┴─────┐
    │          │
┌───▼──┐   ┌──▼───────┐
│ View │   │  Model   │
│ (UI) │   │ (Logic)  │
└──────┘   └──────────┘
```

**See:** [docs/MVC_ARCHITECTURE.md](Radar_Games_ML_v4.3/docs/MVC_ARCHITECTURE.md)

### Core Modules

| Module | Purpose | Lines |
|--------|---------|-------|
| `main.py` | Main window (View) | 1914 |
| `core/application_controller.py` | MVC Controller | 341 |
| `audio/engine.py` | WASAPI loopback capture | 650 |
| `detection/worker.py` | Parallel detection pipeline | 320 |
| `ml/detector.py` | ML inference (YAMNet) | 280 |
| `tracking/target.py` | Multi-target tracker | 245 |

---

## 📚 Documentation

### User Guides

- [Installation Guide](Radar_Games_ML_v4.3/docs/INSTALLATION.md)
- [Usage Guide](Radar_Games_ML_v4.3/docs/USAGE.md)
- [Configuration](Radar_Games_ML_v4.3/docs/CONFIGURATION.md)

### Developer Docs

- [MVC Architecture](Radar_Games_ML_v4.3/docs/MVC_ARCHITECTURE.md) ⭐ NEW v4.3.1
- [API Reference](Radar_Games_ML_v4.3/docs/API.md)
- [Build Instructions](Radar_Games_ML_v4.3/docs/BUILD.md)
- [Module Overview](Radar_Games_ML_v4.3/docs/MODULES.md)

### Reports & Analysis

- [QA Final Report](Radar_Games_ML_v4.3/QA_RAPORT_FINALNY.md) ⭐ NEW v4.3.1
- [Grade A+ Report](Radar_Games_ML_v4.3/Report/GRADE_A_REPORT_k0006.md)
- [Deep Analysis](Radar_Games_ML_v4.3/Report/DEEP_ANALYSIS_REPORT.md)

---

## 🎮 Supported Games

- ✅ **Arc Raiders** (primary target)
- ✅ **CS:GO / CS2**
- ✅ **Valorant**
- ✅ **Apex Legends**
- ✅ **Call of Duty series**
- ✅ **Any FPS game** with audio output

---

## 🧪 Testing

### Run QA Tests

```bash
cd Radar_Games_ML_v4.3
python qa_comprehensive_test.py
```

Expected output:
```
✓ Passed: 266/266 (100%)
✗ Failed: 0
⚠ Warnings: 0
```

### Run Unit Tests

```bash
cd Radar_Games_ML_v4.3/app
python -m pytest tests/core/test_application_controller.py -v
```

---

## 🛠️ Building

### Windows Executable

```bash
cd Radar_Games_ML_v4.3
python build_exe.py
```

Output: `dist/RadarGamesML.exe`

### Linux Binary

```bash
cd Radar_Games_ML_v4.3
python build_linux.py
```

Output: `dist/RadarGamesML`

**See:** [docs/BUILD.md](Radar_Games_ML_v4.3/docs/BUILD.md)

---

## ⚙️ Configuration

### Audio Settings

```python
# config.json
{
  "audio": {
    "use_loopback": true,
    "sample_rate": 48000,
    "blocksize": 2048,
    "device": null  # Auto-detect
  }
}
```

### Detection Settings

```python
{
  "detection": {
    "energy_threshold": 0.02,
    "footstep_enabled": true,
    "shot_enabled": true,
    "machine_enabled": false
  }
}
```

**See:** [docs/CONFIGURATION.md](Radar_Games_ML_v4.3/docs/CONFIGURATION.md)

---

## 🐛 Known Issues

### v4.3.1-k0002

- ✅ **FIXED:** UI freeze on button press (blocking detection)
- ✅ **FIXED:** Radar widget not responding to START button
- ✅ **FIXED:** Tab scaling issues
- ⚠️ **Minor:** GPU utilization reporting (simulated values)

**See:** [docs/KNOWN_ISSUES.md](Radar_Games_ML_v4.3/docs/KNOWN_ISSUES.md)

---

## 📈 Performance

### Benchmarks (v4.3.1-k0002)

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| FPS | 0.5-1.0 | 20.0 | +2000% |
| Tick Time | 1000-2000ms | 40-50ms | -97.5% |
| UI Freeze | Yes | No | ✅ Fixed |
| Detection Lag | High | <50ms | ✅ Optimized |

### System Requirements

**Minimum:**
- CPU: Intel i5-8400 / AMD Ryzen 5 2600
- RAM: 4 GB
- GPU: None (CPU fallback)
- OS: Windows 10 / Ubuntu 20.04

**Recommended:**
- CPU: Intel i7-10700K / AMD Ryzen 7 5800X
- RAM: 8 GB
- GPU: AMD Radeon RX 7900 GRE / NVIDIA RTX 3060
- OS: Windows 11 / Ubuntu 22.04

---

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

### Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest app/tests/ -v

# Run linting
flake8 app/
```

---

## 📝 Changelog

### [4.3.1-k0002] - 2025-12-14

**CRITICAL UI FREEZE FIX + PERFORMANCE OPTIMIZATION**

#### Fixed
- 🔴 UI freeze on button press (blocking `.result()` calls)
- ✅ Radar widget not responding to START
- ✅ Tab scaling issues
- ✅ Widget initialization false positives

#### Added
- ⚡ Non-blocking detection pipeline
- 📊 GPU FFT benchmark tool
- 🎯 Adaptive frame skip strategy
- 📈 Profiling dashboard widget
- ✅ ApplicationController unit tests
- 📚 MVC architecture documentation

#### Performance
- FPS: 0.5-1.0 → 20.0 (+2000%)
- Tick time: 1000-2000ms → 40-50ms (-97.5%)

**Full changelog:** [docs/CHANGELOG.md](Radar_Games_ML_v4.3/docs/CHANGELOG.md)

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

## 🙏 Acknowledgments

- **YAMNet** - Google Research audio classification model
- **PyQt6** - Cross-platform GUI framework
- **NumPy/SciPy** - Scientific computing libraries
- **PyAudioWPatch** - WASAPI loopback support

---

## 📧 Contact

**Author:** Arkadiusz Popiel
**GitHub:** [@arkadiuszpopiel-eng](https://github.com/arkadiuszpopiel-eng)
**Project:** [AudioRadar](https://github.com/arkadiuszpopiel-eng/AudioRadar)

---

**⭐ If you find this project useful, please consider starring it on GitHub!**
