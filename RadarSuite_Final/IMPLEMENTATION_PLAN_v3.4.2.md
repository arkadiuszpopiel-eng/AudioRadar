# 🎮 PLAN IMPLEMENTACJI v3.4.2: Extended Platform Support

## 📋 Informacje Podstawowe

**Wersja:** v3.4.2-Claude-001
**Data utworzenia:** 2025-11-18
**Poprzednia wersja:** v3.4.1-Claude-001 (Gaming Platform Integration)
**Status:** 📝 PLANOWANIE
**ETA:** 3-4 dni robocze

---

## 🎯 Cel Wydania

Rozszerzenie wsparcia platform gaming z 5 do 9 platform poprzez dodanie:
- **Xbox Game Pass** (Microsoft Store games)
- **Ubisoft Connect** (dawniej Uplay)
- **Rockstar Games Launcher** (GTA, RDR2)
- **Origin/EA Desktop** (enhanced - było już częściowo w v3.4.1)

---

## 📊 Aktualny Stan (v3.4.1)

### **Wspierane platformy (5):**
1. ✅ Steam (steam.exe) - pełna integracja z AppID
2. ✅ Epic Games (EpicGamesLauncher.exe) - `-epicapp=` parsing
3. ✅ GOG Galaxy (GalaxyClient.exe)
4. ✅ Battle.net (Battle.net.exe)
5. ✅ EA App (EADesktop.exe) - podstawowa detekcja

### **Struktura kodu:**
- Klasa: `PlatformLauncherDetector` (app/main.py:2643-2897)
- Steam AppID DB: 10 gier
- Audio blacklist: 18 procesów
- UI: Tab 3 - "Gaming Platform Launchers" (2 labels)

---

## 🚀 Nowe Funkcje v3.4.2

### **1. Xbox Game Pass Integration**

#### **Procesy do wykrywania:**
```python
'Xbox Game Pass': {
    'process': 'GamingServices.exe',
    'helper_processes': [
        'XboxPcApp.exe',
        'XboxPcAppFT.exe',
        'GameBar.exe',
        'GameBarFTServer.exe'
    ],
    'paths': [
        r'C:\Program Files\WindowsApps',
        r'C:\XboxGames',
        r'C:\Games\XboxGames'
    ],
    'game_path_pattern': r'WindowsApps[/\\](.+?)[/\\]',
    'priority': 'high'
}
```

#### **Detekcja gier Microsoft Store:**
- Skanowanie procesów z ścieżką zawierającą `WindowsApps`
- Parsing nazwy pakietu (np. `Microsoft.SeaofThieves_2.127.7971.2_x64`)
- Ekstrakcja nazwy gry z package name
- Wykrywanie Xbox Live procesów

#### **Technical challenges:**
- Microsoft Store używa UWP (Universal Windows Platform)
- Procesy mogą mieć długie, zakodowane nazwy
- Gry uruchamiane przez `GamingServices.exe` middleware
- Wymaga parsowania command line i exe path

---

### **2. Ubisoft Connect Integration**

#### **Procesy do wykrywania:**
```python
'Ubisoft Connect': {
    'process': 'upc.exe',
    'helper_processes': [
        'UbisoftConnect.exe',
        'UplayService.exe',
        'UplayWebCore.exe'
    ],
    'paths': [
        r'C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher',
        r'C:\Program Files\Ubisoft\Ubisoft Game Launcher'
    ],
    'game_path_pattern': r'Ubisoft[/\\](.+?)[/\\]',
    'priority': 'medium'
}
```

#### **Detekcja gier Ubisoft:**
- Command line parsing dla Ubisoft game IDs
- Obsługa parametrów `-uplay_id=XXX`
- Gry instalowane w folderach Ubisoft Games
- Wykrywanie przez exe path pattern

#### **Ubisoft Game Database (top 10):**
```python
self.ubisoft_game_db = {
    'RainbowSix.exe': 'Rainbow Six Siege',
    'ACValhalla.exe': 'Assassin\'s Creed Valhalla',
    'FarCry6.exe': 'Far Cry 6',
    'WatchDogs_Legion.exe': 'Watch Dogs: Legion',
    'TheDivision2.exe': 'The Division 2',
    'ForHonor.exe': 'For Honor',
    'Anno1800.exe': 'Anno 1800',
    'ACOdyssey.exe': 'Assassin\'s Creed Odyssey',
    'GRBreakpoint.exe': 'Ghost Recon Breakpoint',
    'RiderRepublic.exe': 'Riders Republic'
}
```

---

### **3. Rockstar Games Launcher Integration**

#### **Procesy do wykrywania:**
```python
'Rockstar Games': {
    'process': 'RockstarService.exe',
    'helper_processes': [
        'LauncherPatcher.exe',
        'Launcher.exe',
        'RockstarSteamHelper.exe',
        'SocialClubHelper.exe'
    ],
    'paths': [
        r'C:\Program Files\Rockstar Games',
        r'C:\Program Files (x86)\Rockstar Games'
    ],
    'game_path_pattern': r'Rockstar Games[/\\](.+?)[/\\]',
    'priority': 'medium'
}
```

#### **Detekcja gier Rockstar:**
- GTA V (GTAVLauncher.exe, GTA5.exe)
- Red Dead Redemption 2 (RDR2.exe)
- GTA Online (Social Club integration)
- Command line parsing dla Rockstar title IDs

#### **Rockstar Game Database:**
```python
self.rockstar_game_db = {
    'GTA5.exe': 'Grand Theft Auto V',
    'RDR2.exe': 'Red Dead Redemption 2',
    'GTAVLauncher.exe': 'GTA V Launcher',
    'Launcher.exe': 'Rockstar Games Launcher'
}
```

---

### **4. Origin/EA Desktop Enhancement**

#### **Co jest już zrobione (v3.4.1):**
- Podstawowa detekcja EADesktop.exe
- Audio blacklist dla EA procesów

#### **Co dodajemy:**
- Enhanced command line parsing
- Origin.exe legacy support (dla starszych instalacji)
- EA game detection przez cmdline parameter `-gameId=`
- EA Play library detection

#### **Rozszerzona konfiguracja:**
```python
'EA App': {
    'process': 'EADesktop.exe',
    'helper_processes': [
        'EABackgroundService.exe',
        'EALocalHostSvc.exe',
        'Origin.exe',              # Legacy
        'OriginWebHelperService.exe'  # Legacy
    ],
    'paths': [
        r'C:\Program Files\Electronic Arts\EA Desktop',
        r'C:\Program Files (x86)\Origin',  # Legacy
        r'C:\Program Files\Origin'         # Legacy
    ],
    'game_path_pattern': r'(EA Games|Origin Games)[/\\](.+?)[/\\]',
    'priority': 'medium'
}
```

#### **EA Game Database (top 10):**
```python
self.ea_game_db = {
    'apexlegends.exe': 'Apex Legends',
    'Battlefield2042.exe': 'Battlefield 2042',
    'FIFA23.exe': 'FIFA 23',
    'NeedForSpeedUnbound.exe': 'Need for Speed Unbound',
    'TheSims4.exe': 'The Sims 4',
    'StarWarsJediFallenOrder.exe': 'Star Wars Jedi: Fallen Order',
    'DeadSpace.exe': 'Dead Space (2023)',
    'MassEffectLegendaryEdition.exe': 'Mass Effect Legendary',
    'Titanfall2.exe': 'Titanfall 2',
    'AnthemGame.exe': 'Anthem'
}
```

---

## 🔧 Zmiany w Kodzie

### **1. PlatformLauncherDetector.__init__() - Rozszerzenie**

**Lokalizacja:** `app/main.py:2643-2700`

**Zmiany:**
- Dodanie 4 nowych platform do `self.platforms` dict
- Rozszerzenie `self.launcher_audio_blacklist` o +6 procesów:
  ```python
  # Nowe procesy (Xbox)
  'gamingservices.exe',
  'xboxpcapp.exe',
  'gamebar.exe',

  # Nowe procesy (Ubisoft)
  'upc.exe',
  'ubisoftconnect.exe',

  # Nowe procesy (Rockstar)
  'rockstarservice.exe'
  ```

- Dodanie 3 nowych game databases:
  ```python
  self.ubisoft_game_db = {...}  # 10 gier
  self.rockstar_game_db = {...}  # 4 gry
  self.ea_game_db = {...}  # 10 gier (nowe)
  ```

**Szacowany kod:** ~80 linii dodanych

---

### **2. detect_game_from_launcher() - Enhancement**

**Lokalizacja:** `app/main.py:2780-2850`

**Nowa logika:**

```python
def detect_game_from_launcher(self, game_processes):
    """
    Wykrywa gry uruchomione przez launchery
    v3.4.2: Xbox, Ubisoft, Rockstar, EA enhanced
    """
    log("PlatformLauncherDetector.detect_game_from_launcher", "INFO")

    # ... istniejący kod dla Steam, Epic ...

    # NOWE: Xbox Game Pass detection
    for proc in game_processes:
        if 'windowsapps' in proc['exe_path'].lower():
            # Parse UWP package name
            match = re.search(r'WindowsApps[/\\](.+?)_', proc['exe_path'])
            if match:
                package_name = match.group(1)
                game_name = self._parse_uwp_package_name(package_name)
                return {
                    'name': game_name,
                    'platform': 'Xbox Game Pass',
                    'process': proc['name'],
                    'exe_path': proc['exe_path'],
                    'detection_method': 'uwp_package'
                }

    # NOWE: Ubisoft Connect detection
    for proc in game_processes:
        proc_name_lower = proc['name'].lower()
        if proc_name_lower in self.ubisoft_game_db:
            return {
                'name': self.ubisoft_game_db[proc_name_lower],
                'platform': 'Ubisoft Connect',
                'process': proc['name'],
                'exe_path': proc['exe_path'],
                'detection_method': 'game_database'
            }

        # Alternatywnie: cmdline parsing dla -uplay_id=
        cmdline = proc.get('cmdline', '')
        match = re.search(r'-uplay_id=(\d+)', cmdline, re.IGNORECASE)
        if match:
            uplay_id = match.group(1)
            return {
                'name': f'Ubisoft Game {uplay_id}',
                'platform': 'Ubisoft Connect',
                'uplay_id': uplay_id,
                'process': proc['name'],
                'detection_method': 'cmdline_uplay_id'
            }

    # NOWE: Rockstar Games detection
    for proc in game_processes:
        proc_name_lower = proc['name'].lower()
        if proc_name_lower in self.rockstar_game_db:
            return {
                'name': self.rockstar_game_db[proc_name_lower],
                'platform': 'Rockstar Games',
                'process': proc['name'],
                'exe_path': proc['exe_path'],
                'detection_method': 'game_database'
            }

    # NOWE: EA enhanced detection
    for proc in game_processes:
        proc_name_lower = proc['name'].lower()
        if proc_name_lower in self.ea_game_db:
            return {
                'name': self.ea_game_db[proc_name_lower],
                'platform': 'EA App',
                'process': proc['name'],
                'exe_path': proc['exe_path'],
                'detection_method': 'game_database'
            }

        # Alternatywnie: cmdline parsing dla -gameId=
        cmdline = proc.get('cmdline', '')
        match = re.search(r'-gameId=(\w+)', cmdline, re.IGNORECASE)
        if match:
            game_id = match.group(1)
            return {
                'name': f'EA Game {game_id}',
                'platform': 'EA App',
                'game_id': game_id,
                'process': proc['name'],
                'detection_method': 'cmdline_game_id'
            }

    return None
```

**Szacowany kod:** ~120 linii dodanych

---

### **3. Nowa metoda: _parse_uwp_package_name()**

**Lokalizacja:** `app/main.py:~2900` (nowa metoda)

**Funkcja:** Parsowanie UWP package names do czytelnych nazw gier

```python
def _parse_uwp_package_name(self, package_name):
    """
    Parsuje UWP package name do czytelnej nazwy gry

    Przykład:
    'Microsoft.SeaofThieves_2.127.7971.2_x64' → 'Sea of Thieves'
    '4df9e0f8.minecraft_1.16.40.2_x64' → 'Minecraft'
    """
    try:
        # UWP format: Publisher.GameName_Version_Arch
        # Wyciągnij Publisher.GameName
        base_name = package_name.split('_')[0]

        # Usuń publisher prefix (Microsoft., 4df9e0f8., etc.)
        if '.' in base_name:
            game_part = base_name.split('.', 1)[1]
        else:
            game_part = base_name

        # Konwersja CamelCase na spacje
        # SeaofThieves → Sea of Thieves
        game_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', game_part)

        return game_name
    except:
        # Fallback: return package name as-is
        return package_name
```

**Szacowany kod:** ~30 linii

---

### **4. Rozszerzenie Steam AppID Database**

**Lokalizacja:** `app/main.py:2720-2750`

**Było:** 10 gier
**Będzie:** 50 gier

**Nowe gry do dodania (40):**
```python
# Dodatkowe Steam games (popular titles)
271590: 'Grand Theft Auto V',
1245620: 'Elden Ring',
252490: 'Rust',
413150: 'Stardew Valley',
892970: 'Valheim',
346110: 'ARK: Survival Evolved',
1172470: 'Apex Legends',  # duplicate check
# ... total 40 more
```

**Szacowany kod:** ~40 linii dodanych

---

## 📊 Statystyki Zmian

| Metryka | v3.4.1 | v3.4.2 | Zmiana |
|---------|---------|---------|---------|
| Platformy wspierane | 5 | 9 | +4 (+80%) |
| Steam AppID DB | 10 | 50 | +40 (+400%) |
| Audio blacklist | 18 | 24 | +6 (+33%) |
| Game databases | 1 (Steam) | 4 (Steam, Ubisoft, Rockstar, EA) | +3 |
| Nowe metody | - | 1 (_parse_uwp_package_name) | +1 |
| Kod dodany | - | ~270 linii | - |
| Performance overhead | <2ms | <3ms (estimated) | +1ms |

---

## 🧪 Plan Testowania

### **Test 1: Xbox Game Pass Detection**
1. Symulacja procesu `GamingServices.exe`
2. Symulacja UWP game z package name
3. Weryfikacja parsowania package name
4. Test UI display dla Xbox games

### **Test 2: Ubisoft Connect Detection**
1. Test detekcji przez game database (Rainbow Six Siege)
2. Test cmdline parsing `-uplay_id=`
3. Weryfikacja UI status dla Ubisoft

### **Test 3: Rockstar Games Detection**
1. Test GTA V detection (GTA5.exe)
2. Test RDR2 detection
3. Weryfikacja platform status "Rockstar Games"

### **Test 4: EA Enhanced Detection**
1. Test game database (Apex Legends)
2. Test cmdline parsing `-gameId=`
3. Test legacy Origin.exe support
4. Weryfikacja backwards compatibility

### **Test 5: Audio Blacklist**
1. Weryfikacja 24 procesów w blacklist
2. Test `should_ignore_audio_source()` dla nowych procesów
3. Test integracji z AudioSourceScanner

### **Test 6: Performance**
1. Benchmark scan_platforms() z 9 platformami
2. Zmierzyć overhead (target: <3ms)
3. Test z wieloma grami uruchomionymi jednocześnie

### **Test 7: UI Integration**
1. Test wyświetlania 9 platform w Tab 3
2. Test długich nazw (Xbox UWP packages)
3. Test multiple platforms active

### **Test 8: Compilation & Syntax**
```bash
python3 -m py_compile app/main.py
```

---

## 📝 Checklist Implementacji

### **Faza 1: Kod (Dzień 1-2)**
- [ ] Rozszerzyć `self.platforms` o 4 nowe platformy
- [ ] Dodać 6 procesów do audio blacklist
- [ ] Stworzyć `ubisoft_game_db` (10 gier)
- [ ] Stworzyć `rockstar_game_db` (4 gry)
- [ ] Stworzyć `ea_game_db` (10 gier)
- [ ] Rozszerzyć Steam AppID DB do 50 gier
- [ ] Zaimplementować Xbox detection w `detect_game_from_launcher()`
- [ ] Zaimplementować Ubisoft detection
- [ ] Zaimplementować Rockstar detection
- [ ] Zaimplementować EA enhanced detection
- [ ] Stworzyć metodę `_parse_uwp_package_name()`
- [ ] Zaktualizować VERSION do v3.4.2-Claude-001
- [ ] Zaktualizować docstring klasy PlatformLauncherDetector

### **Faza 2: Testy (Dzień 2-3)**
- [ ] Test 1: Xbox Game Pass
- [ ] Test 2: Ubisoft Connect
- [ ] Test 3: Rockstar Games
- [ ] Test 4: EA Enhanced
- [ ] Test 5: Audio Blacklist
- [ ] Test 6: Performance (<3ms)
- [ ] Test 7: UI Integration
- [ ] Test 8: Compilation

### **Faza 3: Dokumentacja (Dzień 3)**
- [ ] Stworzyć PLATFORM_v3.4.2_REPORT.md
- [ ] Zaktualizować ROADMAP.md (v3.4.2 → completed)
- [ ] Dodać changelog entry
- [ ] Commit message preparation

### **Faza 4: Finalizacja (Dzień 3-4)**
- [ ] Final code review
- [ ] Performance benchmarks
- [ ] Commit all changes
- [ ] Push to remote
- [ ] Tag release v3.4.2

---

## 🎯 Success Criteria

✅ **Funkcjonalność:**
- Wszystkie 4 nowe platformy wykrywane poprawnie
- Game databases działają (lookups successful)
- UWP package parsing działa dla Xbox
- Cmdline parsing dla Ubisoft/EA działa

✅ **Performance:**
- Overhead <3ms (było <2ms w v3.4.1)
- Brak memory leaks
- Cache działa poprawnie (3s intervals)

✅ **Qualité:**
- Kod kompiluje się bez błędów
- Wszystkie testy przechodzą
- Backwards compatible z v3.4.1
- UI wyświetla wszystkie 9 platform

✅ **Dokumentacja:**
- Pełny raport wygenerowany
- ROADMAP zaktualizowany
- Kod ma docstrings

---

## 🚧 Known Challenges

### **Challenge 1: UWP Package Parsing**
- **Problem:** Xbox UWP packages mają skomplikowane nazwy
- **Solution:** Regex parsing + CamelCase splitting
- **Fallback:** Wyświetl package name as-is

### **Challenge 2: EA Legacy Origin Support**
- **Problem:** Starsze instalacje używają Origin.exe zamiast EADesktop.exe
- **Solution:** Wspieraj oba procesy w helper_processes
- **Testing:** Sprawdź czy detection działa dla obu

### **Challenge 3: Performance z 9 Platformami**
- **Problem:** Więcej platform = więcej skanowania
- **Solution:** Maintain 3s cache, lazy evaluation
- **Target:** <3ms overhead (akceptowalne)

### **Challenge 4: Rockstar Multi-Launcher**
- **Problem:** Rockstar games mogą być uruchamiane przez Steam/Epic + Rockstar Launcher
- **Solution:** Priorytetyzuj Rockstar detection jeśli widzimy RockstarService.exe
- **Logic:** Check for Rockstar processes first

---

## 📦 Deliverables

1. **Kod:** app/main.py (+270 linii)
2. **Dokumentacja:** PLATFORM_v3.4.2_REPORT.md (~400 linii)
3. **Tests:** Test results log
4. **ROADMAP:** Zaktualizowany (v3.4.2 completed)
5. **Commit:** Detailed commit message
6. **Tag:** v3.4.2-Claude-001

---

## 🔄 Next Steps (po v3.4.2)

**Kolejna wersja:** v3.4.3 - Per-Game Profiles
- Auto-load profile przy detekcji gry
- Profile management system
- JSON storage format
- Fundament dla Module 15

**Timeline:**
- v3.4.2 completion: +3-4 dni
- v3.4.3 start: Immediately after
- v3.4.3 ETA: +4-5 dni

---

**Plan Created:** 2025-11-18
**Status:** 📝 READY FOR IMPLEMENTATION
**Next Action:** Start Phase 1 - Code Implementation
