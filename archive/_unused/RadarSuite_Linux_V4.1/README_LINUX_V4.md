# RadarSuite Linux V4

**Dedykowana wersja dla systemu Linux x64**

## Ważne informacje

- ✅ Ta wersja buduje **TYLKO dla Linux x64**
- ✅ Wszystkie buildy są w oddzielnym katalogu `dist/RadarSuite_Linux`
- ✅ Logi są zapisywane do `build_linux.log`
- ✅ **NIE MIESZAJ** z wersją Windows - każda wersja ma własny katalog!

## Wymagania systemowe

### Python
- **Python 3.11** (wymagane)

### Biblioteki systemowe Linux

**UWAGA:** Przed uruchomieniem builda **musisz zainstalować** systemowe biblioteki!

#### Ubuntu/Debian:
```bash
sudo apt install libpulse0 portaudio19-dev libxcb-xinerama0 \
                 libxcb-image0 libxcb-icccm4 libxcb-keysyms1 \
                 libxkbcommon-x11-0 libxcb-render-util0 \
                 libxcb-xkb1 libxcb-shape0 libopengl0
```

#### Fedora/RHEL:
```bash
sudo dnf install pulseaudio-libs portaudio-devel libxcb \
                 xcb-util-image xcb-util-wm xcb-util-keysyms \
                 libxkbcommon-x11 xcb-util-renderutil libglvnd-opengl
```

#### Arch Linux:
```bash
sudo pacman -S libpulse portaudio libxcb xcb-util-image \
               xcb-util-wm xcb-util-keysyms libxkbcommon-x11 \
               xcb-util-renderutil libglvnd
```

## Budowanie

### Szybki start
```bash
chmod +x RUN_BUILD_ALL_Linux.sh
./RUN_BUILD_ALL_Linux.sh
```

### Co robi skrypt?
1. Sprawdza Python 3.11
2. Tworzy wirtualne środowisko (`.venv`)
3. **Sprawdza systemowe biblioteki Linux** (PulseAudio, XCB, itp.)
4. Instaluje zależności Python z `requirements-linux.txt`
5. Buduje executable używając `radarsuite_linux.spec`
6. Tworzy archiwum ZIP z timestampem

## Wyjście

### Plik executable
```
dist/RadarSuite_Linux/RadarSuite_Linux
```

### Archiwum ZIP
```
dist/RadarSuite_Linux_V4_v4.0.0_Linux-x64_<timestamp>.zip
```

## Uruchomienie

### Z katalogu dist:
```bash
cd dist/RadarSuite_Linux
./RadarSuite_Linux
```

### Z archiwum ZIP:
```bash
unzip dist/RadarSuite_Linux_V4_*.zip
cd RadarSuite_Linux
./RadarSuite_Linux
```

## Optymalizacje Linux V4

Ta wersja zawiera optymalizacje redukujące ostrzeżenia podczas builda:

✅ **Wykluczone moduły opcjonalne:**
- `pyqtgraph.jupyter` (wymaga jupyter_rfb)
- `scipy.special._cdflib` (przestarzały moduł scipy)
- Qt5 3D modules (Qt3DCore, Qt3DRender, itp.)
- Qt5 WebEngine (nie używany)
- Qt5 Multimedia (używamy sounddevice zamiast)

✅ **Dedykowany spec file:**
- `build_tools/radarsuite_linux.spec`
- Optymalizowany dla Linux, bez modułów Windows

✅ **Sprawdzanie systemowych bibliotek:**
- Automatyczne wykrywanie brakujących bibliotek
- Komunikaty z instrukcjami instalacji

## Rozwiązywanie problemów

### Brak bibliotek systemowych
Jeśli podczas builda widzisz ostrzeżenia typu:
```
WARNING: Library not found: could not resolve 'libpulse.so.0'
```

Zainstaluj brakujące biblioteki (patrz sekcja "Wymagania systemowe" powyżej).

### Błędy audio (sounddevice)
```
WARNING: portaudio shared library not found
```

Rozwiązanie:
```bash
sudo apt install libpulse0 portaudio19-dev  # Ubuntu/Debian
```

### Błędy GUI (PyQt5/XCB)
```
WARNING: Library not found: libxcb-*
```

Rozwiązanie:
```bash
sudo apt install libxcb-xinerama0 libxcb-image0 libxcb-icccm4  # Ubuntu/Debian
```

## Logi

- **Build log:** `build_linux.log`
- **Runtime log:** Wewnątrz aplikacji (sprawdź `app/core/logger.py`)

## Różnice vs RadarSuite_Windows_V4

| Feature | Linux V4 | Windows V4 |
|---------|----------|------------|
| Platform | Linux x64 | Windows x64 |
| Build script | `RUN_BUILD_ALL_Linux.sh` | `RUN_BUILD_ALL_Win.cmd` |
| Spec file | `radarsuite_linux.spec` | `radarsuite_windows.spec` |
| Requirements | `requirements-linux.txt` | `requirements-windows.txt` |
| Output dir | `dist/RadarSuite_Linux` | `dist/RadarSuite_Windows` |
| Executable | `RadarSuite_Linux` | `RadarSuite_Windows.exe` |
| Log file | `build_linux.log` | `build_windows.log` |

## Wersja

**RadarSuite Linux V4.0.0**
- Bazuje na RadarSuite Final v3.5.0
- Dedykowana dla Linux
- Zoptymalizowana pod kątem redukcji ostrzeżeń

## Wsparcie

W przypadku problemów sprawdź:
1. `build_linux.log` - logi z procesu budowania
2. Zainstalowane biblioteki systemowe
3. Python 3.11 jest zainstalowany

---

**UWAGA:** Nie builduj wersji Windows w tym katalogu! Użyj `RadarSuite_Windows_V4/` do buildów Windows.
