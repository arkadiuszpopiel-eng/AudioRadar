# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for RadarSuite Linux V4.2
Builds standalone Linux executable with all dependencies
Platform: Linux x64 ONLY
Synchronized with Windows V4.2 features
Optimized: Excludes Windows-only modules and reduces warnings
Includes: PyQt5, pyqtgraph, PyOpenGL (3D radar), psutil (game detection)
"""

import os
import sys
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Get base path - use __file__ for more reliable path resolution
# SPEC variable may not work correctly in all environments
try:
    spec_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Fallback to SPEC if __file__ not available (older PyInstaller)
    spec_dir = os.path.dirname(os.path.abspath(SPEC))

BASE = os.path.dirname(spec_dir)
APP_DIR = os.path.join(BASE, 'app')

# Entry point
entry_script = os.path.join(BASE, 'app', 'main.py')

# Verify entry script exists
if not os.path.exists(entry_script):
    raise FileNotFoundError(f"Entry script not found: {entry_script}\nBASE={BASE}\nCWD={os.getcwd()}")

# Add app directory to Python path for module imports
sys.path.insert(0, APP_DIR)

# Collect essential PyQt5 and pyqtgraph modules
# Note: Using selective imports to avoid Qt initialization issues during build
hiddenimports = []

# Custom application modules (CRITICAL for PyInstaller)
# UPDATED V4.2: Added new detection modules synchronized with Windows
hiddenimports += [
    'core', 'core.constants', 'core.config', 'core.logger', 'core.translations', 'core.di', 'core.confidence',
    'hardware', 'hardware.gpu', 'hardware.soundblaster',
    'utils', 'utils.performance', 'utils.game_detection', 'utils.platform_detection', 'utils.audio_scanner', 'utils.launcher', 'utils.game_detector',
    'tracking', 'tracking.target', 'tracking.tracker', 'tracking.threat',
    # V4.2: Enhanced detection modules
    'detection', 'detection.worker', 'detection.footstep', 'detection.shot', 'detection.machine', 'detection.spectral',
    'audio', 'audio.cache', 'audio.engine', 'audio.classifier', 'audio.recorder', 'audio.voice', 'audio.voice_detector',
    'widgets', 'widgets.toast', 'widgets.radar', 'widgets.radar3d', 'widgets.led',
    'widgets.spectrum', 'widgets.waterfall', 'widgets.waveform', 'widgets.panels',
    'widgets.detection_panel', 'widgets.device_panel', 'widgets.military_spectrum'
]

# PyQt5 modules
hiddenimports += [
    'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets',
    'PyQt5.QtOpenGL', 'PyQt5.sip'
]

# pyqtgraph modules
hiddenimports += [
    'pyqtgraph', 'pyqtgraph.graphicsItems', 'pyqtgraph.opengl',
    'pyqtgraph.widgets', 'pyqtgraph.exporters'
]

# OpenGL modules
hiddenimports += [
    'OpenGL', 'OpenGL.GL', 'OpenGL.GLU', 'OpenGL.GLUT',
    'OpenGL.arrays', 'OpenGL.platform'
]

# Scientific computing
hiddenimports += ['numpy', 'scipy', 'scipy.signal', 'scipy.fft']

# Audio libraries (Linux: sounddevice + soundcard + pulsectl)
hiddenimports += ['sounddevice', 'soundcard', 'pulsectl']

# System utilities
hiddenimports += ['psutil']  # Required for game detection (Module 3)

# Standard library
hiddenimports += ['queue', 'math', 'pathlib', 'datetime', 'collections', 'threading', 'subprocess']

# Collect data files for PyQt5 and pyqtgraph
datas = []
datas += collect_data_files('PyQt5')
datas += collect_data_files('pyqtgraph')

# CRITICAL: Include sounddevice data files (contains PortAudio libraries)
try:
    datas += collect_data_files('sounddevice')
except Exception:
    print("Warning: Could not collect sounddevice data files")

# Also try to collect _sounddevice_data which contains PortAudio binaries
try:
    datas += collect_data_files('_sounddevice_data')
except Exception:
    pass

# LINUX OPTIMIZATIONS: Exclude modules that cause warnings
excludes = [
    # GUI frameworks we don't use
    'matplotlib', 'pandas', 'PIL', 'tkinter',
    # Optional pyqtgraph features
    'pyqtgraph.jupyter', 'jupyter_rfb',
    # Optional scipy modules
    'scipy.special._cdflib',
    # Qt5 3D modules (not used in RadarSuite)
    'PyQt5.Qt3DCore', 'PyQt5.Qt3DRender', 'PyQt5.Qt3DAnimation',
    'PyQt5.Qt3DInput', 'PyQt5.Qt3DLogic', 'PyQt5.Qt3DExtras',
    # Qt5 WebEngine (not used)
    'PyQt5.QtWebEngine', 'PyQt5.QtWebEngineCore', 'PyQt5.QtWebEngineWidgets',
    # Qt5 Multimedia (not used - we use sounddevice instead)
    'PyQt5.QtMultimedia', 'PyQt5.QtMultimediaWidgets',
    # Windows-only modules
    'pyaudiowpatch', 'pywin32', 'pythoncom', 'win32api', 'win32com',
]

# Analysis
a = Analysis(
    [entry_script],
    pathex=[BASE, APP_DIR],  # Include app directory for module imports
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# PYZ
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# EXE
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='RadarSuite_Linux',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window (GUI app)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

# COLLECT
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='RadarSuite_Linux',
)
