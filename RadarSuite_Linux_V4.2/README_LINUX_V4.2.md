# RadarSuite Linux V4.2

Wersja Linux zsynchronizowana z Windows V4.2.

## Nowe funkcje w V4.2

- **Detekcja strzałów** (`detection/shot.py`) - rozpoznawanie dźwięków strzałów
- **Detekcja ML** (`detection/machine.py`) - machine learning dla lepszej klasyfikacji
- **Analiza spektralna** (`detection/spectral.py`) - zaawansowana analiza FFT
- **System pewności** (`core/confidence.py`) - scoring pewności detekcji
- **Ulepszone śledzenie celów** (`tracking/target.py`) - rozszerzony tracker
- **Wsparcie 5.1/7.1 surround** - automatyczna detekcja kanałów

## Wymagania systemowe

### Python
- Python 3.11 lub nowszy

### Biblioteki systemowe (Ubuntu/Debian)
```bash
sudo apt install libpulse0 portaudio19-dev libxcb-xinerama0 \
                 libxcb-image0 libxcb-icccm4 libxcb-keysyms1 \
                 libxkbcommon-x11-0 libxcb-render-util0 \
                 libxcb-xkb1 libxcb-shape0 libopengl0
```

### Biblioteki systemowe (Fedora/RHEL)
```bash
sudo dnf install pulseaudio-libs portaudio-devel libxcb \
                 xcb-util-image xcb-util-wm xcb-util-keysyms \
                 libxkbcommon-x11 xcb-util-renderutil libglvnd-opengl
```

### Biblioteki systemowe (Arch Linux)
```bash
sudo pacman -S libpulse portaudio libxcb xcb-util-image \
               xcb-util-wm xcb-util-keysyms libxkbcommon-x11 \
               xcb-util-renderutil libglvnd
```

## Instalacja i budowanie

### 1. Przejdź do katalogu
```bash
cd RadarSuite_Linux_V4.2
```

### 2. Uruchom skrypt budowania
```bash
chmod +x RUN_BUILD_ALL_Linux.sh
./RUN_BUILD_ALL_Linux.sh
```

### 3. Uruchom aplikację
```bash
cd dist/RadarSuite_Linux
./RadarSuite_Linux
```

## Backend audio

Linux V4.2 używa:
- **soundcard** z PulseAudio monitor dla loopback
- **sounddevice** dla standardowych urządzeń wejściowych
- **pulsectl** (opcjonalnie) dla lepszego listowania urządzeń PulseAudio

### Konfiguracja PulseAudio

Upewnij się, że PulseAudio lub PipeWire działa:
```bash
pactl info
```

Sprawdź dostępne urządzenia monitor:
```bash
pactl list sources | grep -A 2 "Name:"
```

## Struktura katalogów

```
RadarSuite_Linux_V4.2/
├── app/                          # Kod źródłowy
│   ├── audio/                    # Moduły audio
│   │   ├── engine.py             # PulseAudio backend
│   │   └── ...
│   ├── core/                     # Moduły rdzenne
│   │   ├── confidence.py         # [NEW] System pewności
│   │   └── ...
│   ├── detection/                # Moduły detekcji
│   │   ├── footstep.py           # Detektor kroków
│   │   ├── shot.py               # [NEW] Detektor strzałów
│   │   ├── machine.py            # [NEW] ML detekcja
│   │   ├── spectral.py           # [NEW] Analiza spektralna
│   │   └── worker.py             # Worker thread
│   ├── tracking/                 # Śledzenie celów
│   ├── utils/                    # Narzędzia
│   ├── widgets/                  # Widgety GUI
│   └── main.py                   # Punkt wejścia
├── build_tools/
│   └── radarsuite_linux.spec     # PyInstaller spec
├── requirements-linux.txt        # Zależności Python
├── RUN_BUILD_ALL_Linux.sh        # Skrypt budowania
└── README_LINUX_V4.2.md          # Ten plik
```

## Różnice względem Windows V4.2

| Aspekt | Windows V4.2 | Linux V4.2 |
|--------|--------------|------------|
| Audio backend | pyaudiowpatch (WASAPI) | soundcard (PulseAudio) |
| Loopback | WASAPI loopback device | PulseAudio monitor source |
| Detekcja gry | Win32 API (psutil) | /proc + psutil |
| Pakowanie | PyInstaller + .exe | PyInstaller + ELF |

## Rozwiązywanie problemów

### Brak dźwięku / brak urządzeń
```bash
# Sprawdź PulseAudio
pulseaudio --check && echo "PulseAudio OK" || echo "PulseAudio not running"

# Uruchom PulseAudio jeśli nie działa
pulseaudio --start

# Sprawdź urządzenia
pactl list sources short
```

### Błąd Qt / XCB
```bash
# Zainstaluj brakujące biblioteki XCB
sudo apt install libxcb-xinerama0 libxcb-image0 libxcb-icccm4 \
                 libxcb-keysyms1 libxkbcommon-x11-0
```

### Błąd OpenGL
```bash
# Zainstaluj Mesa
sudo apt install libgl1-mesa-glx libopengl0
```

## Wersja

- **V4.2.0** - Synchronizacja z Windows V4.2
  - Dodano detekcję strzałów
  - Dodano ML detection
  - Dodano analizę spektralną
  - Dodano system pewności
  - Ulepszono śledzenie celów
  - Wsparcie 5.1/7.1 surround

## Autor

Wersja Linux utworzona przez synchronizację z Windows V4.2.
Data synchronizacji: 2025-12-04
