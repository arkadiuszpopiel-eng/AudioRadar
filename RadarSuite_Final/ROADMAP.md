# 🗺️ ROADMAP - RadarSuite Final v3.4.0 → v4.0.0

## 📊 AKTUALNY STATUS

**Wersja:** v3.4.1-Claude-001
**Ukończono:** 10/16 modułów (62.5%) + Gaming Platform Integration
**Do zrobienia:** 6 modułów (37.5%)
**Target:** v4.0.0-Claude-001 (100% complete)

---

## ✅ UKOŃCZONE MODUŁY (1-9, 12)

### **Phase 1: Core Detection (v3.0.0 - v3.0.5)**

- ✅ **Module 1:** Human Footstep Pattern Recognition (v3.0.0)
  - Cadence analysis (1.5-2.5 walk, 3.0-4.5 run)
  - L-R pattern detection
  - Surface type (hard/medium/soft)
  - Distance estimation (1-100m)
  - Gait classification (walk/run)

- ✅ **Module 2:** Human Voice Detection (v3.0.1)
  - Formant analysis (F1/F2/F3)
  - Pitch detection (male/female/child)
  - Intensity (whisper/normal/shout)
  - Breathing pattern recognition
  - Communication detection

- ✅ **Module 3:** Game & Audio Detection (v3.0.3)
  - 14 games support (ARC Raiders fixed!)
  - 8 game engines
  - Audio source scanner
  - Enhanced 3-source algorithm

- ✅ **Module 4:** 3D Sphere Radar (v3.0.4)
  - OpenGL visualization
  - Elevation tracking (-45° to +45°)
  - Interactive camera
  - Distance rings (25/50/75/100m)

- ✅ **Module 5:** Multi-Target Tracking (v3.0.5)
  - Up to 3 simultaneous targets
  - Intelligent matching/merging
  - Confidence-based persistence
  - Movement history (trails)

### **Phase 2: Advanced Analysis (v3.1.0 - v3.3.1)**

- ✅ **Module 6:** Advanced 3D Sound Localization (v3.2.0)
  - ITD (Interaural Time Difference)
  - ILD (Interaural Level Difference)
  - Combined 70% ITD + 30% ILD
  - Frequency-based elevation
  - Distance estimation

- ✅ **Module 7:** Sound Classification System (v3.2.0)
  - 8 sound types (rifle, pistol, shotgun, sniper, car, helicopter, explosion, grenade)
  - Spectral fingerprinting
  - Confidence scoring
  - Classification history

- ✅ **Module 8:** Threat Priority System (v3.3.0)
  - Threat scores (0-100)
  - Direction multipliers (rear 1.3x)
  - Distance factors
  - 5 threat categories (CRITICAL/HIGH/MEDIUM/LOW/MINIMAL)
  - Auto-ranking

- ✅ **Module 9:** Audio Recording & Replay (v3.3.0)
  - WAV format (16-bit)
  - JSON metadata export
  - Timestamp-based naming
  - Post-game analysis

### **Phase 3: Performance Optimization (v3.4.0)**

- ✅ **Module 12:** Performance Optimization (v3.4.0) 🚀
  - **FFT Caching:** Eliminated 4x redundant FFT computations (1 per frame instead of 4)
  - **Performance Monitoring:** Real-time FPS, CPU%, memory MB, latency ms tracking
  - **Multi-threading:** Worker pool (3 threads) for parallel audio processing
  - **Memory Optimization:** Object pooling, fixed-size buffers (deque with maxlen)
  - **Latency Tracking:** Audio-in → radar-update latency measurement (<10ms target)
  - **Stats Display:** Live performance metrics in toolbar (FPS + latency)
  - **Thread Safety:** Clean worker shutdown on application close
  - **Cache Statistics:** Hit/miss tracking for FFT cache

### **Phase 3.5: Gaming Platform Integration (v3.4.1)**

- ✅ **Gaming Platform Integration (v3.4.1)** 🎮
  - **Platform Detection:** 5 platforms (Steam, Epic Games, GOG Galaxy, Battle.net, EA App)
  - **Steam AppID System:** Database 10 gier + regex extraction z cmdline
  - **Epic Games Support:** Detekcja `-epicapp=` parameter
  - **Audio Filtering:** Blacklist 18 procesów (launchery, Discord, Spotify, przeglądarki)
  - **UI Integration:** Tab 3 - Gaming Platform Launchers sekcja (2 labels)
  - **Intelligent Detection:** Multi-source (process name, exe path, cmdline parsing)
  - **Performance:** <2ms overhead, 3s cache intervals
  - **Dependency Injection:** AudioSourceScanner + PlatformLauncherDetector integration
  - **Documentation:** Pełny raport PLATFORM_INTEGRATION_REPORT.md (550+ linii)

---

## 🚀 PLANOWANE MODUŁY (10-11, 13-16)

### **Phase 3.6: Gaming Platform Extensions (v3.4.2 - v3.4.5)** 🎮

Rozszerzenia platformy gaming przed przejściem do Module 10:

#### 🎯 **v3.4.2: Extended Platform Support**
**Cel:** Wsparcie dla dodatkowych platform gaming
**Priorytet:** HIGH

**Funkcje do implementacji:**
- **Xbox Game Pass Integration**
  - Proces: GamingServices.exe, XboxPcApp.exe
  - Microsoft Store games detection
  - Xbox Live integration (opcjonalnie)
  - Game Pass library detection

- **Ubisoft Connect**
  - Proces: upc.exe, UbisoftConnect.exe
  - Ubisoft game detection
  - Command line parameter extraction

- **Rockstar Games Launcher**
  - Proces: RockstarService.exe, LauncherPatcher.exe
  - GTA, RDR detection
  - Social Club integration

- **Origin/EA Desktop Enhancement**
  - Rozszerzona detekcja EA games
  - Origin cmdline parsing
  - EA Play integration

**Technical Specs:**
- Total platforms: 9 (było 5 + 4 nowe)
- Steam AppID DB: Rozszerzenie do 50 gier
- Audio blacklist: +6 procesów (Xbox, Ubisoft, Rockstar)
- Performance: <3ms overhead (było <2ms)

---

#### 💾 **v3.4.3: Per-Game Profiles**
**Cel:** Automatyczne ładowanie profili przy detekcji gry
**Priorytet:** HIGH (fundament dla Module 15)

**Funkcje do implementacji:**
- **Auto-Profile Loading**
  - Wykrycie gry → load matching profile
  - Profile storage: `profiles/games/{appid}.json`
  - Fallback to default profile
  - Profile validation on load

- **Profile Structure**
  - Audio device preferences
  - Detection thresholds (footsteps, voice, shots)
  - Radar settings (zoom, colors, trails)
  - Alert configuration
  - Game-specific metadata (name, appid, platform)

- **Profile Management**
  - Create profile from current settings
  - Edit existing profiles
  - Delete profiles
  - Import/Export profiles (.json)

- **Smart Profile Matching**
  - Match by Steam AppID (exact)
  - Match by process name (fuzzy)
  - Match by game engine (fallback)
  - Priority: AppID > Process > Engine > Default

**Technical Specs:**
- Profile format: JSON (human-readable)
- Max profiles: Unlimited
- Auto-save on game detection
- Load latency: <50ms

**UI Components:**
- Profile indicator in toolbar ("Profile: CS2 Competitive")
- Quick profile switcher (dropdown)
- Profile status in Tab 3

---

#### 🌐 **v3.4.4: Steam Web API Integration**
**Cel:** Automatyczne pobieranie nazw gier i metadanych
**Priorytet:** MEDIUM

**Funkcje do implementacji:**
- **Steam Web API Client**
  - API key configuration (user-provided, opcjonalnie)
  - GetAppDetails endpoint integration
  - Game name lookup by AppID
  - Cache responses (persistent, 30 days)

- **Enhanced Game Detection**
  - Auto-fetch game names for unknown AppIDs
  - Display game metadata (developer, publisher)
  - Game icon download (optional)
  - Release date, genre info

- **Offline Fallback**
  - Local AppID DB (50 popularnych gier)
  - Fallback: "Steam Game {appid}"
  - Queue for next API fetch when online

- **API Rate Limiting**
  - Max 200 requests/5 min (Steam limits)
  - Request queue with backoff
  - Error handling (API down, invalid key)

**Technical Specs:**
- API: Steam Web API v2
- Endpoint: ISteamApps/GetAppList + store.steampowered.com/api/appdetails
- Cache: SQLite database (lightweight)
- Response time: <100ms (cached), <500ms (API call)

**UI Components:**
- API key input in Settings (Tab 2)
- API status indicator ("API: Online ✅" / "Offline ❌")
- Game metadata display in Tab 3 (developer, genre)

---

#### 🎵 **v3.4.5: Enhanced Audio Routing**
**Cel:** Inteligentne priorytetowanie audio od gier
**Priorytet:** MEDIUM

**Funkcje do implementacji:**
- **Smart Audio Source Priority**
  - Game audio: Priority 1 (highest)
  - Communication (Discord, TeamSpeak): Priority 2
  - Launcher audio (Steam, Epic): Priority 3 (lowest - filtrowane)
  - Browser audio: Priority 3 (lowest)

- **Auto-Source Switching**
  - Wykrycie gry → auto-select game audio source
  - Wykrycie zakończenia gry → revert to default
  - Multi-source monitoring (game + Discord)

- **Audio Source Confidence**
  - Confidence scoring (0-100%)
  - Game audio detection accuracy
  - False positive filtering
  - Source validation (czy to faktycznie gra?)

- **Audio Routing Rules**
  - User-defined routing rules
  - "Always route X to radar when game Y is active"
  - Blacklist override (ignore specific processes)
  - Whitelist (only monitor specific sources)

**Technical Specs:**
- Priority system: 1 (high) - 5 (low)
- Auto-switch latency: <100ms
- Confidence threshold: 70% (configurable)
- Max simultaneous sources: 3

**UI Components:**
- Audio Routing panel in Tab 2
- Priority visualization (numbered list)
- Auto-switch toggle
- Confidence meter

---

### **Phase 4: Environmental & Customization (v3.5.0 - v3.6.0)**

#### 🔊 **Module 10: Environmental Audio Analysis**
**Cel:** Analiza akustyki środowiska i powierzchni
**Priorytet:** HIGH

**Funkcje do implementacji:**
- **Acoustic Environment Detection**
  - Indoor vs Outdoor classification
  - Room size estimation (small/medium/large)
  - Reverberation analysis (RT60 measurement)
  - Echo detection and delay calculation

- **Surface Material Analysis**
  - Enhanced surface detection beyond footsteps
  - Material resonance (metal, wood, concrete, glass)
  - Wall proximity detection
  - Floor type acoustic signature

- **Environmental Sound Mapping**
  - Ambient noise profiling
  - Background sound classification (rain, wind, machinery)
  - Acoustic obstacle detection
  - Sound occlusion modeling

- **Spatial Acoustics**
  - Room mode detection
  - Standing wave identification
  - Acoustic shadow mapping
  - Reflection path analysis

**Technical Specs:**
- FFT analysis: 4096-8192 samples
- Frequency bands: 20Hz - 20kHz full spectrum
- RT60 calculation: Schroeder integration
- Material database: 15+ surface types

**UI Components:**
- Environment Analysis panel (Tab 4)
- Real-time environment type indicator
- Surface material display
- Reverberation time meter

---

#### 🎵 **Module 11: Custom Sound Profiles**
**Cel:** Użytkownik może definiować własne sygnatury dźwiękowe
**Priorytet:** MEDIUM

**Funkcje do implementacji:**
- **Sound Signature Recording**
  - Record custom sound samples (3-10 seconds)
  - Multi-sample training (5+ samples per signature)
  - Automatic feature extraction
  - Signature validation and quality check

- **Custom Classification Engine**
  - User-defined sound categories
  - Template matching algorithm
  - Confidence threshold adjustment
  - Priority vs built-in classifier

- **Profile Management**
  - Save/Load custom profiles (.json)
  - Import/Export signatures
  - Profile sharing (export to file)
  - Per-game profile activation

- **Training Interface**
  - Record button with countdown
  - Real-time waveform preview
  - Feature visualization (spectrum, formants)
  - Test & validate interface

**Technical Specs:**
- Storage format: JSON with base64 audio
- Feature extraction: MFCC, spectral centroid, ZCR
- Matching algorithm: DTW (Dynamic Time Warping)
- Max custom sounds: 50 per profile

**UI Components:**
- Custom Sounds tab (new Tab 5)
- Record/Train interface
- Profile selector dropdown
- Signature library manager

---

#### 📊 **Module 13: Statistics & Heatmap**
**Cel:** Analityka sesji i mapa cieplna zagrożeń
**Priorytet:** MEDIUM

**Funkcje do implementacji:**
- **Session Statistics**
  - Total detections count (footsteps, voice, shots)
  - Detection rate (per minute)
  - Average threat level
  - Most dangerous direction (sector analysis)
  - Engagement time per target

- **Threat Heatmap**
  - 360° circular heatmap (radar-based)
  - Color coding: red (high threat) → blue (low threat)
  - Accumulation over session
  - Time-decay factor (old threats fade)
  - Export heatmap to PNG

- **Timeline Analysis**
  - Event timeline (scrollable)
  - Threat level over time graph
  - Detection frequency histogram
  - Peak danger moments

- **Comparative Statistics**
  - Per-session comparison
  - Best/Worst sessions
  - Improvement tracking
  - Accuracy metrics (false positive rate)

**Technical Specs:**
- Heatmap resolution: 360 sectors (1° precision)
- History depth: Full session (unlimited)
- Update frequency: 1 Hz (every second)
- Export formats: PNG, CSV, JSON

**UI Components:**
- Statistics tab (new Tab 7)
- Heatmap widget (circular visualization)
- Statistics dashboard (cards with numbers)
- Timeline graph (matplotlib/pyqtgraph)
- Export buttons

---

### **Phase 4: Alerts & Finalization (v3.6.0 - v4.0.0)**

#### 🚨 **Module 14: Alert System**
**Cel:** Zaawansowane ostrzeżenia wizualne i dźwiękowe
**Priorytet:** MEDIUM

**Funkcje do implementacji:**
- **Visual Alerts**
  - Screen flash (red for critical threats)
  - Border pulsing (intensity-based)
  - Directional arrows (point to threat)
  - Picture-in-Picture mini-radar overlay

- **Audio Alerts**
  - Beep tones (different pitch per threat level)
  - Voice alerts ("Enemy behind!", "Sniper detected!")
  - 3D positional audio cues
  - Customizable alert sounds (.wav files)

- **Smart Alert Logic**
  - Alert cooldown (avoid spam)
  - Priority filtering (only CRITICAL/HIGH)
  - Proximity triggers (<20m, <10m, <5m)
  - Stealth mode (silent alerts, visual only)

- **Alert Profiles**
  - Aggressive (all alerts)
  - Balanced (medium+ threats)
  - Stealth (visual only, no sound)
  - Custom (user-defined rules)

**Technical Specs:**
- Alert latency: <50ms from detection
- Audio: 16-bit WAV, 44.1kHz
- Voice alerts: TTS or pre-recorded
- Max alert rate: 1 per 2 seconds (configurable)

**UI Components:**
- Alert Settings panel (Tab 2 extension)
- Alert preview/test button
- Volume slider per alert type
- Alert log (recent alerts list)

---

#### 💾 **Module 15: Configuration Profiles**
**Cel:** Zarządzanie i zapis ustawień
**Priorytet:** HIGH

**Funkcje do implementacji:**
- **Profile System**
  - Save current settings to profile (.json)
  - Load profile (apply all settings)
  - Quick-switch profiles (dropdown + hotkey)
  - Default profiles (Universal, ARC Raiders, etc.)

- **Settings Included:**
  - Audio device + settings
  - Detection thresholds
  - Radar appearance
  - Alert configuration
  - Custom sound profiles
  - UI layout (window positions)

- **Profile Sharing**
  - Export profile to file
  - Import from file
  - Profile validation
  - Profile metadata (name, author, game, date)

- **Auto-Profile Loading**
  - Detect game → load matching profile
  - Per-game profile association
  - Fallback to default if no match

**Technical Specs:**
- Format: JSON (human-readable)
- Encryption: Optional (AES-256 for passwords)
- Max profiles: Unlimited
- Auto-save: On exit + periodic (every 5 min)

**UI Components:**
- Profile Manager (new dialog)
- Profile selector in toolbar
- Save/Load/Export buttons
- Profile details panel

---

#### 📋 **Module 16: Export & Reporting**
**Cel:** Eksport danych i raporty sesji
**Priorytet:** LOW

**Funkcje do implementacji:**
- **Data Export Formats**
  - CSV: Session statistics (detections, timestamps)
  - JSON: Full session data (structured)
  - PDF: Professional report with graphs
  - PNG: Heatmap and radar screenshots

- **Report Generation**
  - Session summary (duration, total detections)
  - Threat analysis (most dangerous sectors)
  - Performance metrics (accuracy, response time)
  - Graphs: Timeline, heatmap, detection frequency
  - Recommendations (improve awareness in sector X)

- **Automatic Reporting**
  - Generate report on session end
  - Schedule periodic reports (daily/weekly)
  - Email reports (optional, SMTP)
  - Cloud upload (Google Drive, Dropbox - optional)

- **Custom Report Templates**
  - User-defined sections
  - Branding (logo, colors)
  - Data filtering (include/exclude categories)
  - Multi-session comparison reports

**Technical Specs:**
- PDF generation: ReportLab or matplotlib
- CSV: UTF-8, RFC 4180 compliant
- JSON: Pretty-printed, validated schema
- Max report size: 10MB

**UI Components:**
- Export menu (File → Export)
- Report preview dialog
- Export settings panel
- Batch export (multiple sessions)

---

## 📅 TIMELINE ROZWOJU

### **✅ Completed: v3.4.0-v3.4.1**
- ✅ Module 12: Performance Optimization (v3.4.0) - **COMPLETE!**
- ✅ Gaming Platform Integration (v3.4.1) - **COMPLETE!**

### **Phase 3.6: Gaming Platform Extensions (v3.4.2 - v3.4.5)**
- **v3.4.2:** Extended Platform Support (Xbox, Ubisoft, Rockstar, Origin)
  - ETA: ~3-4 dni
- **v3.4.3:** Per-Game Profiles (Auto-load, profile management)
  - ETA: ~4-5 dni (wysokie znaczenie dla Module 15)
- **v3.4.4:** Steam Web API Integration (auto-fetch game names)
  - ETA: ~2-3 dni
- **v3.4.5:** Enhanced Audio Routing (smart priority, auto-switching)
  - ETA: ~3-4 dni
- **Total Phase 3.6 ETA:** ~12-16 dni (2-3 tygodnie)

### **Milestone 1: v3.5.0** (Moduły 10-11)
- Environmental Audio Analysis
- Custom Sound Profiles
- ETA: ~2-3 tygodnie

### **Milestone 2: v3.6.0** (Moduł 13)
- Statistics & Heatmap
- ETA: ~1-2 tygodnie

### **Milestone 3: v3.7.0** (Moduł 14)
- Alert System
- ETA: ~1 tydzień

### **Milestone 4: v4.0.0** (Moduły 15-16)
- Configuration Profiles
- Export & Reporting
- Final polish & testing
- ETA: ~1-2 tygodnie

**Total ETA:** ~5-8 tygodni do v4.0.0

---

## 🎯 PRIORYTETY IMPLEMENTACJI

### **IMMEDIATE Priority (Phase 3.6):**
1. ✅ ~~Module 12: Performance Optimization~~ (⚡ **COMPLETED v3.4.0**)
2. ✅ ~~Gaming Platform Integration (v3.4.1)~~ (🎮 **COMPLETED**)
3. **v3.4.2:** Extended Platform Support (🎮 Xbox, Ubisoft, Rockstar, Origin) - **NEXT**
4. **v3.4.3:** Per-Game Profiles (💾 fundament dla Module 15) - **HIGH**
5. **v3.4.4:** Steam Web API Integration (🌐 enhanced game detection)
6. **v3.4.5:** Enhanced Audio Routing (🎵 smart priority system)

### **HIGH Priority (Phase 4+):**
7. Module 10: Environmental Audio Analysis (🔊 expands capabilities)
8. Module 15: Configuration Profiles (💾 user experience - wymaga v3.4.3)

### **MEDIUM Priority:**
9. Module 11: Custom Sound Profiles (🎵 power user feature)
10. Module 13: Statistics & Heatmap (📊 analytics)
11. Module 14: Alert System (🚨 gameplay enhancement)

### **LOW Priority:**
12. Module 16: Export & Reporting (📋 nice-to-have)

---

## 🔧 TECHNICAL DEPENDENCIES

### **Module Dependencies:**
- Module 13 depends on → Module 9 (needs recording data)
- Module 14 depends on → Module 8 (uses threat levels)
- Module 15 depends on → All modules (saves all settings)
- Module 16 depends on → Module 13 (exports statistics)

### **Library Requirements (New):**
```python
# Module 10
scipy.signal.welch      # RT60 calculation

# Module 11
dtaidistance            # DTW matching
librosa                 # Audio feature extraction

# Module 12
concurrent.futures      # Threading
numba                   # JIT compilation (optional)
cupy                    # GPU acceleration (optional)

# Module 13
matplotlib              # Graphs
pillow                  # Image export

# Module 14
pyttsx3                 # TTS (optional)
pygame.mixer            # Audio alerts

# Module 16
reportlab               # PDF generation
pandas                  # Data manipulation
```

---

## 📝 DEVELOPMENT GUIDELINES

### **Code Quality:**
- All modules must have docstrings
- Unit tests for core algorithms
- Performance benchmarks for Module 12
- User testing for UI modules (11, 13, 14)

### **Backward Compatibility:**
- v3.x settings must migrate to v4.0
- Old recordings should still play
- Maintain v3.3.1 detection accuracy

### **Documentation:**
- Update README.txt for each milestone
- API documentation for custom profiles (Module 11)
- User guide for new features

---

## 🎉 v4.0.0 FEATURE COMPLETE

When all 16 modules are done, RadarSuite Final will be:
- ✅ **Production-ready** for competitive gaming
- ✅ **Fully customizable** (profiles, alerts, sounds)
- ✅ **Highly optimized** (<10ms latency)
- ✅ **Professional analytics** (heatmaps, reports)
- ✅ **User-friendly** (profiles, auto-setup)

**Target Release:** v4.0.0-Claude-001 "Complete Edition"

---

**Last Updated:** 2025-11-18
**Current Version:** v3.4.1-Claude-001
**Next Release:** v3.4.2 (Extended Platform Support - Xbox, Ubisoft, Rockstar, Origin)
**Recently Completed:**
- Module 12 (Performance Optimization - FFT caching, threading, monitoring)
- Gaming Platform Integration v3.4.1 (Steam, Epic, GOG, Battle.net, EA App)
