# RadarSuite v4.2.1 - API Documentation

> ADDED v4.2.1: ZADANIE 7 - Comprehensive API documentation for key modules

## Table of Contents

1. [Core Module](#core-module)
2. [Audio Module](#audio-module)
3. [Widgets Module](#widgets-module)
4. [Utils Module](#utils-module)
5. [ML Module](#ml-module)

---

## Core Module

### ConfigManager

Configuration management with validation and persistence.

```python
from app.core.config import ConfigManager

config_manager = ConfigManager()
```

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `load()` | - | `Dict[str, Any]` | Load configuration from disk with validation |
| `save(config)` | `config: Dict` | `None` | Save configuration to disk |
| `get(section, key, default)` | `section: str, key: str, default=None` | `Any` | Get config value |
| `set(section, key, value, config)` | `section: str, key: str, value: Any, config: dict=None` | `dict` | Set config value |
| `save_window_state(window, config)` | `window: QMainWindow, config: dict=None` | `dict` | Save window geometry |
| `restore_window_state(window, config)` | `window: QMainWindow, config: dict=None` | `None` | Restore window geometry |

#### Configuration Schema

```python
CONFIG_SCHEMA = {
    "audio": {
        "device": {"type": (None, int, str)},
        "sample_rate": {"type": int, "values": [8000, 16000, 22050, 44100, 48000, 96000]},
        "block_size": {"type": int, "range": (128, 8192)},
        "channels": {"type": int, "values": [1, 2]},
        "loopback": {"type": bool},
        "gain": {"type": (int, float), "range": (0.1, 100.0)},
        "auto_gain": {"type": bool},
        "noise_gate": {"type": (int, float), "range": (-120.0, 0.0)}
    },
    "detection": {
        "walk_threshold": {"type": (int, float), "range": (0, 100)},
        "run_threshold": {"type": (int, float), "range": (0, 100)},
        "shot_threshold": {"type": (int, float), "range": (0, 100)},
        "walk_enabled": {"type": bool},
        "run_enabled": {"type": bool},
        "shot_enabled": {"type": bool}
    },
    "ui": {
        "language": {"type": str, "values": ["en", "pl"]},
        "radar_alpha": {"type": int, "range": (0, 100)},
        "led_alpha": {"type": int, "range": (0, 100)}
    }
}
```

---

### Translations

Localization system for EN/PL support.

```python
from app.core.translations import tr, set_language, get_language

# Get translated string
label = tr('app_title')  # Returns "RadarSuite Final"

# Switch language
set_language('pl')

# Get current language
current = get_language()  # Returns 'pl'
```

---

### ExportImportManager

Export/import configuration, models, and sessions.

```python
from app.core.export_import import ExportImportManager

manager = ExportImportManager(config_manager=config_mgr)
```

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `export_config(config, file_path)` | `config: Dict, file_path: str` | `ExportResult` | Export config to .rscfg |
| `import_config(file_path)` | `file_path: str` | `Tuple[ImportResult, Dict]` | Import config from .rscfg |
| `export_model(model_path, output_path, metadata)` | `model_path: str, output_path: str, metadata: Dict=None` | `ExportResult` | Export ML model to .rsmodel |
| `import_model(file_path, output_dir)` | `file_path: str, output_dir: str` | `Tuple[ImportResult, str]` | Import ML model |
| `export_session(session_id, output_path)` | `session_id: str, output_path: str` | `ExportResult` | Export training session |
| `import_session(file_path)` | `file_path: str` | `ImportResult` | Import training session |

#### File Formats

| Extension | Type | Description |
|-----------|------|-------------|
| `.rscfg` | JSON | Configuration file with validation header |
| `.rsmodel` | ZIP | ML model with metadata.json |
| `.rssession` | ZIP | Training session with audio data |

---

## Audio Module

### AudioEngine

Main audio processing engine.

```python
from app.audio.engine import AudioEngine

engine = AudioEngine(
    sample_rate=48000,
    block_size=2048,
    channels=2
)
```

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `start()` | - | `bool` | Start audio capture |
| `stop()` | - | `None` | Stop audio capture |
| `get_block()` | - | `np.ndarray` | Get current audio block |
| `set_device(device_id)` | `device_id: int` | `bool` | Set capture device |
| `set_gain(gain)` | `gain: float` | `None` | Set input gain |
| `set_noise_gate(threshold_db)` | `threshold_db: float` | `None` | Set noise gate |

---

### SoundClassifier

Audio event classification.

```python
from app.audio.classifier import SoundClassifier

classifier = SoundClassifier()
```

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `classify(audio_block)` | `audio_block: np.ndarray` | `Dict[str, float]` | Classify audio into categories |
| `detect_footsteps(audio_block)` | `audio_block: np.ndarray` | `Tuple[bool, float]` | Detect footstep sounds |
| `detect_gunshot(audio_block)` | `audio_block: np.ndarray` | `Tuple[bool, float]` | Detect gunshot sounds |

#### Output Format

```python
{
    'walk': 0.85,      # Walking footsteps confidence
    'run': 0.12,       # Running footsteps confidence
    'shot': 0.03,      # Gunshot confidence
    'ambient': 0.0     # Ambient noise
}
```

---

## Widgets Module

### WaveformTimelineWidget

Interactive waveform visualization with zoom/scroll.

```python
from app.widgets.waveform_timeline import WaveformTimelineWidget

timeline = WaveformTimelineWidget()
timeline.set_audio_data(audio_array, sample_rate=48000)
```

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `set_audio_data(audio_data, sample_rate)` | `audio_data: np.ndarray, sample_rate: int` | `None` | Set audio for visualization |
| `set_markers(markers)` | `markers: List[Tuple[float, str]]` | `None` | Set label markers |
| `set_playhead(timestamp_sec)` | `timestamp_sec: float` | `None` | Set playback position |
| `get_selection()` | - | `Tuple[float, float]` | Get current selection |
| `clear_selection()` | - | `None` | Clear selection |

#### Signals

| Signal | Parameters | Description |
|--------|------------|-------------|
| `segment_selected` | `start_sec: float, end_sec: float` | Emitted when segment is selected |
| `timestamp_clicked` | `timestamp_sec: float` | Emitted when position is clicked |

---

### MLTrainingPanel

ML training UI panel.

```python
from app.widgets.ml_training_panel import MLTrainingPanel

panel = MLTrainingPanel(parent=main_window)
```

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `feed_audio(block)` | `block: np.ndarray` | `None` | Feed audio data to recorder |

#### Hotkeys

| Key | Action |
|-----|--------|
| `1-8` | Quick add label by class index |
| `Backspace` | Remove last label |

---

## Utils Module

### PerformanceMonitor

Real-time performance tracking.

```python
from app.utils.performance import PerformanceMonitor

monitor = PerformanceMonitor()
```

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `start_frame()` | - | `None` | Mark frame start |
| `end_frame()` | - | `None` | Mark frame end |
| `update()` | - | `None` | Update metrics |
| `get_stats()` | - | `Dict` | Get current stats |

#### Output Format

```python
{
    'fps': 60.0,
    'cpu_percent': 15.5,
    'memory_mb': 256.0,
    'latency_ms': 12.5
}
```

---

### MemoryOptimizer

Memory profiling and optimization.

```python
from app.utils.performance import MemoryOptimizer

optimizer = MemoryOptimizer(enable_profiling=False)
```

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `take_snapshot()` | - | `MemorySnapshot` | Take memory snapshot |
| `check_memory()` | - | `Optional[str]` | Check memory and return warning if high |
| `get_stats()` | - | `MemoryStats` | Get memory statistics |
| `detect_leaks()` | - | `List[str]` | Detect growing object counts |
| `get_buffer(pool_name, shape, dtype)` | `pool_name: str, shape: tuple, dtype` | `np.ndarray` | Get buffer from pool |
| `return_buffer(pool_name, buffer)` | `pool_name: str, buffer: np.ndarray` | `None` | Return buffer to pool |
| `optimize_gc_for_realtime()` | - | `None` | Disable GC for real-time |
| `restore_gc()` | - | `None` | Restore normal GC |
| `cleanup()` | - | `None` | Cleanup resources |

#### Constants

```python
MEMORY_WARNING_MB = 500     # Warning threshold
MEMORY_CRITICAL_MB = 1000   # Critical threshold (triggers GC)
GC_FORCE_THRESHOLD_MB = 800 # Force GC threshold
```

---

## ML Module

### SessionManager

Manage training sessions.

```python
from app.ml.training import SessionManager

manager = SessionManager()
```

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `create_session()` | - | `LabeledSession` | Create new session |
| `load_session(session_id)` | `session_id: str` | `LabeledSession` | Load existing session |
| `list_sessions()` | - | `List[Dict]` | List all sessions |
| `delete_session(session_id)` | `session_id: str` | `bool` | Delete session |

---

### LabeledRecorder

Record and label audio.

```python
from app.ml.training import LabeledRecorder

recorder = LabeledRecorder(session_manager)
recorder.start_recording()
```

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `start_recording()` | - | `bool` | Start recording |
| `stop_recording()` | - | `LabeledSession` | Stop and save session |
| `add_audio_block(block)` | `block: np.ndarray` | `None` | Add audio data |
| `add_label(label_class, description)` | `label_class: str, description: str` | `AudioLabel` | Add label |
| `add_label_with_hotkey(hotkey)` | `hotkey: int` | `AudioLabel` | Add label by hotkey |
| `remove_last_label()` | - | `bool` | Remove last label |

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `is_recording` | `bool` | Recording state |
| `elapsed_seconds` | `float` | Recording duration |
| `current_session` | `LabeledSession` | Active session |

---

### ModelTrainer

Train ML models from sessions.

```python
from app.ml.training import ModelTrainer

trainer = ModelTrainer(session_manager)
trainer.start_training()
```

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `start_training()` | - | `None` | Start training in background |
| `cancel_training()` | - | `None` | Cancel training |
| `set_callbacks(on_progress, on_complete, on_log)` | callbacks | `None` | Set event callbacks |

---

## Data Classes

### AudioLabel

```python
@dataclass
class AudioLabel:
    id: int
    timestamp_sec: float
    label_class: str
    description: str = ""
```

### MemorySnapshot

```python
@dataclass
class MemorySnapshot:
    timestamp: float
    rss_mb: float
    vms_mb: float
    percent: float
    gc_objects: int
    numpy_arrays: int = 0
    numpy_mb: float = 0.0
```

### ExportResult

```python
@dataclass
class ExportResult:
    success: bool
    file_path: Optional[str] = None
    error_message: Optional[str] = None
    items_exported: int = 0
```

### ImportResult

```python
@dataclass
class ImportResult:
    success: bool
    error_message: Optional[str] = None
    items_imported: int = 0
    warnings: List[str] = None
```

---

## Constants

### Audio Constants

```python
SAMPLE_RATE = 48000          # Default sample rate
BLOCK_SIZE = 2048            # Default block size
CHANNELS = 2                 # Default channels
ENERGY_THRESHOLD = 0.01      # Minimum energy for detection
```

### UI Constants

```python
TICK_INTERVAL_MS = 50        # UI update interval
TOAST_DURATION_MS = 3000     # Toast notification duration
TOAST_MAX_COUNT = 3          # Maximum visible toasts
```

### Detection Constants

```python
DETECTION_TIMEOUT_SEC = 2.0  # Target timeout
CLEANUP_INTERVAL_SEC = 1.0   # Cleanup interval
LOCALIZATION_MIN_CONFIDENCE = 0.3  # Minimum confidence for localization
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v4.2.1 | 2024-12 | Added WaveformTimelineWidget, ExportImportManager, MemoryOptimizer |
| v4.2.0 | 2024-12 | Added MLTrainingPanel, refactored AudioProcessor |
| v4.1.0 | 2024-11 | UI improvements, 3D radar enhancements |
| v4.0.0 | 2024-11 | Major architecture refactoring |
