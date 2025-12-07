"""
RadarSuite v3.5.0 - Constants Module
All application constants extracted for maintainability (FIX 9)
"""

# ============================================================================
# VERSION
# ============================================================================

VERSION = "v3.5.0-Diamond-001"

# ============================================================================
# CONSTANTS (FIXED v3.5.0: Extracted magic numbers)
# ============================================================================

# Audio
SAMPLE_RATE = 48000  # Hz - Standard sample rate
BLOCK_SIZE = 2048    # Samples per block
CHANNELS = 2         # Stereo

# Performance
TICK_INTERVAL_MS = 50        # Main loop @ 20 FPS
GAME_SCAN_INTERVAL_MS = 5000  # Scan games every 5s
AUDIO_SCAN_INTERVAL_MS = 2000 # Scan audio every 2s
STARTUP_DELAY_MS = 500        # Initial scan delay
STARTUP_AUDIO_DELAY_MS = 1000 # Audio scan delay

# Detection
ENERGY_THRESHOLD = 0.00001    # Minimum energy for detection
RADAR_ROTATION_DEG = 4.0      # Degrees per frame

# Worker threads
MAX_WORKERS = 3              # Thread pool size
DETECTION_TIMEOUT_SEC = 5.0  # Worker shutdown timeout
CLEANUP_INTERVAL_SEC = 10.0  # Future cleanup interval

# Audio levels (dBFS)
AUDIO_LEVEL_LOUD = -20      # Green
AUDIO_LEVEL_MEDIUM = -40    # Yellow
AUDIO_LEVEL_LOW = -60       # Orange

# Recording (FIXED v3.5.0: Buffering to reduce I/O)
RECORDING_BUFFER_SIZE = 20   # Blocks before flush (1 sec @ 20 FPS)
RECORDING_FLUSH_INTERVAL = 1.0  # Seconds between flushes

# UI
TOAST_DURATION_MS = 3000     # Default toast display time
TOAST_MAX_COUNT = 3          # Max concurrent toasts
