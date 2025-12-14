"""
Unit Tests for ApplicationController (v4.3.1 ULEPSZENIE #5)

Tests MVC business logic without requiring full Qt GUI initialization.
Uses mock objects to isolate controller from view dependencies.
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from PyQt6.QtCore import QTimer
except ImportError:
    from PyQt5.QtCore import QTimer

from core.application_controller import ApplicationController


class MockMainWindow:
    """Mock MainWindow for testing without full GUI"""

    def __init__(self):
        # State
        self.is_running = False

        # Mock dependencies
        self.dev_panel = Mock()
        self.dev_panel.apply_settings = Mock()
        self.dev_panel.update_audio_init_status = Mock()
        self.dev_panel.rms_label = Mock()
        self.dev_panel.rms_label.setText = Mock()

        self.det_panel = Mock()
        self.det_panel.reset_detection = Mock()

        self.audio = Mock()
        self.audio.start = Mock()
        self.audio.stop = Mock()

        self.radar_widget = Mock()
        self.radar_widget.update_target = Mock()

        self.radar_3d_widget = Mock()
        self.radar_3d_widget.clear_targets = Mock()

        self.target_tracker = Mock()
        self.target_tracker.clear = Mock()

        self.record_btn = Mock()
        self.record_btn.setEnabled = Mock()

        self.start_btn = Mock()
        self.start_btn.setText = Mock()
        self.start_btn.setStyleSheet = Mock()

        self.game_detector = Mock()
        self.game_detector.scan = Mock(return_value=[])

        self.audio_scanner = Mock()
        self.audio_scanner.scan_audio_sources = Mock()

        # Track method calls
        self.tick_called = False
        self.scan_games_called = False
        self.scan_audio_called = False

    def tick(self):
        """Mock tick method"""
        self.tick_called = True

    def scan_games(self):
        """Mock scan_games method"""
        self.scan_games_called = True

    def scan_audio_sources(self):
        """Mock scan_audio_sources method"""
        self.scan_audio_called = True


class TestApplicationController(unittest.TestCase):
    """Test ApplicationController business logic"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_window = MockMainWindow()
        self.controller = ApplicationController(self.mock_window)

    def tearDown(self):
        """Clean up after tests"""
        self.controller.stop_timers()

    # =========================================================================
    # INITIALIZATION TESTS
    # =========================================================================

    def test_initialization(self):
        """Test that controller initializes properly"""
        self.assertIsNotNone(self.controller.window)
        self.assertEqual(self.controller.is_running, False)
        self.assertIsNotNone(self.controller.tick_timer)
        self.assertIsNotNone(self.controller.game_scan_timer)
        self.assertIsNotNone(self.controller.audio_scan_timer)

    def test_timers_created(self):
        """Test that all timers are created"""
        self.assertIsInstance(self.controller.tick_timer, QTimer)
        self.assertIsInstance(self.controller.game_scan_timer, QTimer)
        self.assertIsInstance(self.controller.audio_scan_timer, QTimer)

    # =========================================================================
    # START/STOP TESTS
    # =========================================================================

    def test_start_audio_capture(self):
        """Test that start() initiates audio capture"""
        self.controller.start()

        # Verify audio.start() was called
        self.mock_window.audio.start.assert_called_once()

        # Verify state is synchronized
        self.assertTrue(self.controller.is_running)
        self.assertTrue(self.mock_window.is_running)

        # Verify UI updates
        self.mock_window.dev_panel.apply_settings.assert_called_once()
        self.mock_window.dev_panel.update_audio_init_status.assert_called()
        self.mock_window.record_btn.setEnabled.assert_called_with(True)

    def test_stop_audio_capture(self):
        """Test that stop() terminates audio capture"""
        # Start first
        self.controller.start()

        # Then stop
        self.controller.stop()

        # Verify audio.stop() was called
        self.mock_window.audio.stop.assert_called_once()

        # Verify state is synchronized
        self.assertFalse(self.controller.is_running)
        self.assertFalse(self.mock_window.is_running)

        # Verify UI updates
        self.mock_window.det_panel.reset_detection.assert_called_once()
        self.mock_window.radar_widget.update_target.assert_called()
        self.mock_window.radar_3d_widget.clear_targets.assert_called_once()
        self.mock_window.target_tracker.clear.assert_called_once()

    def test_state_synchronization(self):
        """Test that controller and window state stay in sync"""
        # Initial state
        self.assertEqual(self.controller.is_running, self.mock_window.is_running)

        # After start
        self.controller.start()
        self.assertEqual(self.controller.is_running, self.mock_window.is_running)
        self.assertTrue(self.controller.is_running)

        # After stop
        self.controller.stop()
        self.assertEqual(self.controller.is_running, self.mock_window.is_running)
        self.assertFalse(self.controller.is_running)

    # =========================================================================
    # TIMER TESTS
    # =========================================================================

    def test_start_timers(self):
        """Test that start_timers() activates all timers"""
        self.controller.start_timers()

        # All timers should be active
        self.assertTrue(self.controller.tick_timer.isActive())
        self.assertTrue(self.controller.game_scan_timer.isActive())
        self.assertTrue(self.controller.audio_scan_timer.isActive())

    def test_stop_timers(self):
        """Test that stop_timers() deactivates all timers"""
        self.controller.start_timers()
        self.controller.stop_timers()

        # All timers should be inactive
        self.assertFalse(self.controller.tick_timer.isActive())
        self.assertFalse(self.controller.game_scan_timer.isActive())
        self.assertFalse(self.controller.audio_scan_timer.isActive())

    def test_tick_delegates_to_window(self):
        """Test that tick() delegates to window.tick()"""
        self.controller.tick()

        # Verify window.tick() was called
        self.assertTrue(self.mock_window.tick_called)

    def test_scan_games_delegates_to_window(self):
        """Test that scan_games() delegates to window"""
        self.controller.scan_games()

        # Verify window method was called
        self.assertTrue(self.mock_window.scan_games_called)

    def test_scan_audio_sources_delegates_to_window(self):
        """Test that scan_audio_sources() delegates to window"""
        self.controller.scan_audio_sources()

        # Verify window method was called
        self.assertTrue(self.mock_window.scan_audio_called)

    # =========================================================================
    # CLEANUP TESTS
    # =========================================================================

    def test_cleanup_stops_timers_and_audio(self):
        """Test that cleanup() stops timers and audio"""
        self.controller.start()
        self.controller.start_timers()

        # Cleanup
        self.controller.cleanup()

        # Verify audio stopped
        self.mock_window.audio.stop.assert_called()

        # Verify timers stopped
        self.assertFalse(self.controller.tick_timer.isActive())

    # =========================================================================
    # UI UPDATE TESTS
    # =========================================================================

    def test_update_start_button_ui_running(self):
        """Test that start button UI updates when running"""
        self.controller._update_start_button_ui(running=True)

        # Verify button text changed
        self.mock_window.start_btn.setText.assert_called()
        call_args = self.mock_window.start_btn.setText.call_args[0][0]
        self.assertIn("STOP", call_args)

    def test_update_start_button_ui_stopped(self):
        """Test that start button UI updates when stopped"""
        self.controller._update_start_button_ui(running=False)

        # Verify button text changed
        self.mock_window.start_btn.setText.assert_called()
        call_args = self.mock_window.start_btn.setText.call_args[0][0]
        # Should contain START or similar
        self.assertTrue("START" in call_args or "▶" in call_args)


class TestApplicationControllerIntegration(unittest.TestCase):
    """Integration tests for ApplicationController"""

    def setUp(self):
        """Set up integration test fixtures"""
        self.mock_window = MockMainWindow()
        self.controller = ApplicationController(self.mock_window)

    def tearDown(self):
        """Clean up after integration tests"""
        self.controller.cleanup()

    def test_full_lifecycle(self):
        """Test complete start → run → stop lifecycle"""
        # 1. Start timers
        self.controller.start_timers()
        self.assertTrue(self.controller.tick_timer.isActive())

        # 2. Start audio
        self.controller.start()
        self.assertTrue(self.controller.is_running)
        self.mock_window.audio.start.assert_called_once()

        # 3. Stop audio
        self.controller.stop()
        self.assertFalse(self.controller.is_running)
        self.mock_window.audio.stop.assert_called_once()

        # 4. Cleanup
        self.controller.cleanup()
        self.assertFalse(self.controller.tick_timer.isActive())

    def test_multiple_start_stop_cycles(self):
        """Test that multiple start/stop cycles work correctly"""
        for i in range(3):
            self.controller.start()
            self.assertTrue(self.controller.is_running)

            self.controller.stop()
            self.assertFalse(self.controller.is_running)

        # Verify correct number of calls
        self.assertEqual(self.mock_window.audio.start.call_count, 3)
        self.assertEqual(self.mock_window.audio.stop.call_count, 3)


# Run tests
if __name__ == '__main__':
    unittest.main(verbosity=2)
