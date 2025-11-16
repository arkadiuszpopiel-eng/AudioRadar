╔══════════════════════════════════════════════════════════════════════════════╗
║                   AUDIO RADAR v11 - PyQt5 Professional Edition                ║
║                  Zaawansowany system detekcji dźwięku z PyQt5                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════════
  OPIS
═══════════════════════════════════════════════════════════════════════════════

Audio Radar to profesjonalny system detekcji i wizualizacji dźwięku z pełnym
interfejsem graficznym PyQt5. Program wykrywa dźwięki chodzenia, biegania i
strzałów z wykrywaniem kierunku i szacowaniem odległości.

═══════════════════════════════════════════════════════════════════════════════
  FUNKCJE
═══════════════════════════════════════════════════════════════════════════════

✓ Zaawansowany interfejs graficzny PyQt5:
  - Przejrzysty układ z zakładkami
  - Panele konfiguracji
  - Przyciski kontrolne
  - Menu i paski narzędzi

✓ Detekcja dźwięków:
  - Chodzenie (wykrywanie kroków)
  - Bieganie (szybsze kroki, wyższa energia)
  - Strzały (gwałtowne szczyty dźwięku)

✓ Śledzenie kierunkowe:
  - Określanie kierunku (0-360°)
  - Szacowanie odległości (w metrach)
  - Wykrywanie zbliżania/oddalania się

✓ Zaawansowana wizualizacja radaru:
  - Radar 360° z oznaczeniami kierunków
  - Kolorowe wskaźniki dla różnych typów dźwięków
  - Wyświetlanie odległości i prędkości
  - Możliwość odłączenia jako osobne okno
  - Regulowana przezroczystość
  - Możliwość zmiany rozmiaru

✓ Analizator widma na żywo:
  - Wizualizacja częstotliwości w czasie rzeczywistym
  - 64 pasma częstotliwości
  - Kolorowy gradient (zielony → żółty → czerwny)
  - Wygładzanie dla płynnego wyświetlania

✓ Zarządzanie urządzeniami audio:
  - Automatyczne wykrywanie urządzeń
  - Wybór urządzenia wejściowego
  - Wyświetlanie szczegółów urządzenia
  - Optymalizacja dla Sound Blaster Z SE

✓ Testy jakości dźwięku:
  - Test poziomu RMS
  - Test szczytu
  - Pomiar poziomu szumów
  - Obliczanie SNR (stosunek sygnału do szumu)
  - Wykrywanie przesterowania

✓ Zarządzanie motywami:
  - Ciemny motyw (domyślny)
  - Jasny motyw
  - Niebieski ciemny motyw
  - Matrix (zielony)

✓ Statystyki:
  - Liczba wykryć
  - Średnia odległość
  - Średnie zaufanie
  - Metryki jakości audio

✓ Kompleksowe logowanie:
  - Log od procesu budowania
  - Log w czasie działania
  - Wszystkie zdarzenia i błędy
  - Eksport logów do pliku

═══════════════════════════════════════════════════════════════════════════════
  INSTALACJA
═══════════════════════════════════════════════════════════════════════════════

1. SZYBKA INSTALACJA (używając RUN_BUILD_ALL.cmd):

   Uruchom plik RUN_BUILD_ALL.cmd - automatycznie zainstaluje wszystkie
   wymagane biblioteki i utworzy archiwum ZIP.

2. RĘCZNA INSTALACJA:

   Wymagany Python 3.7 lub nowszy.

   Zainstaluj wymagane biblioteki:
   pip install -r requirements.txt

   Wymagane biblioteki:
   - numpy (obliczenia numeryczne)
   - scipy (przetwarzanie sygnałów)
   - sounddevice (przechwytywanie dźwięku)
   - PyQt5 (interfejs graficzny)

═══════════════════════════════════════════════════════════════════════════════
  URUCHOMIENIE
═══════════════════════════════════════════════════════════════════════════════

Uruchom program poprzez:

  python main.py

Program otworzy główne okno z interfejsem graficznym.

═══════════════════════════════════════════════════════════════════════════════
  KONFIGURACJA SOUND BLASTER Z SE
═══════════════════════════════════════════════════════════════════════════════

Dla karty Sound Blaster Z SE:

1. Otwórz oprogramowanie Sound Blaster (Creative)
2. Włącz "Stereo Mix" lub "What U Hear"
3. Ustaw jako domyślne urządzenie nagrywające
4. W programie Audio Radar kliknij "Optimize for Sound Blaster Z"

Optymalne ustawienia:
- Częstotliwość próbkowania: 48000 Hz
- Rozmiar bloku: 2048 próbek
- Kanały: 2 (Stereo)

═══════════════════════════════════════════════════════════════════════════════
  UŻYTKOWANIE
═══════════════════════════════════════════════════════════════════════════════

1. WYBÓR URZĄDZENIA AUDIO:
   - Kliknij "Refresh Devices" aby odświeżyć listę urządzeń
   - Wybierz urządzenie wejściowe z listy
   - Sprawdź szczegóły urządzenia

2. TEST JAKOŚCI DŹWIĘKU:
   - Kliknij "Test Audio Quality"
   - Poczekaj 2 sekundy na test
   - Sprawdź wyniki (RMS, SNR, przesterowanie)

3. URUCHOMIENIE DETEKCJI:
   - Kliknij przycisk "Start"
   - Obserwuj radar i analizator widma
   - Sprawdzaj statystyki w zakładce "Statistics"

4. USTAWIENIA DETEKCJI:
   - Włącz/wyłącz typy detekcji (chodzenie, bieganie, strzały)
   - Dostosuj próg zaufania (0-100%)

5. USTAWIENIA RADARU:
   - Zmień przezroczystość (0-100%)
   - Dostosuj czas zanikania (0.5-10s)

6. ODŁĄCZONY RADAR:
   - Menu: View → Detach Radar
   - Przeciągnij okno radaru w dowolne miejsce
   - Zmień rozmiar według potrzeb
   - Ustaw przezroczystość

7. ZMIANA MOTYWU:
   - Wybierz motyw z listy rozwijanej
   - Dostępne motywy: Dark, Light, Blue Dark, Matrix

8. EKSPORT/IMPORT KONFIGURACJI:
   - Menu: File → Export Configuration
   - Menu: File → Import Configuration

═══════════════════════════════════════════════════════════════════════════════
  PLIKI KONFIGURACJI
═══════════════════════════════════════════════════════════════════════════════

config.json - Główny plik konfiguracji
  Zawiera wszystkie ustawienia programu:
  - Konfiguracja audio
  - Ustawienia detekcji
  - Konfiguracja radaru
  - Ustawienia analizatora widma
  - Preferencje UI

log.txt - Plik logów
  Zawiera szczegółowe logi od budowania do działania programu

═══════════════════════════════════════════════════════════════════════════════
  TRYBY DETEKCJI
═══════════════════════════════════════════════════════════════════════════════

CHODZENIE (Walking):
  - Kolor: Zielony
  - Charakterystyka: Umiarkowana energia, 1-3 kroki/s
  - Zakres detekcji: 0-20 metrów

BIEGANIE (Running):
  - Kolor: Pomarańczowy
  - Charakterystyka: Wyższa energia, 3-6 kroków/s
  - Zakres detekcji: 0-30 metrów

STRZAŁY (Shooting):
  - Kolor: Czerwony
  - Charakterystyka: Gwałtowne szczyty, ostry atak
  - Zakres detekcji: 0-100 metrów

═══════════════════════════════════════════════════════════════════════════════
  WSKAŹNIKI NA RADARZE
═══════════════════════════════════════════════════════════════════════════════

- Kółko z promieniowaniem: Wykryty dźwięk
- Linia od centrum: Kierunek dźwięku
- Litera (W/R/S): Typ dźwięku
- Liczba (m): Odległość w metrach
- Strzałka w górę: Zbliżanie się
- Strzałka w dół: Oddalanie się

═══════════════════════════════════════════════════════════════════════════════
  ROZWIĄZYWANIE PROBLEMÓW
═══════════════════════════════════════════════════════════════════════════════

Problem: Brak urządzeń audio
Rozwiązanie:
  - Sprawdź czy karta dźwiękowa jest zainstalowana
  - Zainstaluj sterowniki audio
  - Włącz "Stereo Mix" w ustawieniach Windows

Problem: Niski poziom dźwięku
Rozwiązanie:
  - Zwiększ głośność urządzenia nagrywającego
  - Sprawdź ustawienia "Stereo Mix"
  - Uruchom test jakości audio

Problem: Za dużo fałszywych detekcji
Rozwiązanie:
  - Zwiększ próg zaufania (50-80%)
  - Wyłącz niepotrzebne typy detekcji
  - Sprawdź poziom szumów w teście jakości

Problem: Radar nie wyświetla detekcji
Rozwiązanie:
  - Sprawdź czy detekcja jest włączona
  - Sprawdź czy odpowiednie typy są aktywne
  - Sprawdź logi w zakładce "Log"

Problem: Aplikacja się nie uruchamia
Rozwiązanie:
  - Sprawdź czy wszystkie biblioteki są zainstalowane
  - Uruchom ponownie RUN_BUILD_ALL.cmd
  - Sprawdź log.txt dla szczegółów błędu

═══════════════════════════════════════════════════════════════════════════════
  STRUKTURA PLIKÓW
═══════════════════════════════════════════════════════════════════════════════

main.py                     - Główny punkt wejścia aplikacji
audio_radar_gui.py          - Główny interfejs graficzny
radar_widget.py             - Widget wizualizacji radaru
spectrum_analyzer.py        - Widget analizatora widma
audio_manager.py            - Zarządzanie urządzeniami i przechwytywaniem audio
sound_detector.py           - Detekcja i klasyfikacja dźwięków
config_manager.py           - Zarządzanie konfiguracją
theme_manager.py            - Zarządzanie motywami
logger.py                   - System logowania
requirements.txt            - Lista wymaganych bibliotek
config.json                 - Plik konfiguracji (tworzony automatycznie)
log.txt                     - Plik logów (tworzony automatycznie)
README_PL.txt               - Ten plik
RUN_BUILD_ALL.cmd           - Skrypt budowania i pakowania

═══════════════════════════════════════════════════════════════════════════════
  SKRÓTY KLAWISZOWE
═══════════════════════════════════════════════════════════════════════════════

(w głównym oknie)
  Ctrl+Q  - Zamknij aplikację
  F5      - Odśwież listę urządzeń

(w odłączonym radarze)
  Przeciągnij lewym przyciskiem myszy - Przenieś okno

═══════════════════════════════════════════════════════════════════════════════
  WYMAGANIA SYSTEMOWE
═══════════════════════════════════════════════════════════════════════════════

Minimalne:
  - Windows 7/10/11 (64-bit)
  - Python 3.7+
  - 2 GB RAM
  - Karta dźwiękowa
  - Procesor: Dual-core 2.0 GHz

Zalecane:
  - Windows 10/11 (64-bit)
  - Python 3.9+
  - 4 GB RAM
  - Sound Blaster Z SE lub lepsza
  - Procesor: Quad-core 3.0 GHz

═══════════════════════════════════════════════════════════════════════════════
  LICENCJA I INFORMACJE
═══════════════════════════════════════════════════════════════════════════════

Audio Radar v11 - PyQt5 Professional Edition
Copyright © 2024 Audio Radar Project

Wersja: 11.0
Data wydania: 2024
Status: Wydanie produkcyjne

═══════════════════════════════════════════════════════════════════════════════
  WSPARCIE
═══════════════════════════════════════════════════════════════════════════════

W razie problemów:
1. Sprawdź plik log.txt
2. Sprawdź sekcję "Rozwiązywanie problemów" powyżej
3. Uruchom test jakości audio
4. Sprawdź konfigurację urządzenia

Wszystkie logi są zapisywane w pliku log.txt z pełnymi informacjami
o działaniu programu od momentu budowania do zamknięcia.

═══════════════════════════════════════════════════════════════════════════════

                    Dziękujemy za użycie Audio Radar v11!

═══════════════════════════════════════════════════════════════════════════════
