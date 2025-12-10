"""Runtime hook zapewniający krótką ścieżkę do PortAudio dla sounddevice.

- Dodaje katalog z DLL PortAudio (_sounddevice_data/portaudio-binaries) do PATH.
- Jeśli DLL zostały skopiowane do katalogu głównego dist, dodaje także tę lokalizację.
Pozwala to uniknąć błędów "PortAudio library not found" i problemów z długimi ścieżkami.
"""
import os
import sys
from pathlib import Path

# Bazowy katalog uruchomieniowy (MEIPASS w trybie onefile, inaczej ścieżka bieżącego pliku)
base_dir = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))

candidates = [
    base_dir / '_sounddevice_data' / 'portaudio-binaries',
    base_dir,  # DLL skopiowane bezpośrednio do katalogu dist
]

existing = [str(p) for p in candidates if p.exists()]
if existing:
    path_parts = os.environ.get('PATH', '').split(os.pathsep)
    # wstawiamy na początek, by Windows znalazł właściwe DLL
    os.environ['PATH'] = os.pathsep.join(existing + path_parts)

# Podpowiedz sounddevice, której biblioteki ma szukać (krótka nazwa)
if 'SOUNDDEVICE_LIBRARY_FILENAME' not in os.environ:
    os.environ['SOUNDDEVICE_LIBRARY_FILENAME'] = 'libportaudio64bit.dll'
