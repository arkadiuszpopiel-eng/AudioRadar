═══════════════════════════════════════════════════════════════
AudioRadar v10.0 - README PL
═══════════════════════════════════════════════════════════════

OPIS:
AudioRadar to aplikacja monitorująca dźwięk w czasie rzeczywistym,
wykrywająca określone zdarzenia dźwiękowe (kroki, strzały) i 
wyświetlająca nakładkę kierunkową pomagającą zlokalizować źródło.

WYMAGANIA:
- Python 3.8 lub nowszy
- PyQt5 (nowoczesny interfejs GUI)
- sounddevice (przechwytywanie audio)
- numpy (przetwarzanie sygnału)
- pygame (wizualizacja)
- psutil (monitoring wydajności)

INSTALACJA:
1. Wypakuj archiwum do odpowiedniego folderu
2. Otwórz PowerShell lub Wiersz poleceń w tym folderze
3. Uruchom START_V10_GUI.bat (automatycznie zainstaluje zależności)

URUCHAMIANIE:
- Dwukrotnie kliknij: START_V10_GUI.bat
- LUB w PowerShell/CMD: python main.py
- LUB uruchom: python START_V10_GUI.py

SKRÓTY KLAWISZOWE:
- SPACE: START/STOP monitorowania
- F5: Odśwież listę urządzeń

═══════════════════════════════════════════════════════════════
ROZWIĄZYWANIE PROBLEMÓW - GUI
═══════════════════════════════════════════════════════════════

PROBLEM: Czarny ekran z radarem zamiast GUI
ROZWIĄZANIE:
  1. Upewnij się że masz PyQt5:
     pip install PyQt5
  
  2. Uruchom przez launcher:
     START_V10_GUI.bat
  
  3. LUB bezpośrednio:
     python START_V10_GUI.py
  
  4. LUB napraw main.py:
     - Zamień zawartość main.py według instrukcji w CHANGELOG.txt

PROBLEM: "No module named audio_radar"
ROZWIĄZANIE:
  - Upewnij się że jesteś w folderze audio_radar/
  - Uruchom: python main.py (nie python -m audio_radar)

PROBLEM: Program się zamyka natychmiast
ROZWIĄZANIE:
  - Sprawdź logi: type log_v10.txt
  - Sprawdź czy PyQt5 jest zainstalowany: python -c "import PyQt5"
  - Uruchom przez CMD/PowerShell aby zobaczyć błędy

PROBLEM: Brak urządzeń audio
ROZWIĄZANIE:
  - Sprawdź czy masz włączone "Stereo Mix" lub "What U Hear"
  - Ustaw loopback jako domyślne urządzenie nagrywania
  - Uruchom: python main.py --list-devices (w starym trybie)

PROBLEM: Wysokie użycie CPU
ROZWIĄZANIE:
  - Zmniejsz blocksize w audio_capture.py
  - Zamknij inne aplikacje audio
  - Sprawdź monitoring w statusbar GUI

═══════════════════════════════════════════════════════════════
KONFIGURACJA ZAAWANSOWANA
═══════════════════════════════════════════════════════════════

Plik config.json (opcjonalny):
{
  "input_device": null,    // indeks urządzenia lub null (domyślne)
  "output_device": null,   // zarezerwowane na przyszłość
  "bar_width": 40,         // szerokość pasków radaru
  "bar_height": 200,       // wysokość pasków radaru
  "transparency": 180      // przezroczystość (0-255)
}

Aby znaleźć indeks urządzenia:
python -c "from audio_capture import list_audio_input_devices; print(list_audio_input_devices())"

═══════════════════════════════════════════════════════════════
LOGI I DEBUGGING
═══════════════════════════════════════════════════════════════

Logi zapisywane są w: audio_radar/log_v10.txt

Sprawdź logi:
- Windows: type log_v10.txt
- Linux/Mac: cat log_v10.txt

Poziomy logowania:
- INFO: normalne operacje
- WARNING: ostrzeżenia (np. brak urządzeń)
- ERROR: błędy (np. błąd inicjalizacji audio)

═══════════════════════════════════════════════════════════════
WSPARCIE I ROZWÓJ
═══════════════════════════════════════════════════════════════

Ten projekt został wygenerowany przez ChatGPT OpenAI na podstawie
wymagań użytkownika. Możesz swobodnie modyfikować i rozszerzać
go według własnych potrzeb.

Algorytmy detekcji znajdują się w: sound_analysis.py
Interfejs GUI w: gui.py
Motyw ciemny w: theme_manager.py
Przechwytywanie audio w: audio_capture.py

═══════════════════════════════════════════════════════════════
