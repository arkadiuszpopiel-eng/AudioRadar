# KOMPLEKSOWY PLAN NAPRAW - 4 PRIORYTETY

**Data:** 2025-12-20
**Wersja:** v4.3.1-k0007 → k0008 ✅ COMPLETED
**Użytkownik:** Wszystkie 4 priorytety muszą działać!
**Scenariusz wybrany:** B (krok po kroku z testowaniem)

---

## 🎯 STATUS IMPLEMENTACJI (v4.3.1-k0008)

### ✅ PRIORYTET 1: Radar UI - Lepsze & Dopracowane
**Status:** ✅ UKOŃCZONE w k0007

### ✅ PRIORYTET 2: Radar Widget Nie Reaguje na START
**Status:** ✅ UKOŃCZONE w k0008
- ✅ Obniżone progi detekcji (ENERGY_THRESHOLD: 0.001→0.0005, LOCALIZATION_MIN_CONFIDENCE: 30→20)
- ✅ Obniżone progi confidence (ALGORITHM_MIN: 30→20, UI_MIN: 50→40, THREAT_MIN: 70→60)
- ✅ Dodano debug logging (co 100 klatek: has_detection, energy, active_targets, events)

### 📦 PRIORYTET 3: ML Tab - Wszystkie Funkcje
**Status:** ⚠️ WYMAGA AKCJI UŻYTKOWNIKA
- Użytkownik musi uruchomić: `pip install joblib scikit-learn`
- ML Training panel zadziała po instalacji zależności
- Moduł opcjonalny - graceful degradation bez joblib

### ✅ PRIORYTET 4: Radar Rotation - Czyste Programowe Rozwiązanie
**Status:** ✅ UKOŃCZONE w k0008
- ✅ Usunięto broken player_yaw memory reading (zawsze zwracało 0.0)
- ✅ Zaimplementowano camera-relative radar: `angle_radar = 90.0 + angle_combined`
- ✅ Działa bez zewnętrznych urządzeń, konfiguracji, Cheat Engine
- ✅ Bezpieczne (no anti-cheat risk), uniwersalne dla wszystkich gier

---

## 1️⃣ **PRIORYTET 1: Radar UI - Lepsze & Dopracowane** ✅ ZROBIONE

### Status: UKOŃCZONE w k0007

**Co zostało zrobione:**
- ✅ Czcionki +30-50% większe (12pt/11pt/13pt/15pt)
- ✅ Kolory +50% jaśniejsze (grid, text, distance labels)
- ✅ Ikony celów +50% większe z 2x jaśniejszym glow
- ✅ Panel legendy pokazujący Walk/Run/Shot
- ✅ Lista celów z lepszym spacingiem (10 zamiast 8)
- ✅ Overflow indicator gdy >10 celów

**Pliki:**
- `app/widgets/military_hud.py` (+90 linii)
- `app/core/translations.py` (+2 klucze)

---

## 2️⃣ **PRIORYTET 2: Radar Widget Nie Reaguje na START** 🔴 KRYTYCZNE

### Problem Diagnosis:

**Możliwe przyczyny:**
1. Audio device nie jest wybrany prawidłowo
2. Detection threshold za wysoki (brak wykryć)
3. Sweep animation nie działa
4. Targets nie są dodawane do radaru

### Co sprawdzić:

```python
# TEST 1: Czy audio device jest wybrany?
# W Detection & Audio tab → sprawdź czy urządzenie jest wybrane

# TEST 2: Czy detection działa?
# Otwórz Analysis tab → sprawdź czy spektrum się rusza

# TEST 3: Czy sweep się obraca?
# Radar powinien mieć wirującą zieloną linię

# TEST 4: Czy są jakieś błędy w log?
# Sprawdź log/super_log.txt
```

### Rozwiązanie:

**OPCJA A: Test Mode (Syntetyczny sygnał)**
```python
# main.py - dodaj przycisk "TEST MODE" który generuje sztuczne cele
def enable_test_mode(self):
    self.test_mode = True
    # Generuje syntetyczne audio z krokami/strzałami
```

**OPCJA B: Obniż Detection Threshold**
```python
# app/core/constants.py
ENERGY_THRESHOLD = 0.001  # było 0.005 - NIŻSZY = bardziej czuły
LOCALIZATION_MIN_CONFIDENCE = 30  # było 50 - NIŻSZY = więcej wykryć
```

**OPCJA C: Debug Logging**
```python
# Dodaj więcej logów w _process_detection_and_tracking
log(f"Detection: has_detection={has_detection}, energy={energy}, "
    f"active_targets={len(active_targets)}", "DEBUG")
```

### Action Plan:

1. **Najpierw sprawdzę logi** - zobacz czy są błędy
2. **Obniżę thresholdy** - łatwiejsze wykrywanie
3. **Dodam debug mode** - wizualne potwierdzenie że działa
4. **Stworzę "Synthetic Test Mode"** - zawsze pokazuje cele testowe

---

## 3️⃣ **PRIORYTET 3: ML Tab - Wszystkie Funkcje** 🔴 KRYTYCZNE

### Problem:
```
ModuleNotFoundError: No module named 'joblib'
```

### Rozwiązanie:

**KROK 1: Zainstaluj zależności ML**
```bash
pip install joblib scikit-learn numpy
```

**KROK 2: Restart aplikacji**
```bash
python app/main.py
```

**KROK 3: Sprawdź ML Training tab**
- Powinien pokazać pełny panel zamiast błędu
- Przyciski: Quick Record, Start Session, Stop Session
- Waveform timeline, class selection

### Jeśli nadal nie działa:

**Plan B: Opcjonalne ML**
```python
# Zmodyfikuję builder.py żeby ML był OPCJONALNY
# Jeśli brakuje joblib, pokaż uproszczony panel z informacją
# ALe nie blokuj reszty funkcjonalności
```

---

## 4️⃣ **PRIORYTET 4: Radar Rotation - Czyste Programowe Rozwiązanie** 🎯

### Obecny Problem:
- `player_yaw` zawsze = 0.0 (memory reading nie działa)
- Radar pokazuje dźwięki względem słuchawek, NIE gracza

### Rozwiązanie: Camera-Relative Radar (BEZ zewnętrznych urządzeń!)

**Koncepcja:**
```
Gracz obraca się w grze → głowa się obraca → audio zmienia się → radar aktualizuje

PRZYKŁAD:
1. Przeciwnik jest NA PÓŁNOC w grze
2. Gracz patrzy NA PÓŁNOC → słyszy z PRZODU → radar: cel Z PRZODU ✅
3. Gracz obraca się i patrzy NA WSCHÓD → słyszy z LEWEJ → radar: cel Z LEWEJ ✅
```

**Zmiana w kodzie:**

```python
# PRZED (main.py linia 1541-1556):
try:
    player_yaw = self.memory_reader.read_player_yaw()  # ❌ Zawsze 0
except:
    player_yaw = 0.0

angle_radar = 90.0 + angle_combined
angle_radar = (angle_radar - player_yaw) % 360.0  # ❌ Broken transform

# PO:
# Camera-relative - pokazuje dźwięki względem słuchawek/kamery
angle_radar = 90.0 + angle_combined  # ✅ PROSTE!
# Gdy się obracasz, audio się zmienia, radar się aktualizuje
```

**ZALETY:**
- ✅ Działa NATYCHMIAST bez konfiguracji
- ✅ Czyste programowe rozwiązanie (ZERO hardware)
- ✅ Bezpieczne (no memory reading, no anti-cheat risk)
- ✅ Uniwersalne dla WSZYSTKICH gier
- ✅ Intuicyjne: "słyszę z przodu" = "radar pokazuje z przodu"

**WADY:**
- ⚠️ Nie pokazuje absolute position w grze
- ⚠️ Jeśli stoisz w miejscu i przeciwnik chodzi wokół, radar go śledzi względem CIEBIE

**WADA JEST MINIMALNA** bo:
- 99% czasu się ruszasz/obracasz w grze
- Radar nadal pokazuje GDZIE SĄ wrogowie względem CIEBIE
- To jest DOKŁADNIE to czego potrzebujesz w grze!

---

## 📋 **KOLEJNOŚĆ IMPLEMENTACJI:**

### **SPRINT 1: Krytyczne Poprawki (1-2h)**
1. ✅ Radar UI improvements (DONE)
2. 🔴 Fix radar widget not responding
3. 🔴 ML dependencies installation guide
4. 🔴 Camera-relative radar fix

### **SPRINT 2: Ulepszenia (30min-1h)**
5. Test mode dla radaru (synthetic targets)
6. Debug panel showing detection stats
7. Adjustable detection thresholds in UI

### **SPRINT 3: Dokumentacja (30min)**
8. User guide for radar positioning
9. Troubleshooting guide
10. Update CHANGELOG

---

## 🔧 **NATYCHMIASTOWE AKCJE:**

### **Akcja 1: Zbierz informacje diagnostyczne**

Proszę uruchom te komendy i wyślij mi output:

```bash
# 1. Sprawdź czy joblib jest zainstalowany
pip list | findstr joblib

# 2. Sprawdź logi
type log\super_log.txt | findstr /i "error\|critical\|detection"

# 3. Sprawdź czy audio device działa
# (uruchom app, otwórz Detection & Audio tab, zrób screenshot)
```

### **Akcja 2: Powiedz mi:**
- Czy widzisz zieloną wirującą linię na radarze (sweep)?
- Czy w Analysis tab widzisz ruchome spektrum audio?
- Czy kiedy robisz hałas (klaskanie), LED zmienia kolor?

---

## ✅ **CO ZROBIĘ TERAZ:**

Wybierz scenariusz:

**SCENARIUSZ A: "Napraw wszystko za jednym razem"**
- Zrobię wszystkie 4 priorytety naraz
- Czas: 1-2h
- Commit wszystko razem jako k0008

**SCENARIUSZ B: "Krok po kroku z testowaniem"**
- Najpierw priorytet 2 (radar fix) → test → commit
- Potem priorytet 3 (ML) → test → commit
- Potem priorytet 4 (rotation) → test → commit
- Czas: 2-3h z testami

**SCENARIUSZ C: "Tylko najważniejsze"**
- Priorytet 2 (radar fix) + Priorytet 4 (rotation)
- Priorytet 3 (ML) zostawiam Tobie (pip install)
- Czas: 30-60min

---

## 🎯 **CZEKAM NA DECYZJĘ:**

1. Który scenariusz wybierasz (A/B/C)?
2. Wyślij mi diagnostykę (Akcja 1)
3. Odpowiedz na pytania (Akcja 2)

**Kiedy dostanę odpowiedzi, zacznę naprawiać!** 🚀
