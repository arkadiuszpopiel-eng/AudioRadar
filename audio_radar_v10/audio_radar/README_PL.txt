═══════════════════════════════════════════════════════════════
                    AUDIO RADAR v10.1
                     Radar Dźwiękowy
═══════════════════════════════════════════════════════════════

OPIS
═══════════════════════════════════════════════════════════════

Audio Radar to aplikacja dla Windows, która w czasie rzeczywistym
monitoruje dźwięk z gry i wizualizuje kierunek kroków i strzałów.
Program przechwytuje audio przez loopback (Stereo Mix) i wykrywa
zdarzenia dźwiękowe, wyświetlając je na radarze 2D.

NOWOŚCI W WERSJI 10.1
═══════════════════════════════════════════════════════════════

✓ Narzędzie testowania audio (klawisz T)
✓ Miernik poziomu VU (wyświetla RMS i Peak na żywo)
✓ Rzeczywiste obliczenie opóźnienia (latencja)
✓ Tryb debugowania (klawisz D)
✓ Zamykanie przez ESC
✓ Ulepszona diagnostyka audio

WYMAGANIA
═══════════════════════════════════════════════════════════════

• Windows 11 (lub Windows 10)
• Python 3.8 lub nowszy
• Biblioteki:
  - sounddevice
  - pygame
  - numpy
• Karta dźwiękowa z obsługą loopback (np. Sound Blaster Z SE)

INSTALACJA
═══════════════════════════════════════════════════════════════

1. Rozpakuj archiwum do wybranego folderu

2. Zainstaluj zależności:
   pip install sounddevice pygame numpy

3. Skonfiguruj loopback:
   - Otwórz Ustawienia Dźwięku Windows
   - Włącz "Stereo Mix" lub "What U Hear"
   - Ustaw jako domyślne urządzenie nagrywające

4. Uruchom program:
   python -m audio_radar
   
   lub:
   
   cd audio_radar
   python main.py

PIERWSZE URUCHOMIENIE
═══════════════════════════════════════════════════════════════

1. Uruchom program
2. Zobaczysz okno radaru (czarne tło, szare kontury)
3. Naciśnij T aby otworzyć TEST audio
4. Włącz muzykę/grę i sprawdź poziomy
5. Jeśli poziomy są OK, zamknij test i graj

TESTOWANIE AUDIO (KLAWISZ T)
═══════════════════════════════════════════════════════════════

PROBLEM: Radar nie wykrywa dźwięków?

ROZWIĄZANIE: Użyj narzędzia TEST:

1. W głównym oknie naciśnij T
2. Odtwórz coś GŁOŚNO (muzyka, gra, video)
3. Obserwuj poziomy:
   - RMS: średnia głośność
   - Peak: maksymalne szczyty
   - Wykrycia: ile eventów przekroczyło próg

INTERPRETACJA WYNIKÓW:

✓ Peak > 0.1: Silny sygnał - wszystko OK
⚠ Peak 0.01-0.1: Słaby sygnał - zwiększ volume
✗ Peak < 0.01: Prawie zero - sprawdź:
  • Czy wybrane urządzenie to loopback?
  • Czy coś naprawdę gra w systemie?
  • Czy volume nie jest zmutowany?

PRÓG DETEKCJI:
- Domyślnie: 0.05
- Jeśli za mało wykryć → zmniejsz próg w sound_analysis.py
- Jeśli za dużo fałszywych alarmów → zwiększ próg

STEROWNIE
═══════════════════════════════════════════════════════════════

KLAWISZE GŁÓWNE:
  T       - Otwórz okno testowania audio
  D       - Włącz/wyłącz tryb debugowania
  ESC     - Zamknij program

DOSTOSOWANIE WIZUALIZACJI:
  Z / X   - Zmniejsz / zwiększ szerokość pasków
  C / V   - Zmniejsz / zwiększ wysokość pasków
  B / N   - Zmniejsz / zwiększ przezroczystość

ELEMENTY INTERFEJSU
═══════════════════════════════════════════════════════════════

Górny lewy róg:
  VU Meter - Pokazuje bieżący poziom audio
  • Zielony pasek = RMS (średni poziom)
  • Żółty pasek = Peak (szczyt)

Dolny prawy róg:
  Latencja - Rzeczywiste opóźnienie w milisekundach
  Wersja - Numer wersji programu

Tryb Debug (klawisz D):
  Wyświetla statystyki wykrywania w czasie rzeczywistym

KONFIGURACJA
═══════════════════════════════════════════════════════════════

Plik config.json zawiera ustawienia:

{
  "input_device": null,      // null = domyślne urządzenie
  "output_device": null,     // Zarezerwowane
  "bar_width": 40,           // Szerokość pasków
  "bar_height": 200,         // Wysokość pasków
  "transparency": 180        // Przezroczystość (0-255)
}

WYBÓR URZĄDZENIA AUDIO:

1. Wylistuj dostępne urządzenia:
   python main.py --list-devices

2. Skopiuj numer urządzenia loopback

3. Edytuj config.json:
   "input_device": 5

4. Uruchom ponownie program

WYKRYWANIE ZDARZEŃ
═══════════════════════════════════════════════════════════════

Program wykrywa dwa typy zdarzeń:

KROKI (zielone):
  • Wyświetlane na górze radaru (0°)
  • Wykrywane przez średnią wariancję sygnału
  • Próg: FOOTSTEP_STD_THRESHOLD = 0.05

STRZAŁY (czerwone):
  • Wyświetlane na dole radaru (180°)
  • Wykrywane przez ostre szczyty
  • Próg: SHOT_PEAK_THRESHOLD = 0.6

DOSTOSOWANIE PROGÓW:

Edytuj sound_analysis.py:

SHOT_PEAK_THRESHOLD = 0.6      # Zwiększ jeśli za dużo strzałów
FOOTSTEP_STD_THRESHOLD = 0.05  # Zmniejsz jeśli brak kroków

ROZWIĄZYWANIE PROBLEMÓW
═══════════════════════════════════════════════════════════════

PROBLEM: Program się nie uruchamia

ROZWIĄZANIE:
  • Sprawdź czy Python 3.8+ jest zainstalowany
  • Zainstaluj brakujące biblioteki: pip install -r requirements.txt
  • Sprawdź logi w pliku log_v10.1.txt

PROBLEM: Brak wykrywania dźwięków

ROZWIĄZANIE:
  1. Naciśnij T aby otworzyć test audio
  2. Sprawdź czy poziomy się zmieniają
  3. Jeśli zero sygnału:
     • Sprawdź czy loopback jest włączony
     • Sprawdź czy loopback jest domyślnym urządzeniem nagrywającym
     • Sprawdź volume systemowy
  4. Jeśli sygnał jest słaby:
     • Zwiększ głośność systemową
     • Zmniejsz próg w sound_analysis.py

PROBLEM: Za dużo fałszywych alarmów

ROZWIĄZANIE:
  • Włącz tryb debug (D) aby zobaczyć co jest wykrywane
  • Zwiększ progi w sound_analysis.py
  • Sprawdź czy używasz właściwego urządzenia loopback

PROBLEM: Opóźnienie jest zbyt duże

ROZWIĄZANIE:
  • Zmniejsz blocksize w main.py (linia 197):
    blocksize = 512  # zamiast 1024
  • Mniejszy bufor = mniejsze opóźnienie, ale więcej CPU

PROBLEM: Wysokie użycie CPU

ROZWIĄZANIE:
  • Zwiększ blocksize w main.py
  • Zamknij tryb debug (D)
  • Zmniejsz FPS w visualization.py (linia 360)

PLIKI I STRUKTURA
═══════════════════════════════════════════════════════════════

audio_radar/
├── __init__.py              - Inicjalizacja pakietu
├── __main__.py              - Punkt wejścia (python -m audio_radar)
├── main.py                  - Główny moduł aplikacji
├── audio_capture.py         - Przechwytywanie audio (sounddevice)
├── sound_analysis.py        - Detekcja zdarzeń
├── visualization.py         - Radar 2D (Pygame)
├── audio_test_window.py     - Okno testowania audio
├── config.json              - Konfiguracja użytkownika
├── VERSION.txt              - Wersja programu
├── README_PL.txt            - Ta dokumentacja
├── CHANGELOG.txt            - Historia zmian
└── log_v10.1.txt            - Logi runtime (tworzony automatycznie)

LOGI
═══════════════════════════════════════════════════════════════

Program automatycznie zapisuje logi do pliku log_v10.1.txt w folderze
audio_radar. W logach znajdziesz:

• Czas startu i wersję
• Użytą konfigurację
• Wykryte zdarzenia (kroki, strzały)
• Błędy i ostrzeżenia

Aby zobaczyć więcej szczegółów, włącz tryb debug (klawisz D).

WSPARCIE I ROZWÓJ
═══════════════════════════════════════════════════════════════

GitHub: https://github.com/arkadiuszpopiel-eng/AudioRadar
Issues: Zgłaszaj problemy na GitHub Issues
Version: v10.1
Date: 2025-11-09

LICENCJA
═══════════════════════════════════════════════════════════════

Ten projekt jest open source. Możesz go dowolnie modyfikować
i używać do celów osobistych i komercyjnych.

PODZIĘKOWANIA
═══════════════════════════════════════════════════════════════

Projekt stworzony z pomocą AI (OpenAI GPT) na podstawie wymagań
użytkownika. Dziękujemy społeczności open source za biblioteki
sounddevice, pygame i numpy.

═══════════════════════════════════════════════════════════════
                     MIŁEJ ZABAWY!
═══════════════════════════════════════════════════════════════
