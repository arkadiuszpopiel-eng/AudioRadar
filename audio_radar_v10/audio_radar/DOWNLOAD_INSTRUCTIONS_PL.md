# AudioRadar v10.2 - Instrukcje Pobrania i Instalacji

## 📦 Pobieranie Paczek ZIP

### Główna Paczka - AudioRadar v10.2 FULL

**Plik:** `AudioRadar_v10.2_FULL.zip`

**Zawartość:**
- Kompletny kod źródłowy AudioRadar v10.2
- Wszystkie moduły Python (gui.py, main.py, audio_capture.py, itp.)
- Pełna dokumentacja (README.md, CHANGELOG.md, GUI_FEATURES.md)
- Skrypt instalacyjny (RUN_BUILD_ALL.cmd)
- Notatki o wydaniu (RELEASE_NOTES_v10.2.md)
- Przewodnik przed/po (BEFORE_AFTER.md)

**Rozmiar:** ~34 KB (skompresowany)

---

## 🔗 Linki do Pobrania

### Opcja 1: GitHub Releases (Zalecane)

```
https://github.com/arkadiuszpopiel-eng/AudioRadar/releases/tag/v10.2
```

Pobierz plik `AudioRadar_v10.2_FULL.zip` z sekcji Assets.

### Opcja 2: GitHub Repository (Kod Źródłowy)

```
https://github.com/arkadiuszpopiel-eng/AudioRadar
```

**Pobieranie całego repozytorium:**
```bash
git clone https://github.com/arkadiuszpopiel-eng/AudioRadar.git
cd AudioRadar/audio_radar_v10/audio_radar
```

**Lub pobierz jako ZIP:**
- Kliknij zielony przycisk "Code"
- Wybierz "Download ZIP"
- Rozpakuj i przejdź do `audio_radar_v10/audio_radar/`

### Opcja 3: Bezpośredni Link do Branch

```
https://github.com/arkadiuszpopiel-eng/AudioRadar/archive/refs/heads/copilot/add-gain-threshold-controls.zip
```

Ten link pobierze najnowszą wersję z gałęzi z funkcjami v10.2.

---

## 📋 Wymagania Systemowe

### Minimalne:
- **System:** Windows 10/11 (64-bit)
- **Python:** 3.8 lub nowszy
- **RAM:** 2 GB
- **Miejsce na dysku:** 100 MB

### Zalecane:
- **System:** Windows 11 (64-bit)
- **Python:** 3.10 lub nowszy
- **RAM:** 4 GB
- **Karta dźwiękowa:** Z funkcją loopback (np. Sound Blaster Z SE, Stereo Mix)

---

## 🚀 Instalacja Krok po Kroku

### Krok 1: Pobierz Paczkę

Wybierz jedną z opcji powyżej i pobierz plik ZIP.

### Krok 2: Rozpakuj

```
Kliknij prawym → Rozpakuj wszystko → Wybierz lokalizację
```

Zalecana lokalizacja: `C:\AudioRadar\`

### Krok 3: Zainstaluj Python (jeśli nie masz)

Pobierz z: https://www.python.org/downloads/

**Ważne:** Podczas instalacji zaznacz "Add Python to PATH"!

### Krok 4: Otwórz Terminal

```
Windows + R → wpisz "cmd" → Enter
```

Przejdź do folderu:
```bash
cd C:\AudioRadar\audio_radar_v10\audio_radar
```

### Krok 5: Zainstaluj Zależności

**Automatycznie (Windows):**
```bash
RUN_BUILD_ALL.cmd
```

**Ręcznie:**
```bash
pip install PyQt5 sounddevice numpy pygame
```

### Krok 6: Uruchom Program

**Z GUI (Zalecane - v10.2):**
```bash
python run_gui.py
```

**Klasyczny tryb (tylko Pygame):**
```bash
python main.py
```

---

## 📚 Pełna Dokumentacja

Po rozpakowaniu paczki znajdziesz:

### README.md
Główna dokumentacja z opisem funkcji i rozwiązywaniem problemów.

### CHANGELOG.md
Historia zmian i nowe funkcje w każdej wersji.

### GUI_FEATURES.md
Szczegółowy przewodnik po wszystkich funkcjach GUI (8,700+ linii).

### BEFORE_AFTER.md
Wizualne porównanie przed/po z przykładami użycia.

### RELEASE_NOTES_v10.2.md
Kompletne notatki o wydaniu v10.2.

---

## 🎯 Szybki Start - Pierwsze Uruchomienie

### 1. Po Instalacji

```bash
cd C:\AudioRadar\audio_radar_v10\audio_radar
python run_gui.py
```

### 2. Zobaczysz Okno GUI

```
┌─────────────────────────────────────┐
│ Audio Radar v10.2 - Control Panel   │
├─────────────────────────────────────┤
│  [Controls] [Info]                  │
│                                     │
│  Input Gain:     [──●──]  1.0x     │
│  Threshold:      [──●──]  0.050    │
│  Signal Strength: [     ]  0%      │
│                                     │
│  [🎯 Auto-Calibrate Threshold]     │
│  [▶ START Detection]               │
└─────────────────────────────────────┘
```

### 3. Konfiguracja Audio

1. Wybierz urządzenie wejściowe (np. "Stereo Mix")
2. Kliknij "🔄 Refresh" jeśli nie widzisz urządzeń

### 4. Kalibracja (Zalecane)

1. Wyłącz wszystkie gry/muzykę
2. Kliknij "🎯 Auto-Calibrate Threshold"
3. Poczekaj 10 sekund
4. Program ustawi optymalny próg

### 5. Testowanie

1. Uruchom audio (grę, muzykę)
2. Obserwuj "Signal Strength"
3. Jeśli czerwony/pomarańczowy → zwiększ "Input Gain"
4. Kliknij "▶ START Detection"

---

## 🔧 Rozwiązywanie Problemów

### Problem: "PyQt5 not found"

**Rozwiązanie:**
```bash
pip install PyQt5
```

### Problem: "sounddevice library not found"

**Rozwiązanie:**
```bash
pip install sounddevice
```

Jeśli nadal nie działa:
```bash
# Zainstaluj PortAudio
pip install --upgrade sounddevice
```

### Problem: Brak urządzeń audio

**Rozwiązanie:**
1. Włącz "Stereo Mix" w ustawieniach Windows:
   - Prawy klik na ikonę głośnika → Dźwięki
   - Zakładka "Nagrywanie"
   - Prawy klik → Pokaż wyłączone urządzenia
   - Włącz "Stereo Mix"

### Problem: Sygnał za słaby (czerwony pasek)

**Rozwiązanie:**
1. Zwiększ "Input Gain" do 5.0x - 10.0x
2. Lub użyj "Enable Pre-Amplifier"
3. Lub obniż "Detection Threshold" do 0.010-0.025

---

## 📞 Pomoc i Wsparcie

### GitHub Issues
```
https://github.com/arkadiuszpopiel-eng/AudioRadar/issues
```

Zgłoś problemy lub poproś o pomoc.

### Dokumentacja Online
```
https://github.com/arkadiuszpopiel-eng/AudioRadar/tree/copilot/add-gain-threshold-controls/audio_radar_v10/audio_radar
```

Przeczytaj README.md i inne pliki dokumentacji online.

---

## 🆕 Co Nowego w v10.2?

### Główne Funkcje

1. **Kontrola Wzmocnienia (Input Gain)**
   - Zakres: 0.1x - 10.0x
   - Wzmacnia słabe sygnały audio

2. **Regulowany Próg (Adjustable Threshold)**
   - Zakres: 0.001 - 0.200
   - Dostosuj czułość detekcji

3. **Wskaźnik Siły Sygnału**
   - Pasek postępu w czasie rzeczywistym
   - Kodowanie kolorami: 🔴 Czerwony / 🟡 Pomarańczowy / 🟢 Zielony

4. **Auto-Kalibracja**
   - Analiza 10s szumu tła
   - Automatyczne ustawienie optymalnego progu

5. **Wzmacniacz Wstępny**
   - Szybkie wzmocnienie x5
   - Dla bardzo słabych sygnałów

6. **Interfejs GUI PyQt5**
   - Nowoczesny panel sterowania
   - Polskie podpowiedzi
   - Dwie zakładki: Controls + Info

### Rozwiązany Problem

**Przed v10.2:**
- Peak sygnału: 0.005 (0.5%)
- Domyślny próg: 0.050 (5%)
- Wynik: NIE WYKRYTO ❌

**Po v10.2:**
- Peak × 10 gain = 0.050 (5%)
- Lub próg obniżony do 0.003
- Wynik: WYKRYTO ✓

---

## 📦 Struktura Paczki

```
AudioRadar_v10.2_FULL.zip
└── audio_radar_v10/
    └── audio_radar/
        ├── gui.py                    # GUI PyQt5 (660 linii)
        ├── run_gui.py                # Launcher GUI
        ├── main.py                   # Klasyczny tryb
        ├── audio_capture.py          # Przechwytywanie audio
        ├── sound_analysis.py         # Analiza dźwięku
        ├── visualization.py          # Wizualizacja Pygame
        ├── config.json               # Konfiguracja
        ├── RUN_BUILD_ALL.cmd         # Instalator Windows
        │
        ├── README.md                 # Główna dokumentacja
        ├── CHANGELOG.md              # Historia zmian
        ├── VERSION.txt               # Wersja (v10.2)
        ├── RELEASE_NOTES_v10.2.md    # Notatki o wydaniu
        ├── GUI_FEATURES.md           # Przewodnik GUI
        ├── BEFORE_AFTER.md           # Porównanie
        └── DOWNLOAD_INSTRUCTIONS_PL.md  # Ten plik
```

---

## ✅ Lista Kontrolna Po Instalacji

- [ ] Python 3.8+ zainstalowany
- [ ] Wszystkie zależności zainstalowane (PyQt5, sounddevice, numpy, pygame)
- [ ] "Stereo Mix" lub inne urządzenie loopback włączone
- [ ] GUI uruchamia się bez błędów
- [ ] Urządzenie audio widoczne w dropdownie
- [ ] Pasek Signal Strength reaguje na audio
- [ ] Auto-kalibracja działa
- [ ] Detekcja wykrywa footsteps/gunshots

---

## 🎊 Gotowe!

Teraz możesz używać AudioRadar v10.2 z pełną kontrolą wzmocnienia i progu detekcji!

**Problem ze słabym sygnałem? ROZWIĄZANY!** ✓

Ciesz się lepszą detekcją audio bez konieczności kupowania nowego sprzętu!

---

**Wersja:** v10.2  
**Data:** 2025-11-09  
**Repozytorium:** https://github.com/arkadiuszpopiel-eng/AudioRadar  
**Branch:** copilot/add-gain-threshold-controls
