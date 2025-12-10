# Radar Games ML v4.3 — Raport naprawy

## Wykryte błędy
- **PyInstaller / python311.dll** – plik wykonywalny kopiowany do katalogu głównego bez folderu `_internal`, co skutkowało komunikatem „Failed to load Python DLL …\_internal\python311.dll”.
- **Fałszywe "EXE not found"** – niespójność nazw katalogów dist (`RGML` vs `Radar_Games_ML`) powodowała, że walidacja po buildzie raportowała brak pliku mimo udanej kompilacji.
- **UI ML (UnboundLocalError)** – w `app/ui/builder.py` zmienna `ML_TRAINING_ERROR_TRACE` była nadpisywana lokalnie przy inicjalizacji kontrolera, przez co ścieżka błędu skutkowała wyjątkiem podczas budowania zakładki ML Training.

## Wprowadzone zmiany
- Ujednolicono katalogi `logs/` i `reports/` oraz dodano centralne ścieżki w `app/core/paths.py` wraz z kopiowaniem dziedziczonych logów.
- Rozszerzono logger o osobny plik `runtime.log` i zaktualizowano logowanie startu aplikacji (`app/core/logger.py`, `app/main.py`).
- Zabezpieczono zakładkę ML Training przed błędami inicjalizacji, dodając spójne komunikaty i śledzenie trace (`app/ui/builder.py`).
- Uspójniono build PyInstaller: katalog dist `Radar_Games_ML`, kopiowanie `_internal` i python311.dll, pełne logowanie do `logs/build_windows.log`, automatyczna weryfikacja artefaktów (`build_tools/radar_games_ml.spec`, `build_windows.py`).
- Dodano skrypty diagnostyczne: `run_diagnostics.py` (uruchomienie UI w trybie offscreen) oraz `verify_build.py` (kontrola dist, `_internal`, python311.dll, Qt DLL) wraz z raportami w `reports/`.

## Instrukcja: uruchamianie z kodu
1. Stwórz i aktywuj wirtualne środowisko (Windows):
   ```bat
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Zainstaluj zależności:
   ```bat
   pip install -r requirements-windows.txt
   ```
3. Uruchom aplikację w trybie developerskim:
   ```bat
   python main.py
   ```
4. Logi znajdziesz w `logs/runtime.log` oraz `logs/super_log.txt`.

## Instrukcja: build EXE
1. Upewnij się, że aktywne jest to samo środowisko wirtualne i zainstalowany jest PyInstaller.
2. Uruchom build:
   ```bat
   python build_windows.py
   ```
3. Wyniki:
   - Log: `logs/build_windows.log`
   - Raport: `reports/build_report.txt`
   - Artefakty: `dist/Radar_Games_ML/` (wraz z `_internal`) oraz kopia w katalogu głównym (`Radar_Games_ML.exe` + `_internal`).
4. Walidacja powinna zakończyć się komunikatem `SUCCESS: All critical artifacts present.`

## Testy automatyczne
- `python run_diagnostics.py` – szybki start UI w trybie offscreen, raport w `logs/diagnostics.log`.
- `python verify_build.py` – weryfikacja artefaktów PyInstaller, raport w `reports/build_report.txt`.
