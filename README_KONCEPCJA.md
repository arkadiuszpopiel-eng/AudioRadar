# Audio Radar – koncepcja systemu

## Cel projektu
Audio Radar to aplikacja na Windows 11, która w czasie rzeczywistym przechwytuje dźwięk z gry (loopback z karty dźwiękowej), wykrywa w nim kroki oraz strzały przeciwników i wizualizuje kierunek, z którego dochodzą. Projekt ma wspierać graczy, w tym osoby niedosłyszące, w lepszej orientacji przestrzennej.

## Architektura wysokiego poziomu
1. **Przechwytywanie audio** – moduł wykorzystujący WASAPI loopback (PyAudio/PyAudioWPatch lub sounddevice) do pobierania próbek audio 16-bit/48 kHz z urządzenia wyjściowego (stereo lub wielokanałowe 5.1/7.1).
2. **Przetwarzanie sygnału** – potok DSP obejmujący filtrację pasmową, kompresję dynamiki, redukcję szumów oraz detekcję transjentów.
3. **Klasyfikacja zdarzeń** – heurystyki lub lekki model ML, które rozróżniają kroki i strzały oraz odrzucają inne dźwięki.
4. **Lokalizacja źródeł** – analiza energii w kanałach audio i mapowanie jej na kierunek (0–360°) z interpolacją między kanałami.
5. **Warstwa prezentacji** – overlay/radar 2D aktualizowany w 60 FPS, pokazujący znacznik kroku/strzału wraz z intensywnością odpowiadającą głośności.

## Szczegóły modułów
### 1. Przechwytywanie audio
- Ustawienie strumienia WASAPI loopback z minimalnym rozmiarem bufora (20–50 ms) dla małego opóźnienia.
- Obsługa stereo oraz konfiguracji 5.1/7.1 (preferowana) z wykrywaniem liczby kanałów.
- Asynchroniczne pobieranie próbek w oddzielnym wątku, przekazywanie ich do kolejki FIFO dla modułu DSP.

### 2. Potok DSP
- **Filtry pasmowe:**
  - Pasmo 2–8 kHz podkreśla detekcję kroków.
  - Szerokie pasmo 200 Hz – 12 kHz do detekcji strzałów.
- **Kompresor/limiter:** wyrównanie dynamiki, aby ciche kroki były wykrywalne mimo głośnych zdarzeń.
- **Redukcja szumów:** np. RNNoise lub bramka szumów dla usuwania ambientu.
- **Detekcja transjentów:** analiza RMS/energia w oknach 10–20 ms, wykrywanie pików powyżej adaptacyjnego progu tła.

### 3. Klasyfikacja zdarzeń
- Ekstrakcja cech (FFT, MFCC, czas trwania impulsu, stosunek energii w pasmach).
- Reguły heurystyczne:
  - Strzały: pojedynczy impuls o szerokim spektrum i dużej amplitudzie.
  - Kroki: seria mniejszych pików o rytmie 1–3 Hz, zdominowanych przez pasmo 2–8 kHz.
- Możliwość rozszerzenia o model ML (np. sieć CNN na spektrogramach) trenowany na próbkach kroków/strzałów.

### 4. Lokalizacja kierunku
- Odczyt poziomu RMS w każdym kanale w momencie zdarzenia.
- Mapowanie kanałów 5.1/7.1 na sektory (np. Front Left ≈ 30°, Rear Left ≈ 150° itd.).
- Interpolacja między kanałami dla płynnych kątów; w stereo – porównanie L/R i detekcja przód/tył na podstawie cech HRTF (opcjonalne).
- Szacowanie odległości na podstawie amplitudy i pasma (cichsze = dalej).

### 5. Wizualizacja
- Okno overlay (PyGame, PyQt lub pyglet) z przezroczystym tłem, zawsze na wierzchu.
- Radar 2D z podziałem na 360°; markery:
  - Kroki: zielone/pulsujące okręgi.
  - Strzały: czerwone ikony gwiazdki.
- Intensywność markera zależna od głośności (rozmiar/jasność).
- Buforowanie zdarzeń (np. 1–2 s) i stopniowe wygaszanie markerów.

## Wydajność i opóźnienia
- Cel: opóźnienie całkowite < 100 ms.
- Optymalizacja poprzez użycie Numpy/Cython do obróbki bloków audio, wielowątkowość (audio, DSP, GUI).
- Możliwość wykorzystania GPU (cuFFT) dla spektrogramów przy ML.

## Technologia i zależności
- Python 3.11+
- Biblioteki: PyAudioWPatch lub sounddevice, numpy, scipy, librosa, RNNoise (bindings), PyGame/PyQt, opcjonalnie PyTorch/TensorFlow dla ML.
- Wsparcie sterowników WASAPI, konfiguracja systemu na 5.1/7.1 dla maksymalnej precyzji.

## Plan rozwoju MVP
1. Implementacja loopbacku i rejestracji próbek.
2. Prosta detekcja transjentów + heurystyka krok/strzał.
3. Lokalizacja dla stereo (lewo/prawo) i podstawowy radar.
4. Rozszerzenie na 5.1/7.1 z mapowaniem kanałów.
5. Dodanie kompresji, redukcji szumów i opcjonalnego ML.
6. Testy w popularnych grach FPS, strojenie progów i filtrów.

## Testowanie i ewaluacja
- Scenariusze testowe z nagranymi próbkami kroków/strzałów z różnych kątów.
- Walidacja skuteczności detekcji (precision/recall) oraz dokładności kąta.
- Pomiar opóźnienia (nagrywanie ekran + audio, analiza). 

## Potencjalne rozszerzenia
- Integracja z profilem dźwiękowym gry (np. API gry, jeśli dostępne).
- System powiadomień haptic (wibracje) dla dodatkowego sprzężenia zwrotnego.
- Personalizacja HRTF / kalibracja użytkownika.
- Eksport telemetrii (logi zdarzeń) do analizy po meczu.

## Wymagania użytkowe
- Windows 11, karta dźwiękowa z obsługą loopback (np. Sound Blaster Z SE).
- Słuchawki/głośniki dowolne; dla najlepszych efektów konfiguracja 5.1/7.1.
- Interfejs w języku polskim z możliwością zmiany kolorystyki i czułości detekcji.

## Wnioski
Proponowana architektura pozwala stworzyć w Pythonie aplikację, która w czasie rzeczywistym zamienia sygnał audio z gry na intuicyjną reprezentację przestrzenną kroków i strzałów. Kluczowe elementy to skuteczna detekcja transjentów, mapowanie wielokanałowe oraz minimalistyczny, responsywny interfejs radarowy. Dzięki nim Audio Radar może znacząco zwiększyć świadomość sytuacyjną gracza.
