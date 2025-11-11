================================================================================
  AudioRadar v10.2 COMPLETE - README (Polski)
================================================================================

AudioRadar to aplikacja do wykrywania dźwięków strzałów i kroków w grach
wykorzystująca przechwytywanie audio przez WASAPI loopback na Windows.

--------------------------------------------------------------------------------
WYMAGANIA
--------------------------------------------------------------------------------
- Windows 10/11
- Python 3.11 lub nowszy
- Karta dźwiękowa z obsługą WASAPI loopback (np. Sound Blaster Z SE)

--------------------------------------------------------------------------------
SZYBKI START
--------------------------------------------------------------------------------
1. Skonfiguruj kartę dźwiękową aby udostępnić "Stereo Mix" lub "What U Hear"
   jako domyślne urządzenie nagrywające w systemie Windows

2. Uruchom START_HERE.bat - zainstaluje zależności i uruchomi aplikację

3. W aplikacji:
   - Wybierz urządzenie WASAPI loopback z listy
   - Kliknij "Start" aby rozpocząć przechwytywanie audio
   - Dostosuj "Gain" (wzmocnienie) jeśli sygnał jest za cichy
   - Dostosuj "Threshold" (próg wykrywania) dla optymalnej czułości
   - VU meter pokazuje aktualny poziom dźwięku
   - Kliknij "Test" aby sprawdzić czy wykrywanie działa

4. Kliknij "Stop" aby zakończyć przechwytywanie

--------------------------------------------------------------------------------
USTAWIENIA
--------------------------------------------------------------------------------
Gain (Wzmocnienie):
- Zakres: 0.1x - 5.0x
- Zwiększ jeśli dźwięki w grze są ciche
- Zmniejsz jeśli występują fałszywe wykrycia

Threshold (Próg wykrywania):
- Zakres: 0.01 - 1.00
- Niższe wartości = większa czułość
- Wyższe wartości = mniej fałszywych alarmów

VU Meter:
- Zielony/niebieski: normalny poziom
- Pomarańczowy: średni poziom
- Czerwony: wysoki poziom

--------------------------------------------------------------------------------
WYKRYWANIE ZDARZEŃ
--------------------------------------------------------------------------------
Aplikacja wykrywa dwa typy zdarzeń:
- SHOT (strzał): głośny, ostry dźwięk powyżej progu
- FOOTSTEP (krok): umiarkowany dźwięk powyżej niższego progu

Wszystkie wykryte zdarzenia są zapisywane w oknie "Status Log".

--------------------------------------------------------------------------------
WSPARCIE
--------------------------------------------------------------------------------
W razie problemów sprawdź:
1. TROUBLESHOOTING.txt - rozwiązywanie problemów
2. QUICK_START.txt - szybkie instrukcje
3. CHANGELOG.txt - historia zmian

--------------------------------------------------------------------------------
WERSJA: v10.2
DATA: 2024
LICENCJA: Użytek własny
================================================================================
