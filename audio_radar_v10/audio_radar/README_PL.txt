╔═══════════════════════════════════════════════════════════════════════════╗
║                      AudioRadar v10.0 - Optimized Core                    ║
║                     System wykrywania dźwięków w grach                    ║
╚═══════════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════
  ✨ CO NOWEGO W v10.0
═══════════════════════════════════════════════════════════════════════════

🎯 GŁÓWNE USPRAWNIENIA:

1. Nowy nowoczesny interfejs PyQt5
   ✓ Ciemny motyw z cyjanowymi akcentami (#0d7377)
   ✓ Płynna animacja 60 FPS (16ms odświeżanie)
   ✓ Responsywny layout 1200x700px
   ✓ Pasek stanu z live monitoringiem

2. Zoptymalizowany backend audio
   ✓ Domyślny bufor: 128 ramek (było 256)
   ✓ Opóźnienie: ~10ms przy 48kHz (było ~20ms)
   ✓ Priorytet wątku: TIME_CRITICAL
   ✓ Lepsza wydajność pop_latest()

3. Monitoring wydajności w czasie rzeczywistym
   ✓ Śledzenie opóźnień (historia 300 próbek)
   ✓ Monitorowanie CPU przez psutil
   ✓ Licznik porzuconych próbek audio
   ✓ Eksport statystyk do CSV

4. Skróty klawiszowe
   ✓ SPACJA - START/STOP przechwytywania
   ✓ F5 - Odświeżenie listy urządzeń

═══════════════════════════════════════════════════════════════════════════
  📦 INSTALACJA
═══════════════════════════════════════════════════════════════════════════

WYMAGANIA:
- Windows 10/11
- Python 3.11 lub nowszy
- Karta dźwiękowa z obsługą loopback (np. Sound Blaster Z SE)

KROK 1: Instalacja Pythona
---------------------------
1. Pobierz Python 3.11+ z python.org
2. Podczas instalacji zaznacz "Add Python to PATH"
3. Sprawdź instalację: python --version

KROK 2: Instalacja zależności
-----------------------------
Otwórz wiersz poleceń w katalogu audio_radar i wykonaj:

    pip install -r requirements.txt

Lub ręcznie:

    pip install PyQt5 pyaudiowpatch numpy scipy psutil

KROK 3: Konfiguracja audio
---------------------------
1. Otwórz Panel sterowania → Dźwięk
2. Zakładka "Nagrywanie"
3. Kliknij prawym na puste miejsce → "Pokaż wyłączone urządzenia"
4. Znajdź "Stereo Mix" lub "What U Hear"
5. Włącz i ustaw jako domyślne urządzenie nagrywające

═══════════════════════════════════════════════════════════════════════════
  🚀 SZYBKI START
═══════════════════════════════════════════════════════════════════════════

URUCHOMIENIE Z MODUŁU:
    python -m audio_radar

URUCHOMIENIE ZE SKRYPTU:
    python main.py

URUCHOMIENIE Z BAT (jeśli istnieje):
    START_HERE.bat

PIERWSZE URUCHOMIENIE:
1. Uruchom aplikację
2. Naciśnij F5 aby odświeżyć listę urządzeń
3. Wybierz urządzenie loopback (oznaczone 🔄 [LOOPBACK])
4. Ustaw parametry:
   - Częstotliwość: 48000 Hz (zalecane)
   - Bufor: 128 ramek (optymalne dla niskiego opóźnienia)
5. Naciśnij SPACJA lub przycisk START
6. Status LED powinien zmienić się na 🟢 Połączono
7. Obserwuj wskaźniki opóźnienia i CPU w pasku stanu

═══════════════════════════════════════════════════════════════════════════
  🎮 UŻYTKOWANIE
═══════════════════════════════════════════════════════════════════════════

WYBÓR URZĄDZENIA:
- Dla przechwytywania dźwięku z gry: wybierz LOOPBACK
- Dla mikrofonu: wybierz standardowe urządzenie wejściowe

PARAMETRY AUDIO:
- Częstotliwość próbkowania:
  * 48000 Hz - zalecane dla większości gier
  * 44100 Hz - alternatywa dla starszych gier
  * 96000 Hz - dla systemów high-end (więcej CPU)

- Rozmiar bufora:
  * 64 ramki - minimalne opóźnienie, wysokie CPU
  * 128 ramek - ZALECANE (~10ms @ 48kHz)
  * 256 ramek - większa stabilność, większe opóźnienie
  * 512+ ramek - dla słabych komputerów

WSKAŹNIKI WYDAJNOŚCI:
- LED Status: 🟢 połączono / 🔴 rozłączono / 🟡 ostrzeżenie
- Opóźnienie: Czas między dźwiękiem a jego przetworzeniem
- CPU: Użycie procesora przez aplikację

SKRÓTY KLAWISZOWE:
- SPACJA: Włącz/wyłącz przechwytywanie
- F5: Odśwież listę urządzeń
- ALT+F4: Zamknij aplikację

═══════════════════════════════════════════════════════════════════════════
  🔧 ROZWIĄZYWANIE PROBLEMÓW
═══════════════════════════════════════════════════════════════════════════

PROBLEM: Brak urządzeń loopback
ROZWIĄZANIE:
1. Sprawdź czy karta dźwiękowa obsługuje Stereo Mix
2. W Panelu sterowania → Dźwięk → Nagrywanie
3. PPM → Pokaż wyłączone urządzenia
4. Włącz "Stereo Mix" lub "What U Hear"

PROBLEM: Wysokie użycie CPU
ROZWIĄZANIE:
1. Zwiększ rozmiar bufora (256 lub 512 ramek)
2. Zmniejsz częstotliwość próbkowania (44100 Hz)
3. Zamknij inne aplikacje audio
4. Sprawdź sterowniki karty dźwiękowej

PROBLEM: Błąd uruchamiania GUI
ROZWIĄZANIE:
1. Upewnij się że PyQt5 jest zainstalowane: pip install PyQt5
2. Sprawdź logi w pliku: log_v10.txt
3. Spróbuj wersji pygame (automatyczny fallback)

PROBLEM: Nie wykrywa dźwięków
ROZWIĄZANIE:
1. Sprawdź czy gra odtwarza dźwięk
2. Sprawdź czy loopback jest uruchomiony
3. Zwiększ głośność w grze
4. Sprawdź czy wybrano właściwe urządzenie

PROBLEM: Porzucone próbki audio (dropouts)
ROZWIĄZANIE:
1. Zwiększ rozmiar bufora
2. Zamknij aplikacje w tle
3. Sprawdź obciążenie systemu
4. Zaktualizuj sterowniki audio

═══════════════════════════════════════════════════════════════════════════
  📊 METRYKI WYDAJNOŚCI
═══════════════════════════════════════════════════════════════════════════

PORÓWNANIE v9.9.32 vs v10.0:

┌─────────────────────┬─────────────┬─────────────┐
│ Parametr            │ v9.9.32     │ v10.0       │
├─────────────────────┼─────────────┼─────────────┤
│ Domyślny bufor      │ 256 ramek   │ 128 ramek   │
│ Opóźnienie @ 48kHz  │ ~20ms       │ ~10ms       │
│ FPS interfejsu      │ ~20 FPS     │ ~60 FPS     │
│ Użycie CPU          │ 5-8%        │ 3-5%        │
│ Framework GUI       │ pygame      │ PyQt5       │
│ Monitoring wydajn.  │ brak        │ TAK         │
│ Skróty klawiszowe   │ brak        │ TAK         │
│ Ciemny motyw        │ brak        │ TAK         │
└─────────────────────┴─────────────┴─────────────┘

OCZEKIWANE WARTOŚCI:
- Opóźnienie: 8-15ms (128 ramek @ 48kHz)
- CPU: 3-7% w zależności od systemu
- RAM: ~50-100MB
- FPS: stałe 60 FPS

═══════════════════════════════════════════════════════════════════════════
  🗺️ ROADMAP - PLANOWANE FUNKCJE
═══════════════════════════════════════════════════════════════════════════

FAZA B (v10.1) - Wykrywanie dźwięków
□ Detekcja transjentów (piki energii)
□ Filtrowanie pasmowe 2-8 kHz (kroki)
□ Klasyfikacja heurystyczna krok/strzał
□ Podstawowa wizualizacja kierunków

FAZA C (v10.2) - Lokalizacja przestrzenna
□ Analiza wielokanałowa (stereo, 5.1, 7.1)
□ Mapowanie kierunków 0-360°
□ Interpolacja między kanałami
□ Radar 2D z płynnymi markerami

FAZA D (v10.3) - Zaawansowane DSP
□ Kompresor dynamiki
□ Redukcja szumów (RNNoise)
□ Adaptacyjne progi detekcji
□ Estymacja odległości

FAZA E (v10.4) - Machine Learning
□ Model CNN do klasyfikacji
□ Trening na próbkach z gier
□ Rozpoznawanie typów broni
□ Profil dla różnych gier

═══════════════════════════════════════════════════════════════════════════
  📝 STRUKTURA PLIKÓW
═══════════════════════════════════════════════════════════════════════════

audio_radar/
├── __init__.py              - Inicjalizacja pakietu
├── __main__.py              - Punkt wejścia v10.0 (PyQt5)
├── main.py                  - Legacy punkt wejścia (pygame)
├── gui.py                   - Główne okno PyQt5
├── theme_manager.py         - System motywów
├── performance_monitor.py   - Monitoring wydajności
├── audio_backends.py        - Backend audio (PyAudio/WASAPI)
├── audio_capture.py         - Legacy capture (sounddevice)
├── sound_analysis.py        - Analiza sygnału
├── visualization.py         - Legacy wizualizacja (pygame)
├── requirements.txt         - Zależności Pythona
├── README_PL.txt            - Ta dokumentacja
├── CHANGELOG.txt            - Historia zmian
├── config.json              - Konfiguracja użytkownika
├── log_v10.txt              - Logi v10.0
└── VERSION.txt              - Wersja aplikacji

portable/
└── settings.json            - Domyślne ustawienia

═══════════════════════════════════════════════════════════════════════════
  ℹ️ INFORMACJE DODATKOWE
═══════════════════════════════════════════════════════════════════════════

PROJEKT: AudioRadar
WERSJA: 10.0 "Optimized Core"
AUTOR: Arkadiusz Popiel
LICENCJA: Proprietary
JĘZYK: Python 3.11+
PLATFORMA: Windows 10/11

WSPARCIE:
- GitHub: arkadiuszpopiel-eng/AudioRadar
- Logi: log_v10.txt
- Email: [kontakt przez GitHub]

PODZIĘKOWANIA:
- Społeczność Python
- Twórcy PyQt5, PyAudio, NumPy
- Testerzy i użytkownicy feedback

═══════════════════════════════════════════════════════════════════════════
  📄 UWAGI PRAWNE
═══════════════════════════════════════════════════════════════════════════

AudioRadar jest narzędziem pomocniczym do gier. Użytkownicy są odpowiedzialni
za zgodność z regulaminami gier, w których używają tego oprogramowania.

Autor nie ponosi odpowiedzialności za:
- Bany lub kary w grach online
- Uszkodzenie sprzętu przez niewłaściwe ustawienia
- Utratę danych
- Jakiekolwiek inne szkody wynikłe z użycia oprogramowania

Używaj na własną odpowiedzialność.

═══════════════════════════════════════════════════════════════════════════

                        Dziękujemy za używanie AudioRadar v10.0!
                              Miłej zabawy w grach! 🎮

═══════════════════════════════════════════════════════════════════════════
