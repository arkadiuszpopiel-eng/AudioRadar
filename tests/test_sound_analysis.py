"""Tests for sound_analysis module."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "audio_radar_v10" / "audio_radar"))

import numpy as np
import pytest

try:
    from sound_analysis import (
        detect_event,
        detect_event_with_direction,
        apply_bandpass_filter,
        estimate_distance,
        set_detection_config,
    )
except ImportError as e:
    pytest.skip(f"Could not import sound_analysis: {e}", allow_module_level=True)


class TestSoundAnalysis:
    """Test suite for sound analysis functions."""

    def test_detect_silent_audio(self):
        """Test that silent audio produces no events."""
        silent_audio = np.zeros((1024, 2), dtype=np.float32)
        result = detect_event(silent_audio)
        assert result is None

    def test_detect_loud_peak_as_shot(self):
        """Test that a loud peak is detected as a gunshot."""
        audio = np.zeros((1024, 2), dtype=np.float32)
        audio[512, :] = 0.8
        result = detect_event(audio)
        assert result == 'shot'

    def test_set_detection_config(self):
        """Test that detection configuration can be updated."""
        new_config = {
            "shot_peak_threshold": 0.5,
            "footstep_std_threshold": 0.1,
        }
        set_detection_config(new_config)

    def test_estimate_distance(self):
        """Test distance estimation from amplitude."""
        close_distance = estimate_distance(0.8, 0.01)
        far_distance = estimate_distance(0.1, 0.01)
        assert 0.0 <= close_distance <= 1.0
        assert 0.0 <= far_distance <= 1.0
        assert close_distance < far_distance


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
