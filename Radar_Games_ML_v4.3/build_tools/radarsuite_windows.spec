# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Radar Games ML v4.3
Builds standalone Windows executable with all dependencies
Platform: Windows x64 ONLY
Optimized: Excludes Linux-only modules and reduces warnings
Includes: PyQt5, pyqtgraph, PyOpenGL (3D radar), psutil (game detection), ML training

PORTED FROM v4.2.1 radarsuite_windows.spec
ADAPTED FOR v4.3 structure with root main.py entrypoint and app.* imports
"""

import os
import sys
from pathlib import Path
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

# v4.3: Entry point is now root main.py (which delegates to app.main)
entry_script = os.path.join(BASE, 'main.py')

# Verify entry script exists
if not os.path.exists(entry_script):
    raise FileNotFoundError(f"Entry script not found: {entry_script}\nBASE={BASE}\nCWD={os.getcwd()}")

# Add app directory to Python path for module imports
sys.path.insert(0, APP_DIR)

# Collect essential PyQt5 and pyqtgraph modules
# Note: Using selective imports to avoid Qt initialization issues during build
hiddenimports = []

# v4.3: app.* prefix since we now use clean absolute imports
# Custom application modules (CRITICAL for PyInstaller)
hiddenimports += [
    # Version module (v4.3)
    'app.version',
    # Core modules (v4.3: with app. prefix)
    'app.core', 'app.core.constants', 'app.core.config', 'app.core.logger', 'app.core.translations',
    'app.core.di', 'app.core.confidence', 'app.core.error_handler', 'app.core.profiler', 'app.core.export_import',
    # Also include without prefix for backward compatibility
    'core', 'core.constants', 'core.config', 'core.logger', 'core.translations',
    'core.di', 'core.confidence', 'core.error_handler', 'core.profiler', 'core.export_import',
    # Hardware modules
    'app.hardware', 'app.hardware.gpu', 'app.hardware.soundblaster',
    'hardware', 'hardware.gpu', 'hardware.soundblaster',
    # Utilities
    'app.utils', 'app.utils.performance', 'app.utils.game_detector', 'app.utils.audio_scanner', 'app.utils.launcher',
    'utils', 'utils.performance', 'utils.game_detector', 'utils.audio_scanner', 'utils.launcher',
    # Tracking modules
    'app.tracking', 'app.tracking.target', 'app.tracking.threat',
    'tracking', 'tracking.target', 'tracking.threat',
    # Detection modules
    'app.detection', 'app.detection.worker', 'app.detection.footstep', 'app.detection.shot',
    'app.detection.machine', 'app.detection.spectral',
    'detection', 'detection.worker', 'detection.footstep', 'detection.shot',
    'detection.machine', 'detection.spectral',
    # Audio modules
    'app.audio', 'app.audio.cache', 'app.audio.engine', 'app.audio.classifier',
    'app.audio.processor', 'app.audio.recorder', 'app.audio.voice_detector',
    'audio', 'audio.cache', 'audio.engine', 'audio.classifier',
    'audio.processor', 'audio.recorder', 'audio.voice_detector',
    # Widgets (all in separate files)
    'app.widgets', 'app.widgets.toast', 'app.widgets.radar', 'app.widgets.led', 'app.widgets.spectrum',
    'app.widgets.detection_panel', 'app.widgets.device_panel', 'app.widgets.ml_training_panel',
    'app.widgets.ml_waveform', 'app.widgets.military_spectrum', 'app.widgets.waveform_timeline',
    'widgets', 'widgets.toast', 'widgets.radar', 'widgets.led', 'widgets.spectrum',
    'widgets.detection_panel', 'widgets.device_panel', 'widgets.ml_training_panel',
    'widgets.ml_waveform', 'widgets.military_spectrum', 'widgets.waveform_timeline',
    # ML modules (v4.3)
    'app.ml', 'app.ml.detector', 'app.ml.feature_extractor', 'app.ml.yamnet', 'app.ml.model_registry',
    'app.ml.training', 'app.ml.training.recorder', 'app.ml.training.session_manager', 'app.ml.training.trainer',
    'app.ml.training.session_validator', 'app.ml.training.async_session_worker',
    'ml', 'ml.detector', 'ml.feature_extractor', 'ml.yamnet', 'ml.model_registry',
    'ml.training', 'ml.training.recorder', 'ml.training.session_manager', 'ml.training.trainer',
    'ml.training.session_validator', 'ml.training.async_session_worker',
    # UI modules
    'app.ui', 'app.ui.builder',
    'ui', 'ui.builder',
    # Diagnostics
    'app.diagnostics', 'app.diagnostics.selftest',
    'diagnostics', 'diagnostics.selftest',
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

# Audio libraries
hiddenimports += ['sounddevice', 'soundcard']

# System utilities
hiddenimports += ['psutil']  # Required for game detection (Module 3)

# Standard library
hiddenimports += ['queue', 'math', 'pathlib', 'datetime', 'collections', 'threading']

# Collect data files for PyQt5 and pyqtgraph
datas = []
datas += collect_data_files('PyQt5')
datas += collect_data_files('pyqtgraph')

# CRITICAL: Include sounddevice data files (contains PortAudio DLLs)
try:
    datas += collect_data_files('sounddevice')
except Exception:
    print("Warning: Could not collect sounddevice data files")

# Also try to collect _sounddevice_data which contains PortAudio binaries
try:
    datas += collect_data_files('_sounddevice_data')
except Exception:
    pass

# Include PortAudio DLLs as binaries to avoid load failures on Windows
binaries = []
try:
    import importlib.util

    sd_spec = importlib.util.find_spec('_sounddevice_data')
    if sd_spec and sd_spec.submodule_search_locations:
        pa_dir = Path(list(sd_spec.submodule_search_locations)[0]) / 'portaudio-binaries'
        if pa_dir.is_dir():
            for dll_path in pa_dir.glob('*.dll'):
                # Zachowujemy oryginalną lokalizację w _sounddevice_data
                binaries.append((str(dll_path), str(Path('_sounddevice_data/portaudio-binaries'))))
                # Dodatkowo kopiujemy DLL do katalogu głównego dist, aby skrócić ścieżkę
                binaries.append((str(dll_path), '.'))
except Exception as e:
    print(f"[WARNING] Could not collect PortAudio binaries: {e}")

# WINDOWS OPTIMIZATIONS: Exclude modules that cause warnings
excludes = [
    # GUI frameworks we don't use
    'matplotlib', 'pandas', 'PIL', 'tkinter',
    # Optional pyqtgraph features
    'pyqtgraph.jupyter', 'jupyter_rfb',
    # Optional scipy modules
    'scipy.special._cdflib',
    # Qt5 3D modules (not used in Radar Games ML)
    'PyQt5.Qt3DCore', 'PyQt5.Qt3DRender', 'PyQt5.Qt3DAnimation',
    'PyQt5.Qt3DInput', 'PyQt5.Qt3DLogic', 'PyQt5.Qt3DExtras',
    # Qt5 WebEngine (not used)
    'PyQt5.QtWebEngine', 'PyQt5.QtWebEngineCore', 'PyQt5.QtWebEngineWidgets',
    # Qt5 Multimedia (not used - we use sounddevice instead)
    'PyQt5.QtMultimedia', 'PyQt5.QtMultimediaWidgets',
    # Qt5 SQL (not used)
    'PyQt5.QtSql',
]

# Analysis
a = Analysis(
    [entry_script],
    pathex=[BASE, APP_DIR],  # Include app directory for module imports
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[os.path.join(spec_dir, 'portaudio_path_hook.py')],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# PYZ
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# EXE (v4.3: Updated name to Radar_Games_ML)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Radar_Games_ML',
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

# Używamy krótkiej nazwy katalogu dist, aby uniknąć błędów Windows (206: filename too long)
dist_dir_name = 'RGML'

# COLLECT (v4.3: skrócona nazwa katalogu dist)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=dist_dir_name,
)

# Post-build: Copy EXE to project root for easy access (v4.3.0)
# Note: This runs after COLLECT completes
import shutil
import time

def post_build_copy():
    """Copy EXE to project root with error handling"""
    exe_source = os.path.join(BASE, 'dist', dist_dir_name, 'Radar_Games_ML.exe')
    exe_dest = os.path.join(BASE, 'Radar_Games_ML.exe')

    print("\n" + "="*60)
    print("POST-BUILD: Copying EXE to project root")
    print("="*60)

    # Wait a moment for file system to settle
    time.sleep(0.5)

    if os.path.exists(exe_source):
        try:
            # Remove old EXE if exists
            if os.path.exists(exe_dest):
                os.remove(exe_dest)
                print(f"[OK] Removed old: {os.path.basename(exe_dest)}")

            # Copy new EXE
            shutil.copy2(exe_source, exe_dest)
            size_mb = os.path.getsize(exe_dest) / (1024 * 1024)
            print(f"[OK] Copied: {os.path.basename(exe_source)} -> project root")
            print(f"  Size: {size_mb:.2f} MB")
            print(f"  Location: {exe_dest}")
            print("\n[OK] POST-BUILD COMPLETE!")
            print("="*60)
        except Exception as e:
            print(f"[ERROR] Copy failed: {e}")
            print("  EXE is still available in: dist/Radar_Games_ML/")
    else:
        print(f"[WARNING] EXE not found at: {exe_source}")
        print("  Check dist/ folder for build output")

# Execute post-build
post_build_copy()
