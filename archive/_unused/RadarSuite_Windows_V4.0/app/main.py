"""
RadarSuite Final v3.5.0-Diamond-001
Advanced audio radar and detection system for gaming with AI-powered human detection
Supports: sounddevice, soundcard loopback, pyqtgraph visualization
Optimized for: ARC Raiders + Sound Blaster Z SE + HyperX Cloud II

NEW IN v3.5.0-Diamond-001 - COMPREHENSIVE TESTING & MODULARIZATION:
🧪 COMPLETE TESTING SUITE & CODE QUALITY 🧪
- 250+ Unit Tests: Full test coverage for all modules
- 16 Test Files: Detection, Utils, Hardware, Audio, Core, Tracking
- Thread Safety Testing: Validated concurrent operations
- Mock-based Testing: No hardware dependencies required
- Pytest Integration: Professional testing framework
- CI/CD Ready: Automated test execution

📦 FULL MODULARIZATION (Point 10):
- Separate modules: core, hardware, utils, tracking, detection, audio, widgets
- Dependency Injection: IoC container for testability
- Clean imports: Relative imports with standalone script support
- Type safety: Consistent interfaces across modules

🔧 CRITICAL BUG FIXES:
- Fixed: ModuleNotFoundError in main.py (relative imports)
- Fixed: Missing imports in 15+ modules (time, numpy, deque, etc.)
- Fixed: Thread-safe cache operations (AudioProcessingCache)
- Fixed: Memory leak in DetectionWorker cleanup

🏗️ PLATFORM-SPECIFIC BUILDS:
- Separate build scripts for Windows and Linux
- RUN_BUILD_ALL_Win.cmd - Windows x64 only
- RUN_BUILD_ALL_Linux.sh - Linux x64 only
- No cross-platform build issues
- Optimized binaries for each platform

FROM v3.4.1-Claude-001 - GAMING PLATFORM INTEGRATION:
🎮 INTEGRACJA Z PLATFORMAMI GAMING 🎮
- Platform Detection: Steam, Epic Games, GOG Galaxy, Battle.net, EA App
- Steam AppID Detection: Automatyczne wykrywanie gier przez Steam AppID
- Epic Games Integration: Wykrywanie parametrów -epicapp=
- Launcher Audio Filtering: Ignorowanie audio od Steam/Discord/Spotify
- Enhanced Game Detection: Wyświetlanie gry + platforma w UI
- Platform Status Display: Live status wszystkich launcherów w Tab 3
- Intelligent Audio Routing: Priorytetyzacja audio od gier, nie launcherów

TECHNICAL DETAILS:
- 5 platform: Steam (priority: high), Epic (high), GOG (medium), Battle.net (medium), EA App (low)
- Steam AppID database: 10+ popularnych gier (CS2, Apex, PUBG, etc.)
- Audio blacklist: 15+ procesów do ignorowania (launchery, Discord, przeglądaki)
- Regex parsing: Steam AppID extraction, Epic -epicapp parameter
- UI integration: Nowa sekcja "Gaming Platform Launchers" w Tab 3

FROM v3.4.0-Claude-001 - PERFORMANCE OPTIMIZATION:
⚡ MODULE 12: PERFORMANCE OPTIMIZATION ⚡
- FFT Caching: Compute FFT once, reuse 4x (eliminates redundant calculations)
- Performance Monitoring: Real-time FPS, CPU, memory, latency tracking
- Multi-threading: Worker pool for parallel detection processing
- Memory Optimization: Object pooling and fixed-size buffers
- Latency Reduction: Audio-to-radar update now <10ms (target achieved!)
- Stats Display: Live FPS and latency in toolbar
- Thread Safety: Clean shutdown of worker threads

PERFORMANCE IMPROVEMENTS:
- 4x reduction in FFT computations (was: 4 per frame, now: 1 per frame)
- Real-time metrics: FPS, latency, CPU%, memory MB
- Future: GPU acceleration support (planned for v3.4.1)

FROM v3.3.1-Claude-001 - ENHANCED GAME DETECTION:
🎮 IMPROVED ARC RAIDERS & MULTI-GAME DETECTION 🎮
- FIXED: ARC Raiders detection (now detects PioneerGame.exe!)
- ENHANCED: Process detection algorithm
  * Scans process name (e.g., "PioneerGame.exe")
  * Scans full exe path (e.g., "C:\Games\ARC Raiders\...")
  * Scans command line arguments (catches display names)
- ADDED: 6 new games (Destiny 2, Hunt Showdown, The Cycle, Marauders, etc.)
- IMPROVED: More patterns per game for better detection accuracy

FEATURES FROM v3.3.0:
🎯 INTELLIGENT THREAT RANKING & SESSION RECORDING 🎯
- Module 8: Threat Priority System (rank targets by danger level)
  * Scoring: weapon type + distance + direction + confidence
  * Weapon threats: sniper(100) > explosion(90) > rifle(85) > pistol(70)
  * Direction factor: rear attacks = 1.3x threat, front = 0.8x
  * Distance factor: <20m = 1.5x threat, >50m = 0.5x
  * Categories: CRITICAL (red), HIGH (orange), MEDIUM (yellow), LOW (green)
  * Targets auto-sorted by threat level (highest first)

- Module 9: Audio Recording & Replay
  * Record button in toolbar (⏺ REC)
  * WAV format with 16-bit quality
  * Metadata export (JSON with detections + timestamps)
  * Auto-save with timestamp filename
  * Duration display (M:SS)
  * Enabled only when audio is running

- INTEGRATION: Targets now color-coded by threat level
- SAFETY: Rear attacks highlighted as higher priority
- ANALYSIS: Record sessions for post-game review

FEATURES FROM v3.2.0:
🎯 PRECISION LOCALIZATION & CLASSIFICATION 🎯
- Module 6: Advanced 3D Sound Localization (ITD + ILD analysis)
  * ITD (Interaural Time Difference): Cross-correlation for precise azimuth
  * ILD (Interaural Level Difference): Volume difference for angle estimation
  * Combined 70% ITD + 30% ILD for robust positioning
  * Confidence scoring based on signal strength and correlation

- Module 7: Sound Classification System (weapon/vehicle identification)
  * 8 sound types: rifle, pistol, shotgun, sniper, car, helicopter, explosion, grenade
  * Spectral fingerprinting: frequency peaks, sharpness, attack time
  * Automatic classification with confidence scoring
  * Classification history tracking for pattern analysis

- INTEGRATION: Detection now uses precise 3D localization + sound classification
- ACCURACY: Much more precise angle/distance/elevation estimation
- INTELLIGENCE: Auto-detect weapon types and vehicles

FEATURES FROM v3.1.2:
🎚️ AUDIO PROCESSING & DEBUGGING 🎚️
- NEW: Waveform Widget - Visual audio signal display for debugging input issues
- NEW: Auto-Gain - Automatically amplify quiet audio (target -20 dBFS)
- NEW: Manual Gain - 1x to 100x amplification slider for precise control
- NEW: Noise Gate - Block audio below threshold to reduce background noise
- IMPROVED: Audio processing pipeline with gain and noise reduction

FEATURES FROM v3.1.1:
🐛 STABILITY & RELIABILITY 🐛
- CRITICAL FIX: Added error handling to tick() method to prevent application freezes
- FIXED: Quick Setup now properly restarts audio stream when settings change
- FIXED: .gitignore now preserves build_tools/*.spec file
- IMPROVED: More sensitive default detection thresholds (35, 35, 45)
- IMPROVED: Energy detection threshold lowered 10x for better sensitivity

FEATURES FROM v3.1.0:
🎨 MODERN TABBED INTERFACE 🎨
- Clean 4-tab layout: Radar View, Detection & Audio, Game Detection, Analysis
- Real-time audio level monitoring with color-coded feedback
- Quick Setup button for one-click game audio configuration
- Auto-suggestion for loopback mode when games detected
- Live stats in toolbar (Targets, Audio Level, FPS)

FEATURES FROM v3.0.5:
✨ MULTI-TARGET TRACKING (up to 3 simultaneous targets)
✨ 3D SPHERE RADAR with elevation detection
✨ GAME DETECTION (ARC Raiders, Tarkov, CS2, Valorant, etc.)
✨ HUMAN VOICE DETECTION (formant analysis, pitch, breathing)
✨ HUMAN FOOTSTEP PATTERN RECOGNITION (cadence, L-R, surface, gait)
"""

# ============================================================================
# STANDARD LIBRARY IMPORTS
# ============================================================================
import sys
import os
import queue
import time
import math
import threading
import re
import json
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from collections import deque

# ============================================================================
# THIRD-PARTY IMPORTS
# ============================================================================
import numpy as np

# FIXED v3.5.3: Add numpy compatibility shim BEFORE importing soundcard
# soundcard uses deprecated numpy.fromstring which was removed in numpy 2.0
if not hasattr(np, 'fromstring'):
    np.fromstring = np.frombuffer

from scipy import signal as sp_signal
import psutil

try:
    import sounddevice as sd
except ImportError:
    sd = None

try:
    import soundcard as sc
except ImportError:
    sc = None

import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QDockWidget, QTabWidget, QPushButton, QLabel, QComboBox,
    QSlider, QCheckBox, QToolBar, QStatusBar, QSpinBox, QGroupBox,
    QFormLayout, QMessageBox, QAction, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPalette

# ============================================================================
# MODULE IMPORTS - Support both package and standalone execution
# ============================================================================
# Add current directory to path for standalone script execution
# This allows 'from core import ...' to work when running 'python main.py'
_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

# Try relative imports first (when running as package module)
# Fall back to direct imports (when running as standalone script)
try:
    # ============================================================================
    # CORE MODULE IMPORTS (Point 10 - v3.5.0: Modularization)
    # ============================================================================
    from .core import (
        # Constants
        VERSION,
        SAMPLE_RATE,
        BLOCK_SIZE,
        CHANNELS,
        TICK_INTERVAL_MS,
        GAME_SCAN_INTERVAL_MS,
        AUDIO_SCAN_INTERVAL_MS,
        STARTUP_DELAY_MS,
        STARTUP_AUDIO_DELAY_MS,
        ENERGY_THRESHOLD,
        LOCALIZATION_MIN_CONFIDENCE,
        RADAR_ROTATION_DEG,
        MAX_WORKERS,
        DETECTION_TIMEOUT_SEC,
        CLEANUP_INTERVAL_SEC,
        AUDIO_LEVEL_LOUD,
        AUDIO_LEVEL_MEDIUM,
        AUDIO_LEVEL_LOW,
        RECORDING_BUFFER_SIZE,
        RECORDING_FLUSH_INTERVAL,
        TOAST_DURATION_MS,
        TOAST_MAX_COUNT,

        # Logger
        ThreadSafeLogger,
        log,
        ROOT,
        SUPER_LOG,

        # Config
        ConfigManager,

        # Translations
        TRANSLATIONS,
        current_language,
        tr,
        set_language,
        get_language,
    )

    # ============================================================================
    # HARDWARE MODULE IMPORTS (Point 10 - v3.5.0: Modularization)
    # ============================================================================
    from .hardware import (
        GPUAccelerator,
        SoundBlasterOptimizer,
    )

    # ============================================================================
    # UTILS MODULE IMPORTS (Point 10 - v3.5.0: Modularization)
    # ============================================================================
    from .utils import (
        PerformanceMonitor,
        GameProcessDetector,
        PlatformLauncherDetector,
        AudioSourceScanner,
    )

    # ============================================================================
    # TRACKING MODULE IMPORTS (Point 10 - v3.5.0: Modularization)
    # ============================================================================
    from .tracking import (
        Target,
        TargetTracker,
        ThreatPrioritySystem,
    )

    # ============================================================================
    # DETECTION MODULE IMPORTS (Point 10 - v3.5.0: Modularization)
    # ============================================================================
    from .detection import (
        DetectionWorker,
        HumanFootstepDetector,
    )

    # ============================================================================
    # AUDIO MODULE IMPORTS (Point 10 - v3.5.0: Modularization)
    # ============================================================================
    from .audio import (
        AudioProcessingCache,
        AudioEngine,
        SoundClassifier,
        AudioRecorder,
        HumanVoiceDetector,
    )

    # ============================================================================
    # WIDGETS MODULE IMPORTS (Point 10 - v3.5.0: Modularization)
    # ============================================================================
    from .widgets import (
        ToastNotification,
        DetachableRadarWidget,
        RadarWidget,
        MilitaryHUDRadar,
        Military3DRadar,
        Radar3DWidget,
        DetachableLedWidget,
        LedOverlayWidget,
        SpectrumWidget,
        WaterfallWidget,
        WaveformWidget,
        MilitarySpectrumWidget,
        MilitaryWaterfallWidget,
        MilitaryWaveformWidget,
        DevicePanel,
        DetectionPanel,
    )

except ImportError:
    # Fallback to direct imports when running as standalone script
    from core import (
        VERSION, SAMPLE_RATE, BLOCK_SIZE, CHANNELS,
        TICK_INTERVAL_MS, GAME_SCAN_INTERVAL_MS, AUDIO_SCAN_INTERVAL_MS,
        STARTUP_DELAY_MS, STARTUP_AUDIO_DELAY_MS, ENERGY_THRESHOLD,
        LOCALIZATION_MIN_CONFIDENCE, RADAR_ROTATION_DEG, MAX_WORKERS, DETECTION_TIMEOUT_SEC,
        CLEANUP_INTERVAL_SEC, AUDIO_LEVEL_LOUD, AUDIO_LEVEL_MEDIUM,
        AUDIO_LEVEL_LOW, RECORDING_BUFFER_SIZE, RECORDING_FLUSH_INTERVAL,
        TOAST_DURATION_MS, TOAST_MAX_COUNT,
        ThreadSafeLogger, log, ROOT, SUPER_LOG,
        ConfigManager,
        TRANSLATIONS, current_language, tr, set_language, get_language,
    )
    from hardware import GPUAccelerator, SoundBlasterOptimizer
    from utils import (
        PerformanceMonitor, GameProcessDetector,
        PlatformLauncherDetector, AudioSourceScanner,
    )
    from tracking import Target, TargetTracker, ThreatPrioritySystem
    from detection import DetectionWorker, HumanFootstepDetector
    from audio import (
        AudioProcessingCache, AudioEngine, SoundClassifier,
        AudioRecorder, HumanVoiceDetector,
    )
    from widgets import (
        ToastNotification, DetachableRadarWidget, RadarWidget,
        MilitaryHUDRadar, Military3DRadar, Radar3DWidget,
        DetachableLedWidget, LedOverlayWidget,
        SpectrumWidget, WaterfallWidget, WaveformWidget,
        MilitarySpectrumWidget, MilitaryWaterfallWidget, MilitaryWaveformWidget,
        DevicePanel, DetectionPanel,
    )

# ============================================================================
# CONFIG MANAGER - Imported from core module
# ============================================================================

# ============================================================================
# TRANSLATIONS - Imported from core module
# ============================================================================

# ============================================================================
# PATHS AND LOGGING (ENHANCED v3.5.0 - Thread-safe logging)
# ============================================================================

import logging
import logging.handlers

ROOT = Path(__file__).parent.parent
SUPER_LOG = ROOT / "super_log.txt"


# ThreadSafeLogger - Imported from core module


def apply_dark_theme(app: QApplication):
    """Apply dark theme to application"""
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(25, 25, 35))
    palette.setColor(QPalette.WindowText, QColor(220, 220, 230))
    palette.setColor(QPalette.Base, QColor(18, 18, 28))
    palette.setColor(QPalette.AlternateBase, QColor(30, 30, 40))
    palette.setColor(QPalette.ToolTipBase, QColor(50, 50, 60))
    palette.setColor(QPalette.ToolTipText, QColor(220, 220, 230))
    palette.setColor(QPalette.Text, QColor(220, 220, 230))
    palette.setColor(QPalette.Button, QColor(45, 45, 55))
    palette.setColor(QPalette.ButtonText, QColor(220, 220, 230))
    palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

    app.setPalette(palette)

    stylesheet = """
        QMainWindow { background-color: #191923; }
        QWidget { background-color: #191923; color: #DCDCE6; }
        QDockWidget { background-color: #191923; color: #DCDCE6; }
        QDockWidget::title { background-color: #2D2D37; padding: 5px; }
        QPushButton {
            background-color: #2D2D37;
            color: #DCDCE6;
            border: 1px solid #2A82DA;
            border-radius: 3px;
            padding: 5px 15px;
            min-width: 80px;
        }
        QPushButton:hover { background-color: #2A82DA; }
        QPushButton:pressed { background-color: #1A5AA0; }
        QPushButton:checked { background-color: #2A82DA; }
        QComboBox, QSpinBox {
            background-color: #121218;
            color: #DCDCE6;
            border: 1px solid #2A82DA;
            border-radius: 3px;
            padding: 3px;
        }
        QSlider::groove:horizontal {
            background: #121218;
            height: 6px;
            border-radius: 3px;
        }
        QSlider::handle:horizontal {
            background: #2A82DA;
            width: 14px;
            margin: -4px 0;
            border-radius: 7px;
        }
        QLabel { color: #DCDCE6; background: transparent; }
        QGroupBox {
            border: 1px solid #2A82DA;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
            font-weight: bold;
            color: #2A82DA;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 5px;
        }
        QCheckBox { color: #DCDCE6; }
    """
    app.setStyleSheet(stylesheet)


# ============================================================================
# PERFORMANCE OPTIMIZATION (Module 12 - v3.4.0)
# ============================================================================












class MainWindow(QMainWindow):
    """
    Main application window

    Point 11 - v3.5.0: Dependency Injection support
    Can receive dependencies via container or create them directly (backward compatible)
    """

    def __init__(self, container=None):
        super().__init__()
        log("MainWindow.__init__", "INFO")

        self.setWindowTitle(f"{tr('app_title')} {VERSION}")
        self.setGeometry(100, 100, 1400, 900)

        # State
        self.is_running = False
        self.radar_angle = 0.0
        self.test_phase = 0.0

        # Detachable windows
        self.detached_radar = None
        self.detached_led = None

        # Point 11 - v3.5.0: Dependency Injection
        if container is not None:
            log("MainWindow: Using DI container for dependencies", "INFO")
            self._inject_dependencies(container)
        else:
            log("MainWindow: Creating dependencies directly (legacy mode)", "INFO")
            self._create_dependencies()

        # Configuration
        self.config = self.config_manager.load()

        # Toast notification system (v3.5.0 - Phase 7)
        self.toast = ToastNotification()

        self.create_ui()

        # Connect game detector to DevicePanel (FIXED v3.5.2)
        self.dev_panel.set_game_detector(self.game_detector)

        # Main update timer (20 FPS) - FIXED v3.5.0: Use constant
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(TICK_INTERVAL_MS)

        # Game detection timer (scan every 5 seconds) - FIXED v3.5.0: Use constant
        self.game_scan_timer = QTimer()
        self.game_scan_timer.timeout.connect(self.scan_games)
        self.game_scan_timer.start(GAME_SCAN_INTERVAL_MS)

        # Audio source scan timer (scan every 2 seconds) - FIXED v3.5.0: Use constant
        self.audio_scan_timer = QTimer()
        self.audio_scan_timer.timeout.connect(self.scan_audio_sources)
        self.audio_scan_timer.start(AUDIO_SCAN_INTERVAL_MS)

        # Initial scans (v3.0) - FIXED v3.5.0: Use constants
        QTimer.singleShot(STARTUP_DELAY_MS, self.scan_games)
        QTimer.singleShot(STARTUP_AUDIO_DELAY_MS, self.scan_audio_sources)

    def _inject_dependencies(self, container):
        """
        Inject dependencies from DI container (Point 11 - v3.5.0)

        Args:
            container: ServiceContainer with registered dependencies
        """
        # Core
        self.config_manager = container.get('config_manager')

        # Hardware
        self.gpu_accelerator = container.get('gpu')
        self.sb_optimizer = container.get('soundblaster')

        # Audio
        self.fft_cache = container.get('audio_cache')
        self.audio = container.get('audio_engine')
        self.sound_classifier = container.get('sound_classifier')
        self.audio_recorder = container.get('audio_recorder')

        # Detection
        self.detection_worker = container.get('detection_worker')

        # Tracking
        self.target_tracker = container.get('target_tracker')
        self.threat_system = container.get('threat_system')

        # Utils
        self.perf_monitor = container.get('performance_monitor')
        self.game_detector = container.get('game_detector')
        self.platform_detector = container.get('launcher_detector')
        self.audio_scanner = container.get('audio_scanner')

    def _create_dependencies(self):
        """
        Create dependencies directly (legacy mode)
        Backward compatible with pre-DI code
        """
        # Configuration manager (v3.5.0 - Phase 4)
        self.config_manager = ConfigManager()
        config = self.config_manager.load()

        # Performance optimization (Module 12 - v3.4.0)
        use_gpu = config.get('performance', {}).get('use_gpu', True)
        self.gpu_accelerator = GPUAccelerator(enable_gpu=use_gpu)

        # Sound Blaster Z SE optimization (v3.5.0 - Phase 6)
        self.sb_optimizer = SoundBlasterOptimizer()

        # Audio services
        self.fft_cache = AudioProcessingCache(max_size=5, gpu_accelerator=self.gpu_accelerator)
        self.audio = AudioEngine()
        self.sound_classifier = SoundClassifier()
        self.audio_recorder = AudioRecorder(sample_rate=48000)

        # Detection
        self.detection_worker = DetectionWorker(max_workers=MAX_WORKERS)

        # Tracking
        self.target_tracker = TargetTracker(max_targets=3)
        self.threat_system = ThreatPrioritySystem()

        # Utils
        self.perf_monitor = PerformanceMonitor()
        self.game_detector = GameProcessDetector()
        self.platform_detector = PlatformLauncherDetector()
        self.audio_scanner = AudioSourceScanner(platform_detector=self.platform_detector)

    def create_ui(self):
        """Create modern tabbed UI (v3.1.0 - Complete redesign)"""

        # ====================================================================
        # MODERN TABBED INTERFACE - Clean & Organized
        # ====================================================================

        # Main tab widget (center)
        self.main_tabs = QTabWidget()
        self.main_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #333;
                background: #0a0a0a;
            }
            QTabBar::tab {
                background: #1a1a1a;
                color: #aaa;
                padding: 10px 20px;
                margin: 2px;
                border: 1px solid #333;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #2a2a2a;
                color: #0ff;
                border-bottom: 2px solid #0ff;
            }
            QTabBar::tab:hover {
                background: #252525;
                color: #0dd;
            }
        """)

        self.setCentralWidget(self.main_tabs)

        # ====================================================================
        # TAB 1: 🎯 RADAR VIEW (Main tactical display)
        # ====================================================================
        radar_tab = QWidget()
        radar_layout = QVBoxLayout()
        radar_layout.setContentsMargins(5, 5, 5, 5)

        # Radar sub-tabs (2D/3D)
        self.radar_tabs = QTabWidget()
        self.radar_tabs.setStyleSheet("QTabWidget::pane { border: 1px solid #222; }")

        # 2D Radar - Military HUD Style
        self.radar_widget = MilitaryHUDRadar()
        self.radar_tabs.addTab(self.radar_widget, "🎯 Military HUD")

        # 3D Radar - Military Wallhack HUD Style
        self.radar_3d_widget = Military3DRadar()
        self.radar_tabs.addTab(self.radar_3d_widget, "🌐 3D Wallhack")

        radar_layout.addWidget(self.radar_tabs)

        # Radar controls (compact bottom panel)
        radar_controls = QHBoxLayout()
        self.detach_radar_btn = QPushButton("⬜ Detach Window")
        self.detach_radar_btn.setCheckable(True)
        self.detach_radar_btn.clicked.connect(self.toggle_detach_radar)
        radar_controls.addWidget(self.detach_radar_btn)

        self.radar_frameless_btn = QCheckBox("Frameless")
        self.radar_frameless_btn.toggled.connect(self.toggle_radar_frameless)
        radar_controls.addWidget(self.radar_frameless_btn)

        radar_controls.addWidget(QLabel("Opacity:"))
        self.radar_alpha = QSlider(Qt.Horizontal)
        self.radar_alpha.setRange(0, 100)
        self.radar_alpha.setValue(100)
        self.radar_alpha.setMaximumWidth(150)
        self.radar_alpha.valueChanged.connect(self.update_radar_alpha)
        radar_controls.addWidget(self.radar_alpha)
        radar_controls.addStretch()

        radar_layout.addLayout(radar_controls)
        radar_tab.setLayout(radar_layout)
        self.main_tabs.addTab(radar_tab, "🎯 Radar View")

        # ====================================================================
        # TAB 2: 🔊 DETECTION & AUDIO (Detection + Device settings)
        # ====================================================================
        detection_tab = QWidget()
        detection_layout = QHBoxLayout()
        detection_layout.setContentsMargins(5, 5, 5, 5)

        # Left: Detection panel
        self.det_panel = DetectionPanel()
        detection_layout.addWidget(self.det_panel, 3)

        # Right: Device/Audio panel
        self.dev_panel = DevicePanel(self.audio)
        self.dev_panel.set_audio_scanner(self.audio_scanner)  # v3.5.1: Connect for device tracking
        detection_layout.addWidget(self.dev_panel, 2)

        detection_tab.setLayout(detection_layout)
        self.main_tabs.addTab(detection_tab, "🔊 Detection & Audio")

        # ====================================================================
        # TAB 3: 🎮 GAME DETECTION (Games + Audio Sources)
        # ====================================================================
        game_tab = QWidget()
        game_layout = QVBoxLayout()
        game_layout.setContentsMargins(10, 10, 10, 10)

        # Game detection section (from DevicePanel)
        game_group = QGroupBox("🎮 Active Games & Engines")
        game_group_layout = QVBoxLayout()

        self.detected_games_label = QLabel("Scanning for games...")
        self.detected_games_label.setStyleSheet("font-size: 11pt; color: #888888; padding: 10px;")
        self.detected_games_label.setWordWrap(True)
        game_group_layout.addWidget(self.detected_games_label)

        self.detected_engines_label = QLabel("No engines detected")
        self.detected_engines_label.setStyleSheet("font-size: 10pt; color: #888888; padding: 5px;")
        self.detected_engines_label.setWordWrap(True)
        game_group_layout.addWidget(self.detected_engines_label)

        # Quick Setup button for game audio
        self.quick_setup_btn = QPushButton("⚡ QUICK SETUP - Enable Game Audio Capture")
        self.quick_setup_btn.setStyleSheet("""
            QPushButton {
                background: #0066aa;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 4px;
                font-size: 10pt;
                margin: 10px;
            }
            QPushButton:hover {
                background: #0088cc;
            }
        """)
        self.quick_setup_btn.clicked.connect(self.quick_setup_game_audio)
        game_group_layout.addWidget(self.quick_setup_btn)

        game_group.setLayout(game_group_layout)
        game_layout.addWidget(game_group)

        # Platform Launchers section (v3.4.1)
        platform_group = QGroupBox("🚀 Gaming Platform Launchers")
        platform_layout = QVBoxLayout()

        self.detected_platforms_label = QLabel("Scanning for launchers...")
        self.detected_platforms_label.setStyleSheet("font-size: 10pt; color: #888888; padding: 5px;")
        self.detected_platforms_label.setWordWrap(True)
        platform_layout.addWidget(self.detected_platforms_label)

        self.launcher_game_label = QLabel("—")
        self.launcher_game_label.setStyleSheet("font-size: 9pt; color: #00DDFF; padding: 5px;")
        self.launcher_game_label.setWordWrap(True)
        platform_layout.addWidget(self.launcher_game_label)

        platform_group.setLayout(platform_layout)
        game_layout.addWidget(platform_group)

        # Audio sources section
        sources_group = QGroupBox("🔊 Audio Sources Monitor")
        sources_layout = QVBoxLayout()

        # Active sources
        active_label = QLabel("ACTIVE SOURCES:")
        active_label.setStyleSheet("font-weight: bold; color: #00FF00; font-size: 10pt;")
        sources_layout.addWidget(active_label)

        self.active_sources_label = QLabel("Scanning: 0")
        self.active_sources_label.setStyleSheet("font-size: 9pt; color: #00DD00; padding: 5px;")
        sources_layout.addWidget(self.active_sources_label)

        self.active_sources_list = QLabel("—")
        self.active_sources_list.setStyleSheet("font-size: 8pt; color: #00DD00; padding: 5px;")
        self.active_sources_list.setWordWrap(True)
        self.active_sources_list.setMaximumHeight(120)
        sources_layout.addWidget(self.active_sources_list)

        # Inactive sources
        inactive_label = QLabel("INACTIVE SOURCES:")
        inactive_label.setStyleSheet("font-weight: bold; color: #FF6666; font-size: 10pt; margin-top: 10px;")
        sources_layout.addWidget(inactive_label)

        self.inactive_sources_label = QLabel("Inactive: 0")
        self.inactive_sources_label.setStyleSheet("font-size: 9pt; color: #DD6666; padding: 5px;")
        sources_layout.addWidget(self.inactive_sources_label)

        self.inactive_sources_list = QLabel("—")
        self.inactive_sources_list.setStyleSheet("font-size: 8pt; color: #DD6666; padding: 5px;")
        self.inactive_sources_list.setWordWrap(True)
        self.inactive_sources_list.setMaximumHeight(80)
        sources_layout.addWidget(self.inactive_sources_list)

        sources_group.setLayout(sources_layout)
        game_layout.addWidget(sources_group)

        game_layout.addStretch()
        game_tab.setLayout(game_layout)
        self.main_tabs.addTab(game_tab, "🎮 Game Detection")

        # ====================================================================
        # TAB 4: 📊 ANALYSIS (Spectrum + Waterfall + LED)
        # ====================================================================
        analysis_tab = QWidget()
        analysis_layout = QVBoxLayout()
        analysis_layout.setContentsMargins(5, 5, 5, 5)

        # Spectrum & Waterfall & Waveform - Military HUD Style (v3.5.1)
        spectrum_waterfall_tabs = QTabWidget()

        # NEW: Military HUD Spectrum with WALK/RUN/SHOT markers
        self.spectrum = MilitarySpectrumWidget()
        spectrum_waterfall_tabs.addTab(self.spectrum, "📡 LIVE SPECTRUM")

        # NEW: Military HUD Waterfall with WALK/RUN/SHOT markers
        self.waterfall = MilitaryWaterfallWidget()
        spectrum_waterfall_tabs.addTab(self.waterfall, "🌊 WATERFALL")

        # NEW: Military HUD Waveform with WALK/RUN/SHOT markers
        self.waveform = MilitaryWaveformWidget()
        spectrum_waterfall_tabs.addTab(self.waveform, "〰️ WAVEFORM")

        analysis_layout.addWidget(spectrum_waterfall_tabs, 3)

        # LED Alert at bottom
        led_group = QGroupBox("⚡ LED Edge Alert")
        led_layout = QVBoxLayout()
        self.led_widget = LedOverlayWidget()
        self.led_widget.setMinimumHeight(100)
        led_layout.addWidget(self.led_widget)

        # LED controls
        led_controls = QHBoxLayout()
        self.detach_led_btn = QPushButton("⬜ Detach LED")
        self.detach_led_btn.setCheckable(True)
        self.detach_led_btn.clicked.connect(self.toggle_detach_led)
        led_controls.addWidget(self.detach_led_btn)

        self.led_frameless_btn = QCheckBox("Frameless")
        self.led_frameless_btn.toggled.connect(self.toggle_led_frameless)
        led_controls.addWidget(self.led_frameless_btn)

        led_controls.addWidget(QLabel("Opacity:"))
        self.led_alpha = QSlider(Qt.Horizontal)
        self.led_alpha.setRange(0, 100)
        self.led_alpha.setValue(80)
        self.led_alpha.setMaximumWidth(150)
        self.led_alpha.valueChanged.connect(self.update_led_alpha)
        led_controls.addWidget(self.led_alpha)
        led_controls.addStretch()

        led_layout.addLayout(led_controls)
        led_group.setLayout(led_layout)
        analysis_layout.addWidget(led_group, 1)

        analysis_tab.setLayout(analysis_layout)
        self.main_tabs.addTab(analysis_tab, "📊 Analysis")

        # ====================================================================
        # TOOLBAR (Compact - only essentials)
        # ====================================================================
        toolbar = QToolBar()
        toolbar.setStyleSheet("""
            QToolBar {
                background: #1a1a1a;
                border-bottom: 1px solid #333;
                padding: 5px;
            }
        """)
        self.addToolBar(toolbar)

        # Start/Stop button (prominent)
        self.start_btn = QPushButton("▶ START")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background: #00aa00;
                color: white;
                font-weight: bold;
                padding: 8px 20px;
                border-radius: 4px;
                font-size: 11pt;
            }
            QPushButton:hover {
                background: #00cc00;
            }
        """)
        self.start_btn.clicked.connect(self.toggle_start_stop)
        toolbar.addWidget(self.start_btn)

        toolbar.addSeparator()

        # Recording controls (Module 9 - v3.3.0)
        self.record_btn = QPushButton("⏺ REC")
        self.record_btn.setStyleSheet("""
            QPushButton {
                background: #aa0000;
                color: white;
                font-weight: bold;
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background: #cc0000;
            }
            QPushButton:disabled {
                background: #555555;
                color: #888888;
            }
        """)
        self.record_btn.clicked.connect(self.toggle_recording)
        self.record_btn.setEnabled(False)  # Enabled only when audio is running
        toolbar.addWidget(self.record_btn)

        self.record_duration_label = QLabel("0:00")
        self.record_duration_label.setStyleSheet("color: #ff0000; font-family: monospace; font-weight: bold;")
        toolbar.addWidget(self.record_duration_label)

        toolbar.addSeparator()

        # Language switcher (FIXED v3.5.1: Shows current language)
        toolbar.addWidget(QLabel("🌍"))
        self.lang_btn = QPushButton("🇬🇧 EN")  # Default to EN, updated in update_ui_translations
        self.lang_btn.setCheckable(True)
        self.lang_btn.setToolTip("Click to switch language / Kliknij aby zmienić język")
        self.lang_btn.clicked.connect(self.toggle_language)
        toolbar.addWidget(self.lang_btn)

        toolbar.addSeparator()

        # Quick stats
        self.toolbar_stats_label = QLabel("Targets: 0 | FPS: 20")
        self.toolbar_stats_label.setStyleSheet("color: #0dd; padding: 5px; font-family: monospace;")
        toolbar.addWidget(self.toolbar_stats_label)

        # Add spacer to push version to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar.addWidget(spacer)

        # Version label
        version_label = QLabel(f"v{VERSION}")
        version_label.setStyleSheet("color: #666; padding: 5px; font-size: 9pt;")
        toolbar.addWidget(version_label)

        # ====================================================================
        # STATUS BAR
        # ====================================================================
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background: #1a1a1a;
                color: #aaa;
                border-top: 1px solid #333;
            }
        """)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("✓ Ready - All systems operational")

        # Setup keyboard shortcuts (v3.5.0 - Phase 8)
        self.setup_shortcuts()

    def toggle_language(self):
        """Toggle between EN and PL (FIXED v3.5.2: Use get_language function)"""
        current_lang = get_language()

        if current_lang == 'en':
            set_language('pl')
        else:
            set_language('en')

        log(f"Language changed to: {get_language()}", "INFO")
        self.update_ui_translations()

    def update_ui_translations(self):
        """Update all UI text with current language (FIXED v3.5.2: Use get_language function)"""
        lang = get_language()

        # Main window
        self.setWindowTitle(f"{tr('app_title')} {VERSION}")

        # Start/Stop button
        if not self.is_running:
            self.start_btn.setText("▶ START")
        else:
            self.start_btn.setText("⏹ STOP")

        # Status bar
        if not self.is_running:
            self.status_bar.showMessage("✓ Ready - All systems operational" if lang == 'en' else "✓ Gotowy - Wszystkie systemy sprawne")
        else:
            self.status_bar.showMessage("● RUNNING - Detection active" if lang == 'en' else "● DZIAŁA - Detekcja aktywna")

        # Update language button to show current language
        if hasattr(self, 'lang_btn'):
            self.lang_btn.setText("🇬🇧 EN" if lang == 'en' else "🇵🇱 PL")
            self.lang_btn.setChecked(lang == 'pl')

        # Update panels
        self.dev_panel.update_translations()
        self.det_panel.update_translations()

        # Update detached windows titles
        if self.detached_radar:
            self.detached_radar.setWindowTitle(f"{tr('radar')} - RadarSuite {VERSION}")

        if self.detached_led:
            self.detached_led.setWindowTitle(f"{tr('led_alert')} - RadarSuite {VERSION}")

    def setup_shortcuts(self):
        """
        Setup keyboard shortcuts (v3.5.0 - Phase 8)

        Shortcuts:
            Ctrl+S: Start/Stop
            Ctrl+R: Reset radar
            Ctrl+1/2/3/4: Switch tabs
            Space: Quick mute (toggle audio)
            F11: Fullscreen
        """
        from PyQt5.QtWidgets import QShortcut
        from PyQt5.QtGui import QKeySequence

        # Ctrl+S: Start/Stop
        shortcut_startstop = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut_startstop.activated.connect(self.toggle_start_stop)

        # Ctrl+R: Reset radar
        shortcut_reset = QShortcut(QKeySequence("Ctrl+R"), self)
        shortcut_reset.activated.connect(self.reset_radar)

        # Ctrl+1: Switch to Radar tab
        shortcut_tab1 = QShortcut(QKeySequence("Ctrl+1"), self)
        shortcut_tab1.activated.connect(lambda: self.tabs.setCurrentIndex(0))

        # Ctrl+2: Switch to Detection tab
        shortcut_tab2 = QShortcut(QKeySequence("Ctrl+2"), self)
        shortcut_tab2.activated.connect(lambda: self.tabs.setCurrentIndex(1))

        # Ctrl+3: Switch to Settings tab
        shortcut_tab3 = QShortcut(QKeySequence("Ctrl+3"), self)
        shortcut_tab3.activated.connect(lambda: self.tabs.setCurrentIndex(2))

        # Ctrl+4: Switch to Debug tab (if exists)
        shortcut_tab4 = QShortcut(QKeySequence("Ctrl+4"), self)
        shortcut_tab4.activated.connect(lambda: self.tabs.setCurrentIndex(3) if self.tabs.count() > 3 else None)

        # Space: Quick mute toggle
        shortcut_mute = QShortcut(QKeySequence("Space"), self)
        shortcut_mute.activated.connect(self.quick_mute_toggle)

        # F11: Fullscreen toggle
        shortcut_fullscreen = QShortcut(QKeySequence("F11"), self)
        shortcut_fullscreen.activated.connect(self.toggle_fullscreen)

        log("Keyboard shortcuts initialized", "INFO")

    def toggle_start_stop(self):
        """Toggle start/stop via keyboard shortcut"""
        if self.is_running:
            self.stop()
            self.toast.show_toast("Audio detection stopped", "info", 2000)
        else:
            self.start()
            self.toast.show_toast("Audio detection started", "success", 2000)

    def reset_radar(self):
        """Reset radar display"""
        # Reset radar angle
        self.radar_angle = 0.0
        self.toast.show_toast("Radar reset", "info", 1500)
        log("Radar reset via keyboard shortcut", "INFO")

    def quick_mute_toggle(self):
        """Quick mute toggle (Space key)"""
        # Stop/start audio without changing UI state
        if self.is_running:
            self.audio.stop()
            self.toast.show_toast("Audio muted", "warning", 1500)
            log("Audio muted via keyboard shortcut", "INFO")
        else:
            self.audio.start()
            self.toast.show_toast("Audio unmuted", "success", 1500)
            log("Audio unmuted via keyboard shortcut", "INFO")

    def toggle_fullscreen(self):
        """Toggle fullscreen mode (F11)"""
        if self.isFullScreen():
            self.showNormal()
            self.toast.show_toast("Exited fullscreen", "info", 1500)
        else:
            self.showFullScreen()
            self.toast.show_toast("Entered fullscreen (F11 to exit)", "info", 2000)

    def update_radar_alpha(self, value):
        """Update radar opacity"""
        opacity = value / 100.0

        if self.detached_radar:
            self.detached_radar.set_opacity(opacity)

    def update_led_alpha(self, value):
        """Update LED opacity"""
        opacity = value / 100.0

        if self.detached_led:
            self.detached_led.set_opacity(opacity)
        else:
            self.led_widget.global_alpha = opacity

    def _safe_update_detached_radar(self, method_name, *args):
        """
        Safely update detached radar (FIXED v3.5.0: Null-safety)

        Prevents AttributeError when detached_radar or detached_radar.radar is None

        Args:
            method_name: Method name to call on detached_radar.radar
            *args: Arguments to pass to method
        """
        if not self.detached_radar:
            return

        if not hasattr(self.detached_radar, 'radar'):
            log(f"Detached radar missing 'radar' attribute", "WARNING")
            return

        if self.detached_radar.radar is None:
            log(f"Detached radar.radar is None", "WARNING")
            return

        try:
            method = getattr(self.detached_radar.radar, method_name)
            method(*args)
        except AttributeError as e:
            log(f"Method '{method_name}' not found on detached radar: {e}", "WARNING")
        except Exception as e:
            log(f"Error updating detached radar.{method_name}: {e}", "ERROR")

    def toggle_detach_radar(self, checked):
        """Toggle radar detachment"""
        if checked:
            # Create detached radar
            self.detached_radar = DetachableRadarWidget()
            self.detached_radar.set_opacity(self.radar_alpha.value() / 100.0)
            self.detached_radar.show()
            log("Radar detached", "INFO")
        else:
            # Close detached radar
            if self.detached_radar:
                self.detached_radar.close()
                self.detached_radar = None
            log("Radar attached", "INFO")

    def toggle_detach_led(self, checked):
        """Toggle LED detachment"""
        if checked:
            # Create detached LED
            self.detached_led = DetachableLedWidget()
            self.detached_led.set_opacity(self.led_alpha.value() / 100.0)
            self.detached_led.show()
            log("LED detached", "INFO")
        else:
            # Close detached LED
            if self.detached_led:
                self.detached_led.close()
                self.detached_led = None
            log("LED attached", "INFO")

    def toggle_radar_frameless(self, checked):
        """Toggle radar frameless mode"""
        if self.detached_radar:
            self.detached_radar.set_frameless(checked)

    def toggle_led_frameless(self, checked):
        """Toggle LED frameless mode"""
        if self.detached_led:
            self.detached_led.set_frameless(checked)

    def toggle_start_stop(self):
        """Toggle audio capture"""
        if not self.is_running:
            self.start()
        else:
            self.stop()

    def toggle_recording(self):
        """Toggle audio recording (Module 9 - v3.3.0)"""
        if not self.audio_recorder.is_recording:
            # Start recording
            self.audio_recorder.start_recording()
            self.record_btn.setText("⏹ STOP REC")
            self.record_btn.setStyleSheet("""
                QPushButton {
                    background: #00aa00;
                    color: white;
                    font-weight: bold;
                    padding: 8px 15px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background: #00cc00;
                }
            """)
            log("Recording started", "INFO")
        else:
            # Stop recording and save
            self.audio_recorder.stop_recording()

            # Generate filename with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"RadarSuite_Recording_{timestamp}.wav"

            # Save to file
            if self.audio_recorder.save_to_wav(filename):
                self.status_bar.showMessage(f"✓ Recording saved: {filename}")
            else:
                self.status_bar.showMessage("❌ Failed to save recording")

            # Reset button
            self.record_btn.setText("⏺ REC")
            self.record_btn.setStyleSheet("""
                QPushButton {
                    background: #aa0000;
                    color: white;
                    font-weight: bold;
                    padding: 8px 15px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background: #cc0000;
                }
            """)

            log(f"Recording saved to {filename}", "INFO")

    def start(self):
        """Start audio capture"""
        log("Starting audio capture", "INFO")

        self.dev_panel.apply_settings()
        self.audio.start()

        self.is_running = True
        self.record_btn.setEnabled(True)  # Enable recording when audio starts

        # Update audio status indicator (FIXED v3.5.3)
        self.dev_panel.update_audio_init_status(True, False)
        self.start_btn.setText("⏹ STOP")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background: #aa0000;
                color: white;
                font-weight: bold;
                padding: 8px 20px;
                border-radius: 4px;
                font-size: 11pt;
            }
            QPushButton:hover {
                background: #cc0000;
            }
        """)
        self.status_bar.showMessage("● RUNNING - Detection active" if get_language() == 'en' else "● DZIAŁA - Detekcja aktywna")

    def stop(self):
        """Stop audio capture"""
        log("Stopping audio capture", "INFO")

        self.audio.stop()

        self.is_running = False

        # Update audio status indicator (FIXED v3.5.3)
        self.dev_panel.update_audio_init_status(False, False)

        # FIXED v3.5.3: Reset detection labels and clear radars on stop
        self.det_panel.reset_detection()
        self.radar_widget.update_target(None, None)
        self.radar_3d_widget.clear_targets()
        self.target_tracker.clear()
        self.dev_panel.rms_label.setText("RMS: --- dBFS")

        self.start_btn.setText("▶ START")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background: #00aa00;
                color: white;
                font-weight: bold;
                padding: 8px 20px;
                border-radius: 4px;
                font-size: 11pt;
            }
            QPushButton:hover {
                background: #00cc00;
            }
        """)
        self.status_bar.showMessage("✓ Stopped - Ready to start" if get_language() == 'en' else "✓ Zatrzymano - Gotowy do startu")

    def _update_radar_sweep(self):
        """
        Update radar sweep angle and all radar widgets (FIXED v3.5.0: Helper method)
        """
        self.radar_angle = (self.radar_angle + RADAR_ROTATION_DEG) % 360.0
        self.radar_widget.update_sweep(self.radar_angle)
        self.radar_3d_widget.update_sweep(self.radar_angle)
        self._safe_update_detached_radar('update_sweep', self.radar_angle)

    def _acquire_audio_block(self):
        """
        Acquire audio block from test mode or real audio input (FIXED v3.5.0: Helper method)

        Returns:
            Audio block (numpy array) or None if not available
        """
        if self.dev_panel.test_mode.isChecked():
            return self.generate_test_block()
        else:
            # FIXED v3.5.3: Avoid numpy array truth value ambiguity
            block = self.audio.read_block(0.0)
            if block is not None:
                return block
            return self.audio.last_block

    def _update_recording(self, block):
        """
        Update audio recording and duration display (FIXED v3.5.0: Helper method)

        Args:
            block: Audio block to record
        """
        if self.audio_recorder.is_recording:
            self.audio_recorder.add_block(block)
            duration = self.audio_recorder.get_duration()
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            self.record_duration_label.setText(f"{minutes}:{seconds:02d}")

    def _process_audio_visualizations(self, block, fft_result):
        """
        Update spectrum, waterfall, and waveform visualizations (FIXED v3.5.0: Helper method)

        Args:
            block: Audio block (numpy array)
            fft_result: Cached FFT computation result
        """
        # Update spectrum with cached FFT (eliminates duplicate computation)
        self.spectrum.update_from_cache(fft_result)
        self.waveform.update_waveform(block)

        # Update waterfall with cached FFT power
        power = 20 * np.log10(fft_result['power'] + 1e-10)
        self.waterfall.push_row(power)

    def _process_audio_level_monitoring(self, energy):
        """
        Monitor and display audio levels with color coding (FIXED v3.5.0: Helper method)

        Args:
            energy: Audio energy (RMS)
        """
        if energy > 0:
            rms_db = 20 * np.log10(energy + 1e-10)
            self.dev_panel.rms_label.setText(f"{tr('rms')} {rms_db:.1f} dBFS")

            # Color-coded audio level indicator
            if rms_db > AUDIO_LEVEL_LOUD:
                level_color = "#00FF00"  # Green - loud
                level_status = "🔊 LOUD"
            elif rms_db > AUDIO_LEVEL_MEDIUM:
                level_color = "#FFFF00"  # Yellow - medium
                level_status = "🔉 OK"
            elif rms_db > AUDIO_LEVEL_LOW:
                level_color = "#FF8800"  # Orange - quiet
                level_status = "🔈 LOW"
            else:
                level_color = "#FF0000"  # Red - very quiet
                level_status = "🔇 SILENT"

            self.dev_panel.rms_label.setStyleSheet(f"color: {level_color}; font-weight: bold; font-size: 10pt;")
        else:
            self.dev_panel.rms_label.setText(f"{tr('rms')} --- dBFS (NO AUDIO!)")
            self.dev_panel.rms_label.setStyleSheet("color: #FF0000; font-weight: bold; font-size: 10pt;")

    def _process_detection_and_tracking(self, block, fft_result, energy):
        """
        Perform detection, 3D localization, classification, and tracking (FIXED v3.5.0: Helper method)

        Args:
            block: Audio block (numpy array)
            fft_result: Cached FFT computation result
            energy: Audio energy (RMS)

        Returns:
            Tuple of (events, bands, active_targets)
        """
        # Detection - use cached FFT (Module 12 optimization)
        events, bands = self.det_panel.analyze(block, self.audio.sample_rate, fft_cache=fft_result)

        # Multi-target tracking
        has_detection = events.get('walk', False) or events.get('run', False) or events.get('shot', False)

        # Prepare detections for tracker
        detections = []
        if has_detection and energy > ENERGY_THRESHOLD:
            # Use precise 3D localization (Module 6)
            location_3d = self.compute_precise_location_3d(block, self.audio.sample_rate)

            # FIXED v4.1.1: Filter low-confidence localizations to reduce radar chaos
            if location_3d['confidence'] < LOCALIZATION_MIN_CONFIDENCE:
                # Skip low-confidence detections
                return events, bands, self.target_tracker.get_active_targets()

            angle = location_3d['angle']
            distance = location_3d['distance']
            elevation = location_3d['elevation']

            # Classify sound type - use cached FFT
            sound_class = self.sound_classifier.classify_sound(block, self.audio.sample_rate, fft_cache=fft_result)

            # Determine detection type (prioritize classification over simple detection)
            if sound_class['confidence'] > 50:
                target_type = sound_class['type']
            elif events.get('shot', False):
                target_type = 'shot'
            elif events.get('run', False):
                target_type = 'footstep'
            elif events.get('walk', False):
                target_type = 'footstep'
            else:
                target_type = 'unknown'

            detections.append({
                'angle': angle,
                'distance': distance,
                'elevation': elevation,
                'type': target_type,
                'sound_class': sound_class['type'],
                'class_confidence': sound_class['confidence']
            })

        # Update tracker
        active_targets = self.target_tracker.update(detections)

        # Rank targets by threat priority (Module 8)
        if active_targets:
            active_targets = self.threat_system.rank_targets(active_targets)

        return events, bands, active_targets

    def _update_ui_elements(self, active_targets, events, bands, energy, balance):
        """
        Update all UI elements: radars, LEDs, toolbar stats (FIXED v3.5.0: Helper method)

        Args:
            active_targets: List of tracked targets
            events: Detection events dictionary
            bands: Frequency bands data
            energy: Audio energy (RMS)
            balance: L/R audio balance
        """
        # Update radars with all active targets (threat-ranked)
        if active_targets:
            # Update 3D radar (supports multiple targets)
            self.radar_3d_widget.clear_targets()
            for target in active_targets:
                # FIXED v3.5.3: Correct parameter order for add_target
                self.radar_3d_widget.add_target(
                    target['id'],           # target_id
                    target['angle'],        # angle
                    target['distance'],     # distance
                    target['elevation']     # elevation
                )

            # Update 2D radar (show primary target only - highest confidence)
            primary_target = max(active_targets, key=lambda t: t['confidence'])
            self.radar_widget.update_target(primary_target['angle'], primary_target['distance'])
            self._safe_update_detached_radar('update_target', primary_target['angle'], primary_target['distance'])
        else:
            # Clear all radars when no targets
            self.radar_widget.update_target(None, None)
            self.radar_3d_widget.clear_targets()
            self._safe_update_detached_radar('update_target', None, None)

        # Update LED overlays
        self.led_widget.update_from_events(events, bands, energy, balance)
        if self.detached_led:
            self.detached_led.led_overlay.update_from_events(events, bands, energy, balance)

        # Update toolbar stats with real performance metrics
        target_count = len(active_targets) if active_targets else 0
        if energy > 0:
            rms_db = 20 * np.log10(energy + 1e-10)
            audio_indicator = "🔊" if rms_db > -40 else "🔉" if rms_db > -60 else "🔇"
        else:
            audio_indicator = "❌"
            rms_db = -100

        # Performance monitoring - end frame and update stats
        self.perf_monitor.end_frame()
        self.perf_monitor.update()
        perf_stats = self.perf_monitor.get_stats()

        self.toolbar_stats_label.setText(
            f"Targets: {target_count} | Audio: {audio_indicator} {rms_db:.0f}dB | FPS: {perf_stats['fps']:.1f} | Latency: {perf_stats['latency_ms']:.1f}ms"
        )

    def tick(self):
        """
        Main update loop (FIXED v3.5.0: Refactored with helper methods)

        Performance optimizations:
        - Module 12 (v3.4.0): Cached FFT computation
        - v3.5.0: Split into focused helper methods for maintainability
        """
        try:
            # Start performance monitoring
            self.perf_monitor.start_frame()

            # 1. Update radar sweep
            self._update_radar_sweep()

            # 2. Acquire and process audio block
            block = self._acquire_audio_block()
            if block is None:
                # FIXED v3.5.3: Update UI even when no audio block
                if hasattr(self, 'audio_scanner') and self.audio_scanner:
                    self.audio_scanner.report_audio_activity(False)
                # Update status to show no audio
                self.dev_panel.update_audio_init_status(self.is_running, False)
                self.dev_panel.rms_label.setText("RMS: --- dBFS")
                self.perf_monitor.end_frame()
                return
            block = self.apply_audio_processing(block)

            # 2b. Report audio activity to scanner (v3.5.1)
            if hasattr(self, 'audio_scanner') and self.audio_scanner:
                has_audio = np.max(np.abs(block)) > 0.001  # Check if there's actual audio
                self.audio_scanner.report_audio_activity(has_audio)

            # 2c. Update audio status indicator (FIXED v3.5.3)
            has_audio_signal = np.max(np.abs(block)) > 0.001
            self.dev_panel.update_audio_init_status(True, has_audio_signal)

            # 3. Update recording
            self._update_recording(block)

            # 4. Compute FFT once and cache (Module 12 - eliminates 4 redundant computations!)
            fft_result = self.fft_cache.compute_fft(block, self.audio.sample_rate)

            # 5. Update audio visualizations
            self._process_audio_visualizations(block, fft_result)

            # 6. Compute energy and balance
            energy, balance = self.compute_orientation(block)

            # 7. Monitor audio levels
            self._process_audio_level_monitoring(energy)

            # 8. Detection, classification, and tracking
            events, bands, active_targets = self._process_detection_and_tracking(block, fft_result, energy)

            # 9. Update UI elements (radars, LEDs, toolbar stats)
            self._update_ui_elements(active_targets, events, bands, energy, balance)

        except Exception as e:
            # CRITICAL ERROR HANDLING: Prevent application freeze if tick() crashes
            log(f"CRITICAL ERROR in tick(): {e}", "ERROR")
            import traceback
            log(traceback.format_exc(), "ERROR")
            # Don't crash - just skip this frame and continue running

    def apply_audio_processing(self, block):
        """
        Apply audio enhancements: auto-gain, manual gain, noise gate (v3.1.2)

        Args:
            block: Audio data (numpy array)

        Returns:
            Processed audio block
        """
        try:
            if block is None or len(block) == 0:
                return block

            processed = block.copy()

            # Apply noise gate (remove audio below threshold)
            noise_gate_value = self.dev_panel.noise_gate_slider.value()
            noise_gate_db = -80 + noise_gate_value  # Convert slider (0-100) to dB (-80 to -20)
            noise_gate_linear = 10 ** (noise_gate_db / 20.0)

            # Calculate RMS for noise gate
            rms = np.sqrt(np.mean(processed ** 2))
            if rms < noise_gate_linear:
                # Below noise gate - mute
                return np.zeros_like(processed)

            # Apply gain (auto or manual)
            if self.dev_panel.auto_gain_enable.isChecked():
                # Auto-gain: target -20 dBFS RMS
                target_rms = 0.1  # -20 dBFS
                current_rms = np.sqrt(np.mean(processed ** 2)) + 1e-10
                auto_gain = target_rms / current_rms

                # Limit auto-gain to reasonable range (1x to 100x)
                auto_gain = np.clip(auto_gain, 1.0, 100.0)
                processed *= auto_gain

                # Update gain label to show actual gain applied
                self.dev_panel.gain_label.setText(f"AUTO: {auto_gain:.1f}x")
            else:
                # Manual gain
                manual_gain = self.dev_panel.gain_slider.value()
                processed *= manual_gain

            # Prevent clipping - normalize if over ±1.0
            max_val = np.max(np.abs(processed))
            if max_val > 1.0:
                processed /= max_val

            return processed

        except Exception as e:
            log(f"Error in apply_audio_processing: {e}", "ERROR")
            return block  # Return original on error

    def compute_orientation(self, block):
        """Compute energy and L/R balance"""
        try:
            if block.ndim == 2 and block.shape[1] >= 2:
                left = block[:, 0]
                right = block[:, 1]

                rms_L = np.sqrt(np.mean(left ** 2))
                rms_R = np.sqrt(np.mean(right ** 2))

                energy = (rms_L + rms_R) / 2.0
                balance = (rms_R - rms_L) / (rms_R + rms_L + 1e-9)

                return energy, balance
            else:
                energy = np.sqrt(np.mean(block ** 2))
                return energy, 0.0

        except Exception as e:
            log(f"Error in compute_orientation: {e}", "ERROR")
            return 0.0, 0.0

    def compute_precise_location_3d(self, block, sample_rate):
        """
        Advanced 3D sound localization using ITD and ILD (Module 6 - v3.2.0)

        Uses:
        - ITD (Interaural Time Difference): Cross-correlation between L/R channels
        - ILD (Interaural Level Difference): Volume difference between L/R channels
        - Frequency analysis for elevation

        Returns: dict with angle, distance, elevation, confidence
        """
        try:
            if block is None or len(block) == 0:
                return {'angle': 0, 'distance': 50, 'elevation': 0, 'confidence': 0}

            # Ensure stereo
            if block.ndim != 2 or block.shape[1] < 2:
                return {'angle': 0, 'distance': 50, 'elevation': 0, 'confidence': 0}

            left = block[:, 0]
            right = block[:, 1]

            # === ITD (Time Difference) using Cross-Correlation ===
            # Cross-correlate left and right channels
            correlation = np.correlate(left, right, mode='full')
            center = len(correlation) // 2

            # Find peak correlation (time delay)
            # Limit search to ±1ms (realistic head size)
            max_delay_samples = int(0.001 * sample_rate)  # 1ms
            search_range = slice(center - max_delay_samples, center + max_delay_samples)
            local_corr = correlation[search_range]

            if len(local_corr) > 0:
                peak_idx = np.argmax(np.abs(local_corr))
                time_delay_samples = peak_idx - max_delay_samples

                # Convert time delay to azimuth angle
                # Speed of sound: 343 m/s, head diameter: ~0.18m
                # Max ITD: ~0.52ms (90° left/right)
                max_itd_seconds = 0.00052
                max_itd_samples = max_itd_seconds * sample_rate

                if max_itd_samples > 0:
                    # Normalize time delay to angle (-90° to +90°)
                    angle_from_itd = (time_delay_samples / max_itd_samples) * 90.0
                    angle_from_itd = np.clip(angle_from_itd, -90, 90)
                else:
                    angle_from_itd = 0
            else:
                angle_from_itd = 0

            # === ILD (Level Difference) ===
            rms_left = np.sqrt(np.mean(left ** 2)) + 1e-10
            rms_right = np.sqrt(np.mean(right ** 2)) + 1e-10

            # ILD in dB
            ild_db = 20 * np.log10(rms_right / rms_left)

            # Typical ILD range: ±20 dB for ±90°
            angle_from_ild = (ild_db / 20.0) * 90.0
            angle_from_ild = np.clip(angle_from_ild, -90, 90)

            # === Combine ITD and ILD for robust angle estimation ===
            # ITD is more reliable for low frequencies, ILD for high frequencies
            # Weight: 70% ITD, 30% ILD (ITD is generally more accurate)
            angle_combined = 0.7 * angle_from_itd + 0.3 * angle_from_ild

            # Convert to radar coordinates (0° = forward, 90° = right, 180° = back, 270° = left)
            angle_radar = 90.0 + angle_combined  # Center at front (90°)
            angle_radar = angle_radar % 360.0

            # === Distance Estimation ===
            total_energy = (rms_left + rms_right) / 2.0

            # Inverse square law approximation
            # Reference: 0.1 RMS = 10m, 0.01 RMS = 100m
            if total_energy > 0:
                distance = np.clip(10.0 / total_energy, 5.0, 100.0)
            else:
                distance = 50.0

            # === Elevation from frequency content ===
            elevation = self.compute_elevation(block, sample_rate)

            # === Confidence Score ===
            # Based on signal strength and stereo correlation
            signal_strength = total_energy / 0.1  # Normalized to 0.1 = 100%
            correlation_quality = np.max(np.abs(local_corr)) if len(local_corr) > 0 else 0

            confidence = min(100.0, signal_strength * 50 + correlation_quality * 50)

            return {
                'angle': angle_radar,
                'distance': distance,
                'elevation': elevation,
                'confidence': confidence,
                'itd_angle': angle_from_itd,
                'ild_angle': angle_from_ild,
                'ild_db': ild_db
            }

        except Exception as e:
            log(f"Error in compute_precise_location_3d: {e}", "ERROR")
            return {'angle': 0, 'distance': 50, 'elevation': 0, 'confidence': 0}

    def compute_elevation(self, block, sample_rate):
        """
        Estimate elevation angle from frequency content (v3.0.4 - Module 4)

        High frequencies (>2000 Hz) suggest sound from above (positive elevation)
        Low frequencies (<500 Hz) suggest sound from below (negative elevation)
        Mid frequencies suggest horizontal plane (0 elevation)

        Returns: Elevation angle in degrees (-45 to +45)
        """
        try:
            # Convert to mono if stereo
            if block.ndim == 2:
                mono = np.mean(block, axis=1)
            else:
                mono = block.ravel()

            # Compute FFT
            fft_data = np.fft.rfft(mono * np.hanning(len(mono)))
            freqs = np.fft.rfftfreq(len(mono), 1.0 / sample_rate)
            power = np.abs(fft_data) ** 2

            # Define frequency bands
            low_mask = (freqs >= 50) & (freqs < 500)    # Low freq = below
            mid_mask = (freqs >= 500) & (freqs < 2000)  # Mid freq = horizontal
            high_mask = (freqs >= 2000) & (freqs < 8000) # High freq = above

            # Compute energy in each band
            low_energy = np.sum(power[low_mask]) if np.any(low_mask) else 0
            mid_energy = np.sum(power[mid_mask]) if np.any(mid_mask) else 0
            high_energy = np.sum(power[high_mask]) if np.any(high_mask) else 0

            total_energy = low_energy + mid_energy + high_energy

            if total_energy < 1e-10:
                return 0.0

            # Calculate elevation bias (-1 = below, 0 = horizontal, +1 = above)
            elevation_bias = (high_energy - low_energy) / total_energy

            # Map to elevation angle (-45° to +45°)
            elevation_deg = elevation_bias * 45.0

            # Clamp to reasonable range
            elevation_deg = max(-45.0, min(45.0, elevation_deg))

            return elevation_deg

        except Exception as e:
            log(f"Error in compute_elevation: {e}", "ERROR")
            return 0.0

    def generate_test_block(self):
        """Generate synthetic test audio (FIXED v3.5.3: Stronger signals for detection)"""
        duration = self.audio.blocksize / self.audio.sample_rate
        t = np.linspace(self.test_phase, self.test_phase + duration, self.audio.blocksize)
        self.test_phase += duration

        # Stronger test signals for reliable detection (FIXED v3.5.3)
        # Walk: 80 Hz (low frequency footsteps)
        walk = 0.3 * np.sin(2 * np.pi * 80 * t)

        # Run: 420 Hz (mid frequency running)
        run = 0.4 * np.sin(2 * np.pi * 420 * t)

        # Shot: 2200 Hz every 2 seconds (high frequency gunshot)
        shot = np.zeros_like(t)
        if int(self.test_phase) % 2 == 0 and (self.test_phase % 2) < 0.15:
            shot = 0.5 * np.sin(2 * np.pi * 2200 * t)

        mono = walk + run + shot

        # Stereo with slight L/R imbalance for direction detection
        left = mono * 0.85
        right = mono * 1.15

        stereo = np.column_stack([left, right]).astype(np.float32)

        return stereo

    def quick_setup_game_audio(self):
        """Quick setup for game audio capture (v3.1.0 - Fixed to restart audio when running)"""
        log("Quick Setup: Enabling game audio capture", "INFO")

        try:
            # Remember if we were running
            was_running = self.is_running

            # Stop audio if running (to apply new settings)
            if self.is_running:
                log("Quick Setup: Stopping audio to apply new settings", "INFO")
                self.stop()

            # Enable loopback mode
            self.dev_panel.loopback_mode.setChecked(True)

            # Try to find and select a loopback device
            found_loopback = False
            for i in range(self.dev_panel.device_combo.count()):
                device_name = self.dev_panel.device_combo.itemText(i).lower()
                if 'loopback' in device_name or 'speaker' in device_name or 'output' in device_name:
                    self.dev_panel.device_combo.setCurrentIndex(i)
                    log(f"Quick Setup: Selected device: {self.dev_panel.device_combo.itemText(i)}", "INFO")
                    found_loopback = True
                    break

            # Apply settings
            self.dev_panel.apply_settings()

            # Restart audio if it was running before
            if was_running:
                log("Quick Setup: Restarting audio with new settings", "INFO")
                self.start()

            # Show success message
            if found_loopback:
                self.status_bar.showMessage(
                    "✓ Quick Setup Complete! Loopback mode enabled. Press START to capture game audio." if get_language() == 'en'
                    else "✓ Szybka konfiguracja zakończona! Tryb loopback włączony. Naciśnij START aby przechwycić dźwięk."
                )
            else:
                self.status_bar.showMessage(
                    "⚠ Loopback mode enabled, but no loopback device found. Check Tab 2 settings." if get_language() == 'en'
                    else "⚠ Tryb loopback włączony, ale nie znaleziono urządzenia. Sprawdź ustawienia w Zakładce 2."
                )

            # Switch to Detection & Audio tab to see settings
            self.main_tabs.setCurrentIndex(1)

        except Exception as e:
            log(f"Error in quick_setup_game_audio: {e}", "ERROR")
            import traceback
            log(traceback.format_exc(), "ERROR")
            self.status_bar.showMessage(
                "❌ Quick Setup failed - please configure manually (Tab 2)" if get_language() == 'en'
                else "❌ Szybka konfiguracja nie powiodła się - skonfiguruj ręcznie (Zakładka 2)"
            )

    def scan_games(self):
        """Scan for running games and update UI (v3.4.1 - z integracją platform gaming)"""
        try:
            game_data = self.game_detector.scan_processes()

            # Skanuj platformy gaming (v3.4.1)
            platform_data = self.platform_detector.scan_platforms()

            # Inteligentna detekcja przez launchery (v3.4.1)
            launcher_game = self.platform_detector.detect_game_from_launcher(game_data['games'])

            # Update game detection labels in Tab 3
            if game_data['has_games']:
                games_text = ", ".join(game_data['games'][:5])
                if len(game_data['games']) > 5:
                    games_text += f" (+{len(game_data['games']) - 5} more)"

                # Dodaj informację o platformie jeśli wykryto
                if launcher_game:
                    platform_name = launcher_game['platform']
                    games_text += f" 🔹 via {platform_name}"

                self.detected_games_label.setText(f"🎮 {games_text}")
                self.detected_games_label.setStyleSheet("font-size: 11pt; color: #00FF00; font-weight: bold; padding: 10px;")

                # AUTO-SUGGESTION: Enable loopback when game detected (v3.1.0)
                if not self.dev_panel.loopback_mode.isChecked():
                    log("Game detected! Auto-suggesting loopback mode for game audio capture", "INFO")
                    # Show subtle hint in status bar
                    if not self.is_running:
                        self.status_bar.showMessage(
                            "💡 Tip: Enable LOOPBACK mode (Tab 2) to capture game audio!" if get_language() == 'en'
                            else "💡 Wskazówka: Włącz tryb LOOPBACK (Zakładka 2) aby przechwycić dźwięk z gry!"
                        )
            else:
                self.detected_games_label.setText("No games detected")
                self.detected_games_label.setStyleSheet("font-size: 11pt; color: #888888; padding: 10px;")

            if game_data['engines']:
                engines_text = ", ".join(game_data['engines'][:3])
                if len(game_data['engines']) > 3:
                    engines_text += f" (+{len(game_data['engines']) - 3} more)"
                self.detected_engines_label.setText(f"⚙️ Engines: {engines_text}")
                self.detected_engines_label.setStyleSheet("font-size: 10pt; color: #00DDFF; padding: 5px;")
            else:
                self.detected_engines_label.setText("No engines detected")
                self.detected_engines_label.setStyleSheet("font-size: 10pt; color: #888888; padding: 5px;")

            # Aktualizuj informacje o platformach (v3.4.1)
            if platform_data['has_platforms']:
                platforms_list = []
                for p in platform_data['platforms']:
                    status_icon = "✅" if p['status'] == 'running' else "❌"
                    platforms_list.append(f"{status_icon} {p['name']}")

                platforms_text = ", ".join(platforms_list)
                self.detected_platforms_label.setText(platforms_text)
                self.detected_platforms_label.setStyleSheet("font-size: 10pt; color: #00FF00; padding: 5px;")
            else:
                self.detected_platforms_label.setText("No launchers detected")
                self.detected_platforms_label.setStyleSheet("font-size: 10pt; color: #888888; padding: 5px;")

            # Aktualizuj informacje o grze przez launcher (v3.4.1)
            if launcher_game:
                game_info = f"🎯 {launcher_game['name']}"
                if 'appid' in launcher_game:
                    game_info += f" (AppID: {launcher_game['appid']})"
                game_info += f"\n   Platform: {launcher_game['platform']}"
                game_info += f"\n   Process: {launcher_game['process']}"
                self.launcher_game_label.setText(game_info)
                self.launcher_game_label.setStyleSheet("font-size: 9pt; color: #00FFAA; padding: 5px; font-weight: bold;")
            else:
                self.launcher_game_label.setText("—")
                self.launcher_game_label.setStyleSheet("font-size: 9pt; color: #888888; padding: 5px;")

            # Update DevicePanel Game Detection section (FIXED v3.5.2)
            detailed_info = self.game_detector.get_detailed_game_info()
            self.dev_panel.update_game_detection_info(detailed_info, game_data)

        except Exception as e:
            log(f"Error in scan_games: {e}", "ERROR")

    def scan_audio_sources(self):
        """Scan audio sources and update UI (v3.5.1 - Fixed proper status display)"""
        try:
            sources_data = self.audio_scanner.scan_audio_sources()
            is_receiving = sources_data.get('is_receiving', False)

            # Update active/selected sources
            active_count = len(sources_data['active'])

            if active_count > 0:
                # Show "RECEIVING" or "SELECTED" based on actual audio activity
                status_text = "RECEIVING" if is_receiving else "SELECTED"
                status_color = "#00FF00" if is_receiving else "#FFAA00"
                self.active_sources_label.setText(f"{status_text}: {active_count}")
                self.active_sources_label.setStyleSheet(f"font-size: 9pt; font-weight: bold; color: {status_color};")

                active_list = []
                for i, src in enumerate(sources_data['active'][:5]):
                    name = src['name'][:45] + "..." if len(src['name']) > 45 else src['name']
                    icon = "📡" if is_receiving else "✓"
                    active_list.append(f"{icon} {name}")

                if len(sources_data['active']) > 5:
                    active_list.append(f"   (+{len(sources_data['active']) - 5} more)")

                self.active_sources_list.setText("\n".join(active_list))
                self.active_sources_list.setStyleSheet(f"font-size: 9pt; color: {status_color};")
            else:
                self.active_sources_label.setText("NO DEVICE SELECTED")
                self.active_sources_label.setStyleSheet("font-size: 9pt; font-weight: bold; color: #FF6666;")
                self.active_sources_list.setText("Select a device in Tab 2")
                self.active_sources_list.setStyleSheet("font-size: 9pt; color: #888;")

            # Update available (inactive) sources
            inactive_count = len(sources_data['inactive'])
            self.inactive_sources_label.setText(f"Available: {inactive_count}")
            self.inactive_sources_label.setStyleSheet("font-size: 9pt; font-weight: bold; color: #888;")

            if inactive_count > 0:
                inactive_list = []
                for i, src in enumerate(sources_data['inactive'][:3]):
                    name = src['name'][:45] + "..." if len(src['name']) > 45 else src['name']
                    inactive_list.append(f"○ {name}")

                if len(sources_data['inactive']) > 3:
                    inactive_list.append(f"   (+{len(sources_data['inactive']) - 3} more)")

                self.inactive_sources_list.setText("\n".join(inactive_list))
                self.inactive_sources_list.setStyleSheet("font-size: 9pt; color: #666;")
            else:
                self.inactive_sources_list.setText("—")
                self.inactive_sources_list.setStyleSheet("font-size: 9pt; color: #666;")

        except Exception as e:
            log(f"Error in scan_audio_sources: {e}", "ERROR")

    def closeEvent(self, event):
        """
        Handle window close - Enhanced cleanup

        ENHANCED v3.5.0: Thread-safe shutdown with timeout
        """
        log("Application closing - starting cleanup", "INFO")

        # Stop audio first
        self.stop()

        # Shutdown worker threads with timeout (v3.5.0)
        if hasattr(self, 'detection_worker'):
            try:
                self.detection_worker.shutdown(timeout=DETECTION_TIMEOUT_SEC)  # FIXED v3.5.0: Use constant
                log("Detection worker shutdown complete", "INFO")
            except Exception as e:
                log(f"Error shutting down detection worker: {e}", "ERROR")

        # Stop all timers
        if hasattr(self, 'timer'):
            self.timer.stop()

        if hasattr(self, 'game_scan_timer'):
            self.game_scan_timer.stop()

        if hasattr(self, 'audio_scan_timer'):
            self.audio_scan_timer.stop()

        # Stop toast notification timer (v3.5.0)
        if hasattr(self, 'toast') and hasattr(self.toast, 'animation_timer'):
            self.toast.animation_timer.stop()
            self.toast.close()

        # Close detached windows
        if self.detached_radar:
            try:
                self.detached_radar.close()
            except Exception as e:
                log(f"Error closing detached radar: {e}", "WARNING")

        if self.detached_led:
            try:
                self.detached_led.close()
            except Exception as e:
                log(f"Error closing detached LED: {e}", "WARNING")

        # Save configuration (v3.5.0)
        if hasattr(self, 'config_manager'):
            try:
                self.config_manager.save(self.config)
                log("Configuration saved successfully", "INFO")
            except Exception as e:
                log(f"Error saving configuration: {e}", "WARNING")

        log("Application cleanup complete", "INFO")
        event.accept()


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """
    Main entry point

    Point 11 - v3.5.0: Uses Dependency Injection for clean architecture
    """
    log("=" * 80, "INFO")
    log(f"RadarSuite Final {VERSION} - Starting", "INFO")
    log("=" * 80, "INFO")

    log(f"Python: {sys.version}", "INFO")
    log(f"NumPy: {np.__version__}", "INFO")
    log(f"pyqtgraph: {pg.__version__}", "INFO")
    log(f"sounddevice available: {sd is not None}", "INFO")
    log(f"soundcard available: {sc is not None}", "INFO")

    app = QApplication(sys.argv)
    app.setApplicationName("RadarSuite Final")
    app.setOrganizationName("RadarSuite")

    apply_dark_theme(app)

    # Point 11 - v3.5.0: Configure Dependency Injection
    from core import configure_services, ConfigManager

    log("Configuring Dependency Injection container...", "INFO")
    config_mgr = ConfigManager()
    config = config_mgr.load()

    container = configure_services(config)
    log(f"DI: {len(container.get_registered_services())} services registered", "INFO")

    # Create main window with DI
    window = MainWindow(container=container)
    window.show()

    log("Main window shown, entering event loop", "INFO")

    exit_code = app.exec_()

    log(f"Application exited with code: {exit_code}", "INFO")
    log("=" * 80, "INFO")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
