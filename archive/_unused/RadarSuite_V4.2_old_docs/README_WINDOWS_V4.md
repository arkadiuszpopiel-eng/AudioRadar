# RadarSuite Windows V4

**Dedykowana wersja dla systemu Windows x64**

## Ważne informacje

- ✅ Ta wersja buduje **TYLKO dla Windows x64**
- ✅ Wszystkie buildy są w oddzielnym katalogu `dist\RadarSuite_Windows`
- ✅ Logi są zapisywane do `build_windows.log`
- ✅ **NIE MIESZAJ** z wersją Linux - każda wersja ma własny katalog!

## Wymagania systemowe

### Python
- **Python 3.11** (wymagane)
- Pobierz z: https://www.python.org/
- **Ważne:** Podczas instalacji zaznacz "Add Python to PATH"!

### System operacyjny
- Windows 10/11 (x64)
- Visual C++ Redistributable (opcjonalnie, zwykle już zainstalowane)

## Budowanie

### Szybki start
```cmd
RUN_BUILD_ALL_Win.cmd
```

### Co robi skrypt?
1. Sprawdza Python 3.11
2. Tworzy wirtualne środowisko (`.venv`)
3. Instaluje zależności Python z `requirements-windows.txt`
4. Weryfikuje instalację PyQt5, numpy, scipy, itp.
5. Buduje EXE używając `radarsuite_windows.spec`
6. Tworzy archiwum ZIP z timestampem

## Wyjście

### Plik executable
```
dist\RadarSuite_Windows\RadarSuite_Windows.exe
```

### Archiwum ZIP
```
dist\RadarSuite_Windows_V4_v4.0.0_Windows-x64_<timestamp>.zip
```

## Uruchomienie

### Z katalogu dist:
```cmd
cd dist\RadarSuite_Windows
RadarSuite_Windows.exe
```

### Z archiwum ZIP:
1. Rozpakuj `dist\RadarSuite_Windows_V4_*.zip`
2. Otwórz folder `RadarSuite_Windows`
3. Uruchom `RadarSuite_Windows.exe`

## Optymalizacje Windows V4

Ta wersja zawiera optymalizacje redukujące ostrzeżenia podczas builda:

✅ **Wykluczone moduły opcjonalne:**
- `pyqtgraph.jupyter` (wymaga jupyter_rfb)
- `scipy.special._cdflib` (przestarzały moduł scipy)
- Qt5 3D modules (Qt3DCore, Qt3DRender, itp.)
- Qt5 WebEngine (nie używany w RadarSuite)
- Qt5 Multimedia (używamy sounddevice zamiast)
- Qt5 SQL (nie używany)

✅ **Dedykowany spec file:**
- `build_tools\radarsuite_windows.spec`
- Optymalizowany dla Windows, bez modułów Linux

✅ **Automatyczna instalacja DLL:**
- PyQt5 automatycznie instaluje wszystkie potrzebne DLL
- Brak potrzeby ręcznej instalacji bibliotek systemowych

## Rozwiązywanie problemów

### Python nie został znaleziony
```
[ERROR] Python 3.11 is not installed or not in PATH!
```

Rozwiązanie:
1. Zainstaluj Python 3.11 z https://www.python.org/
2. Podczas instalacji zaznacz "Add Python to PATH"
3. Uruchom ponownie terminal

### Ostrzeżenia o Qt5 DLL podczas builda
```
WARNING: Library not found: could not resolve 'Qt53DCore.dll'
```

To normalne! Te DLL są opcjonalne i **nie są wymagane** do działania RadarSuite.
Build zakończy się sukcesem i aplikacja będzie działać poprawnie.

### Błędy instalacji requirements
```
[ERROR] Failed to install requirements from requirements-windows.txt
```

Rozwiązanie:
1. Sprawdź połączenie internetowe
2. Sprawdź logi w `build_windows.log`
3. Spróbuj uruchomić ponownie skrypt

### Antywirus blokuje exe
Niektóre antywirus mogą fałszywie wykryć PyInstaller EXE jako podejrzany.

Rozwiązanie:
- Dodaj folder `dist\RadarSuite_Windows` do wyjątków antyvirusa
- To normalne zachowanie dla aplikacji spakowanych PyInstaller

## Logi

- **Build log:** `build_windows.log`
- **Runtime log:** Wewnątrz aplikacji (sprawdź `app\core\logger.py`)

## Różnice vs RadarSuite_Linux_V4

| Feature | Windows V4 | Linux V4 |
|---------|------------|----------|
| Platform | Windows x64 | Linux x64 |
| Build script | `RUN_BUILD_ALL_Win.cmd` | `RUN_BUILD_ALL_Linux.sh` |
| Spec file | `radarsuite_windows.spec` | `radarsuite_linux.spec` |
| Requirements | `requirements-windows.txt` | `requirements-linux.txt` |
| Output dir | `dist\RadarSuite_Windows` | `dist/RadarSuite_Linux` |
| Executable | `RadarSuite_Windows.exe` | `RadarSuite_Linux` |
| Log file | `build_windows.log` | `build_linux.log` |
| System libs | Automatyczne (via pip) | Wymagane ręczne (apt/dnf) |

## Struktura katalogów

```
RadarSuite_Windows_V4/
├── app/                          # Kod źródłowy aplikacji
├── build_tools/
│   └── radarsuite_windows.spec   # PyInstaller spec dla Windows
├── dist/                         # Output (tworzone przez build)
│   ├── RadarSuite_Windows/       # Folder z exe i zależnościami
│   └── RadarSuite_Windows_V4_*.zip  # Archiwum dystrybucyjne
├── .venv/                        # Wirtualne środowisko (tworzone)
├── requirements-windows.txt      # Zależności Python (Windows)
├── RUN_BUILD_ALL_Win.cmd         # Skrypt buildowania
└── README_WINDOWS_V4.md          # Ten plik
```

## Wersja

**RadarSuite Windows V4.0.0**
- Bazuje na RadarSuite Final v3.5.0
- Dedykowana dla Windows
- Zoptymalizowana pod kątem redukcji ostrzeżeń

## FAQ

### Czy mogę buildować na Windows 11?
Tak! RadarSuite Windows V4 działa na Windows 10 i 11 (x64).

### Czy potrzebuję Visual Studio?
Nie. Python 3.11 zawiera wszystko co potrzebne do builda.

### Dlaczego exe jest tak duży (~13MB)?
PyInstaller pakuje Python interpreter + wszystkie biblioteki (PyQt5, numpy, scipy, itp.) w jeden plik wykonywalny. To normalne.

### Czy mogę dystrybuować exe?
Tak! Rozpakuj ZIP i całą zawartość folderu `RadarSuite_Windows` możesz kopiować na inne komputery z Windows.

## Wsparcie

W przypadku problemów sprawdź:
1. `build_windows.log` - logi z procesu budowania
2. Python 3.11 jest zainstalowany i w PATH
3. Antywirus nie blokuje procesu

---

**UWAGA:** Nie builduj wersji Linux w tym katalogu! Użyj `RadarSuite_Linux_V4/` do buildów Linux.
