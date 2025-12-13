"""
Radar Games ML v4.3.1 - Application Controller
ADDED v4.3.1: MVC Pattern - Controller Layer (SPRINT 2.1)

Extracted from MainWindow (2080 lines) to implement MVC architecture.
Handles application lifecycle, processing loop, and business logic coordination.

Architecture:
- Model: Audio, Detection, Tracking modules (existing)
- View: MainWindow, UIBuilder, widgets (existing)
- Controller: ApplicationController (new) - coordinates Model and View

Responsibilities:
- Application lifecycle (start/stop/tick)
- Audio processing coordination
- Detection and tracking coordination
- Timer management
- UI update orchestration
- Game/audio source scanning
"""

import time
import numpy as np
from typing import Optional, Dict, Any, List, Tuple
from PyQt5.QtCore import QTimer

from .logger import log
from .constants import (
    TICK_INTERVAL_MS,
    GAME_SCAN_INTERVAL_MS,
    AUDIO_SCAN_INTERVAL_MS,
    STARTUP_DELAY_MS,
    STARTUP_AUDIO_DELAY_MS,
    RADAR_ROTATION_DEG,
    DETECTION_TIMEOUT_SEC,
)


class ApplicationController:
    """
    Application Controller - MVC Pattern (v4.3.1)

    Coordinates between Model (audio/detection/tracking) and View (MainWindow/UI).
    Extracted from MainWindow to reduce complexity and improve testability.

    The controller owns the main processing loop and application lifecycle,
    while MainWindow is reduced to just UI presentation and event delegation.
    """

    def __init__(self, main_window):
        """
        Initialize Application Controller.

        Args:
            main_window: MainWindow instance (provides access to view and dependencies)
        """
        self.window = main_window
        log("ApplicationController initialized", "INFO")

        # Processing state
        self.is_running = False
        self.radar_angle = 0.0
        self.test_phase = 0.0

        # Setup timers
        self._setup_timers()

    def _setup_timers(self):
        """Setup application timers for periodic tasks."""
        # Main update timer (20 FPS)
        self.tick_timer = QTimer()
        self.tick_timer.timeout.connect(self.tick)

        # Game detection timer (scan every 5 seconds)
        self.game_scan_timer = QTimer()
        self.game_scan_timer.timeout.connect(self.scan_games)

        # Audio source scan timer (scan every 2 seconds)
        self.audio_scan_timer = QTimer()
        self.audio_scan_timer.timeout.connect(self.scan_audio_sources)

        log("Application timers initialized", "DEBUG")

    def start_timers(self):
        """Start all application timers."""
        self.tick_timer.start(TICK_INTERVAL_MS)
        self.game_scan_timer.start(GAME_SCAN_INTERVAL_MS)
        self.audio_scan_timer.start(AUDIO_SCAN_INTERVAL_MS)

        # Initial scans with delay
        QTimer.singleShot(STARTUP_DELAY_MS, self.scan_games)
        QTimer.singleShot(STARTUP_AUDIO_DELAY_MS, self.scan_audio_sources)

        log("Application timers started", "INFO")

    def stop_timers(self):
        """Stop all application timers."""
        if self.tick_timer:
            self.tick_timer.stop()
        if self.game_scan_timer:
            self.game_scan_timer.stop()
        if self.audio_scan_timer:
            self.audio_scan_timer.stop()

        log("Application timers stopped", "INFO")

    # ========================================================================
    # APPLICATION LIFECYCLE
    # ========================================================================

    def start(self):
        """
        Start audio capture and detection.

        Delegates to view for UI updates.
        """
        log("Starting audio capture", "INFO")

        self.window.dev_panel.apply_settings()
        self.window.audio.start()

        # v4.3.1 SPRINT 2.1: Sync state with window
        self.is_running = True
        self.window.is_running = True
        self.window.record_btn.setEnabled(True)

        # Update audio status indicator
        self.window.dev_panel.update_audio_init_status(True, False)

        # Update UI through window
        self._update_start_button_ui(running=True)

        log("Audio capture started successfully", "INFO")

    def stop(self):
        """
        Stop audio capture and detection.

        Delegates to view for UI updates.
        """
        log("Stopping audio capture", "INFO")

        self.window.audio.stop()

        # v4.3.1 SPRINT 2.1: Sync state with window
        self.is_running = False
        self.window.is_running = False

        # Update audio status indicator
        self.window.dev_panel.update_audio_init_status(False, False)

        # Reset detection labels and clear radars on stop
        self.window.det_panel.reset_detection()
        self.window.radar_widget.update_target(None, None)
        self.window.radar_3d_widget.clear_targets()
        self.window.target_tracker.clear()
        self.window.dev_panel.rms_label.setText("RMS: --- dBFS")

        # Update UI through window
        self._update_start_button_ui(running=False)

        log("Audio capture stopped successfully", "INFO")

    def _update_start_button_ui(self, running: bool):
        """Update start/stop button UI state."""
        from core.translations import get_language

        if running:
            self.window.start_btn.setText("⏹ STOP")
            self.window.start_btn.setStyleSheet("""
                QPushButton {
                    background: #aa0000;
                    color: white;
                    font-weight: bold;
                    padding: 8px 20px;
                    border-radius: 4px;
                    font-size: 11pt;
                }
                QPushButton:hover {
                    background: #cc0000;
                }
            """)
            msg = "● RUNNING - Detection active" if get_language() == 'en' else "● DZIAŁA - Detekcja aktywna"
        else:
            self.window.start_btn.setText("▶ START")
            self.window.start_btn.setStyleSheet("""
                QPushButton {
                    background: #00aa00;
                    color: white;
                    font-weight: bold;
                    padding: 8px 20px;
                    border-radius: 4px;
                    font-size: 11pt;
                }
                QPushButton:hover {
                    background: #00cc00;
                }
            """)
            msg = "✓ Stopped - Ready to start" if get_language() == 'en' else "✓ Zatrzymano - Gotowy do startu"

        self.window.status_bar.showMessage(msg)

    # ========================================================================
    # MAIN PROCESSING LOOP (TICK)
    # ========================================================================

    def tick(self):
        """
        Main update loop - 20 FPS (50ms interval).

        v4.3.1 SPRINT 2.1: Delegates to MainWindow.tick() for now.
        Future: Move all processing logic into controller.

        Orchestrates:
        1. Radar sweep animation
        2. Audio acquisition and processing
        3. Detection and tracking
        4. UI updates
        """
        # v4.3.1 SPRINT 2.1: Delegate to window.tick() for full implementation
        # This allows incremental refactoring without breaking existing functionality
        self.window.tick()

    def _update_radar_sweep(self):
        """Update radar sweep angle and all radar widgets."""
        self.radar_angle = (self.radar_angle + RADAR_ROTATION_DEG) % 360.0
        self.window.radar_widget.update_sweep(self.radar_angle)
        self.window.radar_3d_widget.update_sweep(self.radar_angle)
        self.window._safe_update_detached_radar('update_sweep', self.radar_angle)

    def _acquire_audio_block(self) -> Optional[np.ndarray]:
        """
        Acquire audio block from queue.

        Returns:
            Audio block or None if queue is empty
        """
        try:
            block = self.window.audio.block_queue.get_nowait()
            return block
        except:
            return None

    def _update_recording(self, block: np.ndarray):
        """Update audio recording if active."""
        if self.window.audio_recorder.is_recording:
            self.window.audio_recorder.add_block(block)

    def _process_audio(self, block: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Process audio block (FFT, energy).

        Returns:
            Tuple of (fft_result, energy)
        """
        # Delegate to window's existing methods for now
        # TODO: Move to audio processor in future refactoring
        fft_result = self.window.apply_audio_processing(block)

        # Calculate energy
        energy = float(np.sqrt(np.mean(block ** 2)))

        return fft_result, energy

    def _process_audio_visualizations(self, block: np.ndarray, fft_result: np.ndarray):
        """Update audio visualization widgets."""
        # Spectrum
        self.window.spectrum_widget.update_data(fft_result)
        self.window.mil_spectrum_widget.update_spectrum(fft_result)

        # Waterfall
        self.window.waterfall_widget.update_data(fft_result)
        self.window.mil_waterfall_widget.add_spectrum(fft_result)

        # Waveform
        self.window.waveform_widget.update_data(block)
        self.window.mil_waveform_widget.update_waveform(block)

    def _process_audio_level_monitoring(self, energy: float):
        """Process and display audio level monitoring."""
        # Calculate RMS in dBFS
        if energy > 0:
            rms_dbfs = 20 * np.log10(energy)
        else:
            rms_dbfs = -120.0

        # Update RMS label
        self.window.dev_panel.rms_label.setText(f"RMS: {rms_dbfs:.1f} dBFS")

        # Update LED based on level
        from core.constants import AUDIO_LEVEL_LOUD, AUDIO_LEVEL_MEDIUM, AUDIO_LEVEL_LOW

        if rms_dbfs > AUDIO_LEVEL_LOUD:
            color = 'red'
        elif rms_dbfs > AUDIO_LEVEL_MEDIUM:
            color = 'yellow'
        elif rms_dbfs > AUDIO_LEVEL_LOW:
            color = 'green'
        else:
            color = 'gray'

        self.window.dev_panel.rms_label.setStyleSheet(f"color: {color}; font-weight: bold;")

    def _process_detection_and_tracking(self, block: np.ndarray, fft_result: np.ndarray, energy: float):
        """
        Process detection and tracking (main business logic).

        This is delegated to window for now as it's complex.
        TODO: Further refactor this in future iterations.
        """
        # Delegate to existing window method
        self.window._process_detection_and_tracking(block, fft_result, energy)

    # ========================================================================
    # SCANNING METHODS
    # ========================================================================

    def scan_games(self):
        """Scan for running games and update UI - delegated to window."""
        self.window.scan_games()

    def scan_audio_sources(self):
        """Scan audio sources and update UI - delegated to window."""
        self.window.scan_audio_sources()

    # ========================================================================
    # CLEANUP
    # ========================================================================

    def cleanup(self):
        """Cleanup controller resources."""
        log("ApplicationController cleanup starting", "INFO")

        # Stop processing
        if self.is_running:
            self.stop()

        # Stop timers
        self.stop_timers()

        log("ApplicationController cleanup complete", "INFO")
