# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['audio_radar/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('audio_radar/config.json', 'audio_radar'),
    ],
    hiddenimports=[
        'numpy',
        'sounddevice',
        'pygame',
        'audio_radar.main',
        'audio_radar.audio_capture',
        'audio_radar.sound_analysis',
        'audio_radar.visualization',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AudioRadar',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AudioRadar',
)
