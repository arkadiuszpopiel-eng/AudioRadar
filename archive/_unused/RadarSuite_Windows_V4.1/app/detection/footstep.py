"""
RadarSuite v3.5.0 - Human Footstep Detector
Advanced footstep pattern recognition
"""

import time
import numpy as np
from scipy import signal as sp_signal
from collections import deque

from core.logger import log


class HumanFootstepDetector:
    """
    Advanced human footstep pattern recognition
    Detects cadence, rhythm, weight distribution, and distinguishes human steps from other sounds

    FIXED v4.1.2: Added adaptive noise floor estimation to reduce false positives
    """

    def __init__(self):
        log("HumanFootstepDetector.__init__", "INFO")

        # Temporal analysis buffers
        self.step_history = []  # timestamps of detected steps
        self.max_history = 20   # keep last 20 steps

        # L-R pattern tracking
        self.lr_pattern = []    # left/right classification history
        self.max_lr_history = 10

        # Surface type detection
        self.surface_type = "unknown"
        self.surface_confidence = 0.0

        # Distance estimation
        self.estimated_distance = 0.0

        # Cadence parameters (steps per second)
        self.cadence_walk = (1.5, 2.5)   # 1.5-2.5 steps/sec for walking
        self.cadence_run = (3.0, 4.5)    # 3.0-4.5 steps/sec for running

        # Frequency ranges for human footsteps
        self.freq_impact = (60, 180)     # main impact (heel strike)
        self.freq_detail = (180, 400)    # shoe/surface detail
        self.freq_body = (20, 60)        # body weight shift

        # Pattern detection
        self.last_step_time = 0.0
        self.step_intervals = []
        self.max_intervals = 10

        # FIXED v4.1.2: Adaptive noise floor estimation
        self.noise_history = deque(maxlen=100)  # ~5 seconds of noise samples at 20fps
        self.noise_floor = 0.0
        self.noise_floor_impact = 0.0
        self.noise_floor_detail = 0.0
        self.noise_floor_body = 0.0

        # Base thresholds (will be adjusted based on noise floor)
        self.base_impact_threshold = 0.15
        self.base_detail_threshold = 0.05
        self.base_body_threshold = 0.02

        # Adaptive threshold multiplier (how much above noise floor to detect)
        self.threshold_multiplier = 1.5  # 1.5x above noise floor

        # Repetitive sound filter (for ambient like rain, fans)
        self.ambient_filter_history = deque(maxlen=50)
        self.ambient_variance_threshold = 0.05  # low variance = repetitive ambient

    def analyze_footstep(self, block, sample_rate, stereo=True):
        """
        Analyze audio block for human footstep patterns

        Returns:
            dict: {
                'is_human_step': bool,
                'confidence': float (0-100),
                'cadence': float (steps/sec),
                'foot': str ('left'/'right'/'unknown'),
                'surface': str,
                'distance_m': float,
                'gait_type': str ('walk'/'run'/'unknown')
            }
        """
        try:
            current_time = time.time()

            # Convert to mono for frequency analysis
            if block.ndim == 2:
                mono = np.mean(block, axis=1)
                left = block[:, 0]
                right = block[:, 1]
            else:
                mono = block.ravel()
                left = mono
                right = mono
                stereo = False

            # FFT analysis
            window = np.hanning(len(mono))
            windowed = mono * window
            fft_data = np.fft.rfft(windowed)
            freqs = np.fft.rfftfreq(len(mono), d=1.0/sample_rate)
            power = np.abs(fft_data)

            # Analyze frequency bands characteristic for human footsteps
            impact_mask = (freqs >= self.freq_impact[0]) & (freqs < self.freq_impact[1])
            detail_mask = (freqs >= self.freq_detail[0]) & (freqs < self.freq_detail[1])
            body_mask = (freqs >= self.freq_body[0]) & (freqs < self.freq_body[1])

            impact_power = np.mean(power[impact_mask]) if np.any(impact_mask) else 0.0
            detail_power = np.mean(power[detail_mask]) if np.any(detail_mask) else 0.0
            body_power = np.mean(power[body_mask]) if np.any(body_mask) else 0.0

            total_power = np.mean(power) + 1e-9

            # Ratios characteristic for footsteps
            impact_ratio = impact_power / total_power
            detail_ratio = detail_power / total_power
            body_ratio = body_power / total_power

            # FIXED v4.1.2: Update noise floor estimation (using median for robustness)
            self.noise_history.append({
                'impact': impact_ratio,
                'detail': detail_ratio,
                'body': body_ratio,
                'total': total_power
            })

            # Calculate adaptive noise floor from recent history
            if len(self.noise_history) >= 20:
                impact_values = [h['impact'] for h in self.noise_history]
                detail_values = [h['detail'] for h in self.noise_history]
                body_values = [h['body'] for h in self.noise_history]

                # Use median (robust to outliers/actual footsteps)
                self.noise_floor_impact = np.median(impact_values)
                self.noise_floor_detail = np.median(detail_values)
                self.noise_floor_body = np.median(body_values)

                # Check for repetitive ambient sound (low variance = ambient)
                self.ambient_filter_history.append(total_power)
                if len(self.ambient_filter_history) >= 20:
                    variance = np.var(list(self.ambient_filter_history))
                    mean_power = np.mean(list(self.ambient_filter_history))
                    normalized_variance = variance / (mean_power ** 2 + 1e-9)

                    # If very low variance, this is repetitive ambient - raise thresholds
                    if normalized_variance < self.ambient_variance_threshold:
                        self.threshold_multiplier = 2.0  # Higher threshold for ambient
                    else:
                        self.threshold_multiplier = 1.5  # Normal threshold

            # FIXED v4.1.2: Adaptive thresholds based on noise floor
            adaptive_impact_threshold = max(
                self.base_impact_threshold,
                self.noise_floor_impact * self.threshold_multiplier
            )
            adaptive_detail_threshold = max(
                self.base_detail_threshold,
                self.noise_floor_detail * self.threshold_multiplier
            )
            adaptive_body_threshold = max(
                self.base_body_threshold,
                self.noise_floor_body * self.threshold_multiplier
            )

            # Human footstep signature: strong impact + moderate detail + low body
            # Using adaptive thresholds instead of static ones
            is_step_candidate = (
                impact_ratio > adaptive_impact_threshold and  # strong impact above noise
                detail_ratio > adaptive_detail_threshold and  # some detail above noise
                body_ratio > adaptive_body_threshold          # some body weight above noise
            )

            # Initialize result
            result = {
                'is_human_step': False,
                'confidence': 0.0,
                'cadence': 0.0,
                'foot': 'unknown',
                'surface': 'unknown',
                'distance_m': 0.0,
                'gait_type': 'unknown'
            }

            if not is_step_candidate:
                return result

            # Temporal pattern analysis (cadence detection)
            time_since_last = current_time - self.last_step_time

            # Valid step interval: 150ms to 800ms (covers walk and run)
            if 0.15 < time_since_last < 0.8:
                self.step_intervals.append(time_since_last)
                if len(self.step_intervals) > self.max_intervals:
                    self.step_intervals.pop(0)

                self.step_history.append(current_time)
                if len(self.step_history) > self.max_history:
                    self.step_history.pop(0)

                # Calculate cadence (steps per second)
                if len(self.step_intervals) >= 3:
                    avg_interval = np.mean(self.step_intervals[-5:])
                    cadence = 1.0 / avg_interval if avg_interval > 0 else 0.0

                    # Check if cadence matches human walking or running
                    is_walk_cadence = self.cadence_walk[0] <= cadence <= self.cadence_walk[1]
                    is_run_cadence = self.cadence_run[0] <= cadence <= self.cadence_run[1]

                    if is_walk_cadence or is_run_cadence:
                        result['is_human_step'] = True
                        result['cadence'] = cadence
                        result['gait_type'] = 'walk' if is_walk_cadence else 'run'

                        # Confidence based on pattern regularity
                        if len(self.step_intervals) >= 5:
                            interval_std = np.std(self.step_intervals[-5:])
                            regularity = 1.0 - min(interval_std / avg_interval, 1.0)
                            result['confidence'] = regularity * 100.0
                        else:
                            result['confidence'] = 60.0  # moderate confidence

                self.last_step_time = current_time

            # L-R pattern detection (foot classification)
            if stereo and result['is_human_step']:
                left_rms = np.sqrt(np.mean(left ** 2))
                right_rms = np.sqrt(np.mean(right ** 2))

                if left_rms > right_rms * 1.2:
                    result['foot'] = 'left'
                    self.lr_pattern.append('L')
                elif right_rms > left_rms * 1.2:
                    result['foot'] = 'right'
                    self.lr_pattern.append('R')
                else:
                    result['foot'] = 'center'
                    self.lr_pattern.append('C')

                if len(self.lr_pattern) > self.max_lr_history:
                    self.lr_pattern.pop(0)

                # Check for L-R-L-R pattern (increases confidence)
                if len(self.lr_pattern) >= 4:
                    pattern_str = ''.join(self.lr_pattern[-4:])
                    if pattern_str in ['LRLR', 'RLRL', 'LRCR', 'RLCR', 'CRLR', 'CLRL']:
                        result['confidence'] = min(result['confidence'] + 15.0, 100.0)

            # Surface type detection (based on detail frequency ratio)
            if result['is_human_step']:
                if detail_ratio > 0.15:
                    result['surface'] = 'hard'  # concrete, metal
                elif detail_ratio > 0.08:
                    result['surface'] = 'medium'  # wood, tile
                else:
                    result['surface'] = 'soft'  # carpet, grass, dirt

                self.surface_type = result['surface']

            # Distance estimation (based on loudness)
            if result['is_human_step']:
                rms = np.sqrt(np.mean(mono ** 2))
                if rms > 0:
                    # Rough estimation: louder = closer
                    # This is simplified, real distance needs proper calibration
                    db = 20 * np.log10(rms + 1e-10)
                    # Map dB to distance (empirical formula)
                    # -60 dB = far (50m), -20 dB = close (5m)
                    distance = np.clip(50.0 * ((-20 - db) / 40.0), 1.0, 100.0)
                    result['distance_m'] = distance
                    self.estimated_distance = distance

            return result

        except Exception as e:
            log(f"Error in HumanFootstepDetector.analyze_footstep: {e}", "ERROR")
            return {
                'is_human_step': False,
                'confidence': 0.0,
                'cadence': 0.0,
                'foot': 'unknown',
                'surface': 'unknown',
                'distance_m': 0.0,
                'gait_type': 'unknown'
            }

    def get_pattern_quality(self):
        """
        Get overall pattern quality score (0-100)
        Based on regularity and L-R pattern consistency
        """
        if len(self.step_intervals) < 3:
            return 0.0

        # Temporal regularity
        avg_interval = np.mean(self.step_intervals)
        std_interval = np.std(self.step_intervals)
        temporal_quality = (1.0 - min(std_interval / avg_interval, 1.0)) * 50.0

        # L-R pattern quality
        lr_quality = 0.0
        if len(self.lr_pattern) >= 4:
            # Count alternations
            alternations = sum(1 for i in range(len(self.lr_pattern)-1)
                             if self.lr_pattern[i] != self.lr_pattern[i+1])
            expected_alternations = len(self.lr_pattern) - 1
            if expected_alternations > 0:
                lr_quality = (alternations / expected_alternations) * 50.0

        return temporal_quality + lr_quality

