# Poprawka błędu PyInstaller - RadarSuite Final (Windows 11)

## Problem

Otrzymujesz błąd: **[ERROR] PyInstaller not available**

## Przyczyny błędu na Windows 11

1. **PyInstaller nie jest zainstalowany** - Najczęstsza przyczyna
2. **Środowisko wirtualne nie jest aktywowane** - PyInstaller zainstalowany, ale nie w aktywnym środowisku
3. **Problem z PATH** - PyInstaller zainstalowany, ale niedostępny w wierszu poleceń
4. **Uruchamianie przez WSL** - Skrypt .cmd uruchomiony w WSL zamiast na Windows

## Rozwiązanie krok po kroku

### Metoda 1: Automatyczna (Zalecana)

1. **Otwórz PowerShell lub Command Prompt jako Administrator**
   - Naciśnij `Win + X`
   - Wybierz "Terminal (Administrator)" lub "Windows PowerShell (Administrator)"

2. **Przejdź do katalogu projektu**
   ```cmd
   cd C:\ścieżka\do\AudioRadar\RadarSuite_Final
   ```

3. **Uruchom skrypt budowania**
   ```cmd
   RUN_BUILD_ALL.cmd
   ```

Skrypt automatycznie:
- Sprawdzi Python 3.11
- Utworzy środowisko wirtualne
- Zainstaluje PyInstaller i wszystkie zależności
- Zbuduje aplikację

### Metoda 2: Ręczna instalacja PyInstaller

Jeśli skrypt automatyczny nie działa:

#### Krok 1: Sprawdź wersję Pythona

```cmd
py -3.11 --version
```

Powinieneś zobaczyć: `Python 3.11.x`

Jeśli nie masz Python 3.11:
- Pobierz z https://www.python.org/downloads/
- Podczas instalacji zaznacz **"Add Python to PATH"**

#### Krok 2: Utwórz środowisko wirtualne

```cmd
py -3.11 -m venv .venv
```

#### Krok 3: Aktywuj środowisko wirtualne

```cmd
.venv\Scripts\activate.bat
```

Po aktywacji zobaczysz `(.venv)` na początku linii.

#### Krok 4: Zainstaluj PyInstaller i zależności

```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Lub zainstaluj ręcznie:
```cmd
pip install PyQt5 pyqtgraph PyOpenGL PyOpenGL_accelerate numpy scipy sounddevice soundcard psutil pyinstaller
```

#### Krok 5: Sprawdź instalację PyInstaller

```cmd
pyinstaller --version
```

Powinieneś zobaczyć wersję PyInstaller (np. `6.11.0`).

#### Krok 6: Zbuduj aplikację

```cmd
pyinstaller --clean --noconfirm build_tools\radarsuite.spec
```

#### Krok 7: Uruchom aplikację

```cmd
cd dist\RadarSuite_Final
RadarSuite_Final.exe
```

## Rozwiązywanie problemów

### Błąd: "Python 3.11 is not installed"

**Rozwiązanie:**
1. Pobierz Python 3.11 z https://www.python.org/downloads/
2. Podczas instalacji **KONIECZNIE zaznacz** "Add Python to PATH"
3. Po instalacji uruchom ponownie terminal
4. Sprawdź: `py -3.11 --version`

### Błąd: "PyInstaller not available" (pomimo instalacji)

**Rozwiązanie A - Reaktywuj środowisko:**
```cmd
deactivate
.venv\Scripts\activate.bat
pyinstaller --version
```

**Rozwiązanie B - Zainstaluj ponownie:**
```cmd
pip uninstall pyinstaller
pip install pyinstaller --no-cache-dir
```

**Rozwiązanie C - Użyj modułu Python:**
```cmd
python -m PyInstaller --version
```

Jeśli to działa, edytuj `RUN_BUILD_ALL.cmd` w linii 172:
Zamień: `pyinstaller --version`
Na: `python -m PyInstaller --version`

I w linii 198:
Zamień: `pyinstaller --clean --noconfirm build_tools\radarsuite.spec`
Na: `python -m PyInstaller --clean --noconfirm build_tools\radarsuite.spec`

### Błąd: "Module verification failed"

Oznacza to, że niektóre moduły nie mogą być zaimportowane.

**Rozwiązanie:**
1. Sprawdź logi w `super_log.txt`
2. Zainstaluj Visual C++ Redistributable:
   - Pobierz z: https://aka.ms/vs/17/release/vc_redist.x64.exe
3. Zainstaluj ponownie problematyczne moduły:
   ```cmd
   pip install --force-reinstall --no-cache-dir numpy scipy
   ```

### Błąd: "UpdateResourceW" lub błąd ikony

To problem z plikiem ikony w PyInstaller.

**Rozwiązanie - Tymczasowe:**
Edytuj `build_tools\radarsuite.spec`, znajdź linię:
```python
icon='assets/icon.ico',
```

Zamień na:
```python
icon=None,
```

### Skrypt uruchamia się w WSL zamiast Windows

Jeśli używasz WSL (Windows Subsystem for Linux):

**Rozwiązanie:**
1. Otwórz **Windows Terminal** (nie WSL)
2. Wybierz zakładkę **PowerShell** lub **Command Prompt**
3. Uruchom `RUN_BUILD_ALL.cmd`

Lub przejdź do folderu w Windows Explorer i kliknij dwukrotnie `RUN_BUILD_ALL.cmd`

## Poprawiony skrypt budowania

Jeśli nadal masz problemy, stworzę ulepszoną wersję skryptu:

### RUN_BUILD_FIXED.cmd (nowa wersja)

Zapisz ten skrypt jako `RUN_BUILD_FIXED.cmd` w katalogu `RadarSuite_Final`:

```cmd
@echo off
echo Checking Python installation...

REM Try different Python commands
where py >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py -3.11
    goto :FOUND_PYTHON
)

where python >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto :FOUND_PYTHON
)

echo [ERROR] Python not found!
echo Please install Python 3.11 from https://www.python.org/
pause
exit /b 1

:FOUND_PYTHON
echo Using Python: %PYTHON_CMD%
%PYTHON_CMD% --version

echo.
echo Creating virtual environment...
%PYTHON_CMD% -m venv .venv

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing requirements...
pip install -r requirements.txt

echo.
echo Verifying PyInstaller...
python -m PyInstaller --version
if errorlevel 1 (
    echo [ERROR] PyInstaller not found, installing...
    pip install pyinstaller
)

echo.
echo Building with PyInstaller...
python -m PyInstaller --clean --noconfirm build_tools\radarsuite.spec

if errorlevel 1 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD SUCCESSFUL!
echo ========================================
echo.
echo Location: dist\RadarSuite_Final\RadarSuite_Final.exe
echo.
pause
```

## Wymagania systemowe (Windows 11)

### Wymagane oprogramowanie:
- **Windows 11** 64-bit (wersja 25H2 lub nowsza) ✓ Masz
- **Python 3.11** (pobierz z python.org)
- **Visual C++ Redistributable** (pobierz z Microsoft)

### Opcjonalne:
- **Git for Windows** (jeśli chcesz klonować repozytorium)

## Szybkie sprawdzenie systemu

Uruchom te komendy aby sprawdzić konfigurację:

```cmd
echo === Sprawdzanie Pythona ===
py -3.11 --version
echo.

echo === Sprawdzanie pip ===
py -3.11 -m pip --version
echo.

echo === Sprawdzanie PyInstaller ===
py -3.11 -m PyInstaller --version
echo.

echo === Sprawdzanie zainstalowanych pakietów ===
py -3.11 -m pip list
```

## Najczęstsze błędy i szybkie rozwiązania

| Błąd | Rozwiązanie |
|------|-------------|
| Python 3.11 not found | Zainstaluj Python 3.11 z python.org |
| PyInstaller not available | `pip install pyinstaller` |
| venv creation failed | Uruchom jako Administrator |
| Module import failed | Zainstaluj VC++ Redistributable |
| icon error | Ustaw `icon=None` w .spec |
| Permission denied | Wyłącz antywirus lub dodaj wyjątek |

## Kontakt

Jeśli problem nadal występuje, przygotuj:
1. Wersję Pythona: `py -3.11 --version`
2. Zawartość `super_log.txt`
3. Pełny komunikat błędu
4. Screenshot błędu (opcjonalnie)
