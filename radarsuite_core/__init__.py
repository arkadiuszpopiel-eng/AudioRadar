"""
RadarSuite Core - Shared Module Package
========================================

This package contains platform-independent modules shared between
RadarSuite Windows and RadarSuite Linux versions.

Version: 4.2.0
Created: 2025-12-04

Modules:
--------
- detection: Audio detection algorithms (footstep, shot, spectral, ML)
- tracking: Target tracking and spatial positioning
- core: Core utilities (logger, confidence scoring)
- utils: Helper utilities

Usage:
------
This package is designed to be imported by platform-specific RadarSuite builds.
It does NOT include platform-specific audio capture code.

Example:
    from radarsuite_core.detection import footstep, shot, spectral
    from radarsuite_core.tracking import target
    from radarsuite_core.core import logger, confidence

Platform-Specific Modules (NOT included here):
----------------------------------------------
- app/audio/engine.py - Windows uses WASAPI, Linux uses PulseAudio/PipeWire
- app/version.py - Contains BUILD_PLATFORM constant
"""

__version__ = "4.2.0"
__author__ = "RadarSuite Team"
__platforms__ = ["Windows", "Linux"]

# Package-level imports for convenience
from . import detection
from . import tracking
from . import core
from . import utils
