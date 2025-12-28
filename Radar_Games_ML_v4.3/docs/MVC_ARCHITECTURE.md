# MVC Architecture in Radar Games ML v4.3.1

**Document Version:** 1.0
**Date:** 2025-12-14
**Sprint:** 2.1 - ApplicationController Foundation

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture Components](#architecture-components)
3. [Delegation Flow](#delegation-flow)
4. [File Structure](#file-structure)
5. [Implementation Examples](#implementation-examples)
6. [Best Practices](#best-practices)
7. [Migration Guide](#migration-guide)

---

## Overview

Starting with **v4.3.1**, Radar Games ML adopts the **Model-View-Controller (MVC)** pattern to improve code maintainability, testability, and separation of concerns.

### Goals

- **Reduce MainWindow complexity** (was 1978 lines → now 1914 lines)
- **Improve testability** by isolating business logic from UI
- **Enable easier refactoring** through clear responsibility boundaries
- **Facilitate team collaboration** with well-defined component roles

### Implementation Status

- ✅ **Phase 1:** ApplicationController foundation (SPRINT 2.1)
- ✅ **Phase 2:** MainWindow MVC integration
- ⏳ **Phase 3:** Complete extraction (planned)

---

## Architecture Components

### Model

**Location:** `app/audio/`, `app/detection/`, `app/tracking/`

**Responsibility:** Business logic, data processing, state management

**Key Components:**
- `AudioEngine` - Audio capture and processing
- `DetectionWorker` - Sound detection and classification
- `TargetTracker` - Multi-target tracking system
- `SoundClassifier` - ML-based sound classification

**Characteristics:**
- No UI dependencies
- Pure Python logic
- Testable in isolation
- Reusable across different views

---

### View

**Location:** `app/main.py`, `app/ui/`, `app/widgets/`

**Responsibility:** UI presentation, user input, visual updates

**Key Components:**
- `MainWindow` - Primary application window
- `UIBuilder` - UI construction (v4.2.0 pattern)
- `Widgets` - Radar displays, panels, visualizations
- `EventHandlers` - UI event delegation (v4.3.1)

**Characteristics:**
- PyQt5/Qt6 specific code
- Delegates business logic to Controller
- Minimal state management
- Focus on presentation only

---

### Controller

**Location:** `app/core/application_controller.py`

**Responsibility:** Coordinate between Model and View, application lifecycle

**Key Components:**
- `ApplicationController` - Main controller (v4.3.1)

**Responsibilities:**
```python
# Timer Management
- tick_timer (20 FPS main loop)
- game_scan_timer (5s interval)
- audio_scan_timer (2s interval)

# Lifecycle Management
- start() / stop() audio capture
- cleanup() on application exit

# State Synchronization
- controller.is_running ↔ window.is_running
- Coordinated state updates
```

---

## Delegation Flow

### User Interaction Flow

```
┌─────────────┐
│ User Action │ (Button Click, Keyboard Shortcut)
└──────┬──────┘
       ↓
┌─────────────┐
│ View (UI)   │ MainWindow receives Qt event
└──────┬──────┘
       ↓
┌──────────────┐
│ EventHandler │ event_handlers.toggle_start_stop()
└──────┬───────┘
       ↓
┌──────────────┐
│ Controller   │ controller.start() / stop()
└──────┬───────┘
       ↓
┌──────────────┐
│ Model        │ audio.start(), detection_worker.submit()
└──────┬───────┘
       ↓
┌──────────────┐
│ View Update  │ window.update_ui(), radar_widget.update()
└──────────────┘
```

### Code Example

```python
# 1. UI Event (View)
def start_btn_clicked(self):
    # ui/builder.py:490
    self.main.start_btn.clicked.connect(self.main.toggle_start_stop)

# 2. Event Handler (View → Controller)
def toggle_start_stop(self):
    # ui/event_handlers.py:225
    if not self.window.is_running:
        self.window.start()  # Delegate to window
    else:
        self.window.stop()

# 3. MainWindow Delegation (View → Controller)
def start(self):
    # main.py:901
    self.controller.start()  # Delegate to controller

# 4. Controller Logic (Controller → Model)
def start(self):
    # core/application_controller.py:111
    self.window.dev_panel.apply_settings()  # Configure model
    self.window.audio.start()               # Start model

    # State sync (Controller → View)
    self.is_running = True
    self.window.is_running = True
    self.window.record_btn.setEnabled(True)

    # UI update (Controller → View)
    self._update_start_button_ui(running=True)

# 5. Model Processing (Model)
def start(self) -> None:
    # audio/engine.py:156
    self.running = True
    self._start_loopback()  # Start audio capture thread
```

---

## File Structure

```
Radar_Games_ML_v4.3/
├── app/
│   ├── main.py                          # View: MainWindow (1914 lines)
│   │   └─ Delegates lifecycle to ApplicationController
│   │
│   ├── core/
│   │   ├── application_controller.py    # Controller (341 lines) ⭐ NEW v4.3.1
│   │   │   ├─ Timer management
│   │   │   ├─ State synchronization
│   │   │   └─ Lifecycle coordination
│   │   ├── config.py                    # Model: Configuration
│   │   └── logger.py                    # Model: Logging
│   │
│   ├── audio/
│   │   ├── engine.py                    # Model: Audio capture
│   │   └── processor.py                 # Model: Audio processing
│   │
│   ├── detection/
│   │   ├── worker.py                    # Model: Detection worker
│   │   └── spectral.py                  # Model: Spectral analysis
│   │
│   ├── ui/
│   │   ├── builder.py                   # View: UI construction
│   │   └── event_handlers.py            # View: Event delegation ⭐ v4.3.1
│   │
│   └── widgets/
│       ├── radar.py                     # View: Radar display
│       └── device_panel.py              # View: Settings panel
│
└── docs/
    └── MVC_ARCHITECTURE.md              # This document ⭐ v4.3.1
```

---

## Implementation Examples

### Example 1: Starting Audio Capture

**Before v4.3.1 (Monolithic):**
```python
# main.py - Everything in MainWindow
def start(self):
    self.dev_panel.apply_settings()
    self.audio.start()
    self.is_running = True
    self.record_btn.setEnabled(True)
    self.start_btn.setText("⏹ STOP")
    # ... more UI updates ...
```

**After v4.3.1 (MVC):**
```python
# main.py - View delegates to Controller
def start(self):
    """Start audio capture (v4.3.1: Delegated to Controller)"""
    self.controller.start()

# core/application_controller.py - Controller coordinates
def start(self):
    """Start audio capture and detection"""
    log("Starting audio capture", "INFO")

    # Configure and start model
    self.window.dev_panel.apply_settings()
    self.window.audio.start()

    # Synchronize state
    self.is_running = True
    self.window.is_running = True
    self.window.record_btn.setEnabled(True)

    # Update view
    self._update_start_button_ui(running=True)
    self.window.dev_panel.update_audio_init_status(True, False)

    log("Audio capture started successfully", "INFO")
```

**Benefits:**
- ✅ Clear separation: Model (audio), View (UI), Controller (coordination)
- ✅ Testable: Can test controller logic without Qt
- ✅ Maintainable: Logic centralized in controller

---

### Example 2: Main Loop (Tick)

**Before v4.3.1:**
```python
# main.py - MainWindow owns timer
def __init__(self):
    self.tick_timer = QTimer()
    self.tick_timer.timeout.connect(self.tick)
    self.tick_timer.start(50)

def tick(self):
    # Mix of model and view code
    block = self.audio.get_block()
    events = self.detect(block)
    self.update_ui(events)
```

**After v4.3.1:**
```python
# core/application_controller.py - Controller owns timers
def __init__(self, main_window):
    self.window = main_window
    self._setup_timers()

def _setup_timers(self):
    self.tick_timer = QTimer()
    self.tick_timer.timeout.connect(self.tick)
    # Timer started later in start_timers()

def tick(self):
    """Main update loop - 20 FPS (50ms interval)."""
    # v4.3.1: Delegate to window.tick() for now
    # Allows incremental refactoring without breaking functionality
    self.window.tick()
```

**Migration Strategy:**
- ✅ **Phase 1:** Controller owns timer (DONE)
- ⏳ **Phase 2:** Extract tick logic from window to controller
- ⏳ **Phase 3:** Pure controller tick (no window dependency)

---

## Best Practices

### DO ✅

1. **Delegate lifecycle to Controller**
   ```python
   # main.py
   def start(self):
       self.controller.start()  # ✅ Delegate to controller
   ```

2. **Keep Model UI-agnostic**
   ```python
   # audio/engine.py
   def start(self) -> None:
       self.running = True
       self._start_loopback()  # ✅ No Qt dependencies
   ```

3. **Synchronize state through Controller**
   ```python
   # core/application_controller.py
   def start(self):
       self.is_running = True
       self.window.is_running = True  # ✅ Keep in sync
   ```

4. **Use EventHandlers for UI events**
   ```python
   # ui/event_handlers.py
   def toggle_start_stop(self):
       self.window.start()  # ✅ Centralized event logic
   ```

---

### DON'T ❌

1. **Don't put business logic in View**
   ```python
   # main.py - BAD ❌
   def start(self):
       self.audio.running = True  # ❌ Direct model manipulation
       self.audio.thread.start()  # ❌ Implementation details
   ```

2. **Don't put UI code in Model**
   ```python
   # audio/engine.py - BAD ❌
   def start(self):
       self.status_label.setText("Running")  # ❌ UI dependency
   ```

3. **Don't skip Controller**
   ```python
   # ui/event_handlers.py - BAD ❌
   def toggle_start_stop(self):
       self.window.audio.start()  # ❌ Bypass controller
   ```

4. **Don't duplicate state**
   ```python
   # BAD ❌
   self.controller.is_running = True
   self.window.is_running = False  # ❌ Inconsistent!
   ```

---

## Migration Guide

### For New Features

When adding new features:

1. **Identify component type**
   - Business logic → Model (`app/core/`, `app/audio/`, etc.)
   - UI presentation → View (`app/main.py`, `app/widgets/`)
   - Coordination → Controller (`app/core/application_controller.py`)

2. **Implement with delegation**
   ```python
   # View
   def new_feature_button_clicked(self):
       self.controller.new_feature()

   # Controller
   def new_feature(self):
       result = self.window.model.process()
       self.window.update_feature_ui(result)
   ```

3. **Test in isolation**
   ```python
   # tests/core/test_application_controller.py
   def test_new_feature():
       mock_window = MockMainWindow()
       controller = ApplicationController(mock_window)
       controller.new_feature()
       assert mock_window.feature_called
   ```

---

### Refactoring Existing Code

**Step 1:** Identify code to extract
```python
# Find methods in MainWindow that:
- Coordinate between multiple components
- Manage application lifecycle
- Don't directly manipulate UI widgets
```

**Step 2:** Move to ApplicationController
```python
# Before (main.py)
def scan_games(self):
    games = self.game_detector.scan()
    self.update_game_ui(games)

# After (core/application_controller.py)
def scan_games(self):
    games = self.window.game_detector.scan()
    self.window.update_game_ui(games)

# Update (main.py)
def scan_games(self):
    self.controller.scan_games()  # Delegate
```

**Step 3:** Update timer ownership
```python
# Before (main.py __init__)
self.game_timer = QTimer()
self.game_timer.timeout.connect(self.scan_games)
self.game_timer.start(5000)

# After (core/application_controller.py)
def _setup_timers(self):
    self.game_scan_timer = QTimer()
    self.game_scan_timer.timeout.connect(self.scan_games)

def start_timers(self):
    self.game_scan_timer.start(GAME_SCAN_INTERVAL_MS)
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-14 | Initial documentation for v4.3.1 MVC architecture |

---

## References

- **SPRINT 2.1:** ApplicationController Foundation
- **v4.3.1 Changelog:** MVC Integration Phase 1-2
- **Code:** `app/core/application_controller.py` (341 lines)
- **Tests:** `tests/core/test_application_controller.py` (planned ULEPSZENIE #5)

---

**Document maintained by:** Radar Games ML Development Team
**Last updated:** 2025-12-14
