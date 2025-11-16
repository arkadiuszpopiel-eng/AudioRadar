# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for RadarSuite Final v3.0.5
Builds standalone EXE with all dependencies
Includes: PyQt5, pyqtgraph, PyOpenGL (3D radar), psutil (game detection)
"""

import os
import sys
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Get base path
BASE = os.path.dirname(os.path.dirname(os.path.abspath(SPEC)))

# Entry point
entry_script = os.path.join(BASE, 'app', 'main.py')

# Collect all PyQt5 and pyqtgraph modules
hiddenimports = []
hiddenimports += collect_submodules('PyQt5')
hiddenimports += collect_submodules('pyqtgraph')
hiddenimports += collect_submodules('OpenGL')  # Required for 3D radar (Module 4)
hiddenimports += ['numpy', 'scipy', 'scipy.signal']
hiddenimports += ['sounddevice', 'soundcard']
hiddenimports += ['psutil']  # Required for game detection (Module 3)
hiddenimports += ['queue', 'math', 'pathlib', 'datetime']

# Collect data files for PyQt5 and pyqtgraph
datas = []
datas += collect_data_files('PyQt5')
datas += collect_data_files('pyqtgraph')

# Analysis
a = Analysis(
    [entry_script],
    pathex=[BASE],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'pandas', 'PIL', 'tkinter'],
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
    name='RadarSuite_Final',
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
    name='RadarSuite_Final',
)
