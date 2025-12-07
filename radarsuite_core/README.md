# RadarSuite Core - Shared Module Package

Pakiet zawierający współdzielone moduły między wersjami Windows i Linux RadarSuite.

## Wersja
- **V4.2.0** - Synchronizacja z RadarSuite V4.2

## Struktura

```
radarsuite_core/
├── __init__.py              # Package init
├── setup.py                 # Pip installation script
├── README.md                # This file
├── core/                    # Core modules
│   ├── __init__.py          # Core package init with constants export
│   ├── constants.py         # Application constants
│   ├── config.py            # Configuration manager
│   ├── confidence.py        # Detection confidence scoring
│   ├── di.py                # Dependency injection container
│   ├── logger.py            # Thread-safe logger
│   └── translations.py      # Internationalization
├── detection/               # Detection algorithms
│   ├── __init__.py          # Detection package init
│   ├── footstep.py          # Human footstep detector
│   ├── shot.py              # Gunshot detector
│   ├── machine.py           # Machine learning detector
│   ├── spectral.py          # Spectral feature extractor
│   └── worker.py            # Detection worker thread
├── tracking/                # Target tracking
│   ├── __init__.py          # Tracking package init
│   ├── target.py            # Target tracker
│   └── threat.py            # Threat assessment
└── utils/                   # Utilities
    ├── __init__.py          # Utils package init
    ├── audio_scanner.py     # Audio device scanner
    ├── game_detector.py     # Game process detector
    ├── launcher.py          # Application launcher
    └── performance.py       # Performance monitoring
```

## Moduły platform-specificzne (NIE zawarte tutaj)

Te moduły muszą być implementowane osobno dla każdej platformy:

| Moduł | Windows | Linux |
|-------|---------|-------|
| `audio/engine.py` | WASAPI (pyaudiowpatch) | PulseAudio/PipeWire (soundcard, pw-record) |
| `version.py` | BUILD_PLATFORM="Windows" | BUILD_PLATFORM="Linux" |
| `widgets/*` | Niektóre mogą różnić się | Niektóre mogą różnić się |

## Użycie

### Instalacja dla developmentu

```bash
cd radarsuite_core
pip install -e .
```

### Import w kodzie

```python
# Importuj z radarsuite_core
from radarsuite_core.detection import footstep, shot, spectral
from radarsuite_core.tracking import target
from radarsuite_core.core import log, ConfigManager
from radarsuite_core.core.constants import SAMPLE_RATE, BLOCK_SIZE
```

### Synchronizacja z wersjami platformowymi

Moduły w `radarsuite_core` są kanonicznymi wersjami wspólnego kodu.
Aby zsynchronizować z wersją platformową:

```bash
# Kopiowanie do Windows
cp -r radarsuite_core/detection/* RadarSuite_Windows_V4.2/app/detection/
cp -r radarsuite_core/tracking/* RadarSuite_Windows_V4.2/app/tracking/
cp -r radarsuite_core/core/* RadarSuite_Windows_V4.2/app/core/
cp -r radarsuite_core/utils/* RadarSuite_Windows_V4.2/app/utils/

# Kopiowanie do Linux
cp -r radarsuite_core/detection/* RadarSuite_Linux_V4.2/app/detection/
cp -r radarsuite_core/tracking/* RadarSuite_Linux_V4.2/app/tracking/
cp -r radarsuite_core/core/* RadarSuite_Linux_V4.2/app/core/
cp -r radarsuite_core/utils/* RadarSuite_Linux_V4.2/app/utils/
```

## Importy wewnętrzne

Moduły w tym pakiecie używają importów relatywnych do `core` i innych modułów.
Jest to zgodne z strukturą w wersjach platformowych, gdzie `core`, `detection`,
`tracking` i `utils` są podkatalogami `app/`.

Przykład z `detection/footstep.py`:
```python
from core.logger import log
from core import FOOTSTEP_FREQ_MIN_HZ, FOOTSTEP_FREQ_MAX_HZ
from detection.spectral import SpectralFeatureExtractor
```

## Kompatybilność

- Python 3.11+
- NumPy 1.21+
- SciPy 1.7+
- psutil 5.9+

## Testowanie

```bash
cd radarsuite_core
pip install -e ".[dev]"
pytest
```

## Changelog

### V4.2.0 (2025-12-04)
- Utworzenie pakietu radarsuite_core
- Wydzielenie wspólnych modułów z Windows/Linux V4.2
- Dodanie setup.py dla pip install
- Dokumentacja migracji

## Licencja

MIT License - zgodnie z głównym projektem RadarSuite.
