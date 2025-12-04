================================================================================
 RADARSUITE - ARCHIWUM STARYCH WERSJI I PROTOTYPÓW
================================================================================

Data archiwizacji: 2025-11-29

================================================================================
 INFORMACJE OGÓLNE
================================================================================

Ten katalog zawiera STARE, NIEAKTUALNE wersje projektu RadarSuite oraz
wcześniejsze prototypy i eksperymenty. Katalogi znajdujące się tutaj:

- NIE są już aktywnie rozwijane
- SĄ zachowane TYLKO jako archiwum/historia projektu
- NIE powinny być używane do nowych prac rozwojowych

================================================================================
 AKTUALNE WERSJE PRODUKCYJNE (POZA TYM KATALOGIEM)
================================================================================

Wszystkie nowe prace nad projektem RadarSuite powinny być prowadzone
WYŁĄCZNIE w następujących katalogach:

WINDOWS:
  - RadarSuite_Windows_V4.0  (wersja bazowa)
  - RadarSuite_Windows_V4.1  (wersja rozszerzona)
  - RadarSuite_Windows_V4.2  (najnowsza - do utworzenia)

LINUX:
  - RadarSuite_Linux_V4.0    (wersja bazowa)
  - RadarSuite_Linux_V4.1    (wersja rozszerzona)
  - RadarSuite_Linux_V4.2    (najnowsza - do utworzenia)

HIERARCHIA ROZWOJU:
  Priorytet: V4.2 → V4.1 → V4.0
  - Nowe funkcje i poprawki najpierw w V4.2
  - Backport do V4.1 i V4.0 tylko gdy to sensowne

================================================================================
 ZAWARTOŚĆ ARCHIWUM
================================================================================

1. RadarSuite_Final_V4/
   - Stara wersja (v3.5.0) która próbowała budować dla obu platform
     z jednego katalogu
   - Problem: mieszanie build artifacts, 144 ostrzeżenia podczas builda
   - Zastąpiona przez: osobne katalogi RadarSuite_Windows_V4.x i
     RadarSuite_Linux_V4.x
   - Status: PRZESTARZAŁA - zachowana dla referencji

2. audio_radar_v9/
   - Wczesny prototyp projektu AudioRadar
   - Podstawowa funkcjonalność: audio capture, sound analysis, visualization
   - Wersja z main.py VERSION = "v9"
   - Status: PROTOTYP - zastąpiony przez RadarSuite V4.x

3. audio_radar_v10/
   - Kolejny prototyp projektu AudioRadar
   - Ulepszenia względem v9
   - Wersja z main.py VERSION = "v10"
   - Status: PROTOTYP - zastąpiony przez RadarSuite V4.x

4. ARC_FPS_PersonDetector_v9_5_1_FULL A/
   - Eksperymentalny prototyp detektora osób dla gier FPS
   - Wersja testowa z Arc Raiders
   - Status: EKSPERYMENT - nieutrzymywany

================================================================================
 UWAGI TECHNICZNE
================================================================================

- Prototypy audio_radar_v9 i v10 używały prostszej architektury
  (PyGame, sounddevice, basic event detection)

- RadarSuite_Final_V4 była próbą unifikacji, ale miała problemy:
  * Mieszanie artifacts Windows/Linux
  * Konflikty w logach
  * Trudności w debugowaniu platform-specific issues

- RadarSuite V4.x (aktualne wersje) rozwiązują te problemy poprzez:
  * Oddzielne katalogi dla każdej platformy
  * Dedykowane spec files PyInstaller
  * Zoptymalizowane requirements
  * Czyste logi buildów

================================================================================
 CO ROBIĆ Z TYM ARCHIWUM?
================================================================================

✅ DOZWOLONE:
  - Przeglądanie kodu dla referencji historycznej
  - Porównywanie starych implementacji z nowymi
  - Ekstrakcja pomysłów/rozwiązań do backportu do V4.x

❌ NIE ROBIĆ:
  - Rozwijanie kodu w tych katalogach
  - Tworzenie nowych feature'ów na bazie starych wersji
  - Commitowanie zmian do tych katalogów
  - Używanie jako bazy dla nowych projektów

================================================================================
 HISTORIA WERSJI
================================================================================

audio_radar_v9          → Pierwszy prototyp (data nieznana)
audio_radar_v10         → Drugi prototyp (data nieznana)
ARC_FPS_PersonDetector  → Eksperyment Arc Raiders (v9.5.1)
RadarSuite_Final_V4     → Unified build attempt (v3.5.0, ~2025-11-19)
RadarSuite V4.0         → Split Windows/Linux (v4.0.0, 2025-11-19)
RadarSuite V4.1         → Enhanced version (v4.1.x, 2025-11-xx)
RadarSuite V4.2         → Latest version (planowana)

================================================================================
 KONTAKT / WSPARCIE
================================================================================

W przypadku pytań dotyczących aktualnych wersji RadarSuite V4.x:
  - Windows: Zobacz RadarSuite_Windows_V4.x/README_WINDOWS_V4.md
  - Linux:   Zobacz RadarSuite_Linux_V4.x/README_LINUX_V4.md
  - Ogólne:  Zobacz RADARSUITE_V4_README.md (katalog główny)

W przypadku pytań o historię projektu i stare wersje:
  - Sprawdź commity w git log
  - Przejrzyj pliki w tym archiwum

================================================================================
 PODSUMOWANIE
================================================================================

To archiwum służy WYŁĄCZNIE jako backup historyczny.

Wszystkie nowe prace: RadarSuite_Windows_V4.x i RadarSuite_Linux_V4.x

Priorytet rozwoju: V4.2 (najnowsza) → V4.1 → V4.0

================================================================================
Koniec dokumentu
================================================================================
