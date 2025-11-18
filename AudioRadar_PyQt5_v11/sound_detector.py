"""
Advanced Sound Detection for AudioRadar PyQt5
Detects walking, running, and shooting sounds with directional tracking and distance estimation.
"""

import numpy as np
from scipy import signal
from typing import Optional, Tuple, Dict
from dataclasses import dataclass
from enum import Enum
import time

from logger import get_logger


class SoundType(Enum):
    """Types of sounds that can be detected."""
    WALKING = "walking"
    RUNNING = "running"
    SHOOTING = "shooting"
    UNKNOWN = "unknown"


@dataclass
class SoundDetection:
    """Represents a detected sound event."""
    sound_type: SoundType
    direction: float  # Direction in degrees (0-360, 0=front)
    distance: float  # Estimated distance in meters
    confidence: float  # Detection confidence (0-1)
    velocity: float  # Radial velocity (positive=approaching, negative=retreating)
    timestamp: float  # Detection timestamp


class SoundDetector:
    """
    Advanced sound detector with walking/running/shooting detection
    and directional tracking with distance estimation.
    """

    def __init__(self, sample_rate: int = 48000):
        self.logger = get_logger()
        self.sample_rate = sample_rate
        self.logger.info(f"Initializing Sound Detector (sample rate: {sample_rate} Hz)")

        # Detection thresholds
        self.thresholds = {
            'walking_rms_min': 0.02,
            'walking_rms_max': 0.15,
            'walking_freq_min': 1.0,  # Hz (steps per second)
            'walking_freq_max': 3.0,
            'running_rms_min': 0.10,
            'running_rms_max': 0.40,
            'running_freq_min': 3.0,  # Hz (steps per second)
            'running_freq_max': 6.0,
            'shooting_peak_threshold': 0.60,
            'shooting_attack_time': 0.01,  # seconds
            'confidence_threshold': 0.5
        }

        # History for tracking
        self.detection_history = []
        self.max_history = 10

        # Previous detection for velocity calculation
        self.previous_detection: Optional[SoundDetection] = None

        self.logger.info("Sound Detector initialized successfully")

    def detect(self, audio_data: np.ndarray, sample_rate: float) -> Optional[SoundDetection]:
        """
        Detect sound type, direction, and distance from audio data.

        Args:
            audio_data: Audio samples (stereo, shape: [frames, 2])
            sample_rate: Audio sample rate

        Returns:
            SoundDetection object if sound detected, None otherwise
        """
        try:
            # Update sample rate if changed
            if self.sample_rate != sample_rate:
                self.sample_rate = int(sample_rate)

            # Ensure stereo audio
            if audio_data.ndim == 1:
                # Convert mono to stereo
                audio_data = np.column_stack([audio_data, audio_data])
            elif audio_data.shape[1] > 2:
                # Take first two channels
                audio_data = audio_data[:, :2]

            # Analyze audio
            sound_type, confidence = self._classify_sound(audio_data)

            if sound_type == SoundType.UNKNOWN or confidence < self.thresholds['confidence_threshold']:
                return None

            # Estimate direction
            direction = self._estimate_direction(audio_data)

            # Estimate distance
            distance = self._estimate_distance(audio_data, sound_type)

            # Calculate velocity (approaching/retreating)
            velocity = self._calculate_velocity(direction, distance)

            # Create detection
            detection = SoundDetection(
                sound_type=sound_type,
                direction=direction,
                distance=distance,
                confidence=confidence,
                velocity=velocity,
                timestamp=time.time()
            )

            # Update history
            self.detection_history.append(detection)
            if len(self.detection_history) > self.max_history:
                self.detection_history.pop(0)

            self.previous_detection = detection

            # Log detection
            self.logger.log_detection(
                sound_type.value,
                direction,
                distance,
                confidence
            )

            return detection

        except Exception as e:
            self.logger.error(f"Error in sound detection", e)
            return None

    def _classify_sound(self, audio_data: np.ndarray) -> Tuple[SoundType, float]:
        """
        Classify sound type and return confidence.

        Returns:
            Tuple of (SoundType, confidence)
        """
        # Convert to mono for analysis
        mono = np.mean(audio_data, axis=1)

        # Calculate features
        rms = np.sqrt(np.mean(mono ** 2))
        peak = np.max(np.abs(mono))
        std = np.std(mono)

        # Zero crossing rate
        zcr = np.sum(np.diff(np.sign(mono)) != 0) / len(mono)

        # Spectral features
        freqs, psd = signal.welch(mono, fs=self.sample_rate, nperseg=min(len(mono), 2048))

        # Dominant frequency
        dominant_freq_idx = np.argmax(psd)
        dominant_freq = freqs[dominant_freq_idx]

        # Detect periodicity for footsteps
        autocorr = np.correlate(mono, mono, mode='full')
        autocorr = autocorr[len(autocorr) // 2:]
        autocorr = autocorr / autocorr[0] if autocorr[0] != 0 else autocorr

        # Find peaks in autocorrelation to detect periodic patterns
        peaks, _ = signal.find_peaks(autocorr, height=0.5, distance=int(self.sample_rate / 6))

        # Calculate periodicity
        if len(peaks) > 0:
            avg_period = np.mean(np.diff(peaks)) if len(peaks) > 1 else peaks[0]
            step_frequency = self.sample_rate / avg_period if avg_period > 0 else 0
        else:
            step_frequency = 0

        # Shooting detection (sharp attack, high peak)
        if peak > self.thresholds['shooting_peak_threshold']:
            # Check for sharp attack
            attack_samples = int(self.thresholds['shooting_attack_time'] * self.sample_rate)
            if attack_samples < len(mono):
                attack_slope = np.max(np.abs(np.diff(mono[:attack_samples])))
                if attack_slope > 0.1:
                    confidence = min(peak / self.thresholds['shooting_peak_threshold'], 1.0)
                    return SoundType.SHOOTING, confidence

        # Running detection (higher energy, faster periodicity)
        if (self.thresholds['running_rms_min'] < rms < self.thresholds['running_rms_max'] and
                self.thresholds['running_freq_min'] < step_frequency < self.thresholds['running_freq_max']):
            # Calculate confidence based on how well it matches running profile
            rms_conf = 1.0 - abs(rms - 0.25) / 0.25
            freq_conf = 1.0 - abs(step_frequency - 4.5) / 3.0
            confidence = (rms_conf + freq_conf) / 2.0
            confidence = max(0.0, min(1.0, confidence))
            return SoundType.RUNNING, confidence

        # Walking detection (moderate energy, slower periodicity)
        if (self.thresholds['walking_rms_min'] < rms < self.thresholds['walking_rms_max'] and
                self.thresholds['walking_freq_min'] < step_frequency < self.thresholds['walking_freq_max']):
            # Calculate confidence
            rms_conf = 1.0 - abs(rms - 0.08) / 0.08
            freq_conf = 1.0 - abs(step_frequency - 2.0) / 2.0
            confidence = (rms_conf + freq_conf) / 2.0
            confidence = max(0.0, min(1.0, confidence))
            return SoundType.WALKING, confidence

        return SoundType.UNKNOWN, 0.0

    def _estimate_direction(self, audio_data: np.ndarray) -> float:
        """
        Estimate direction of sound source based on stereo audio.

        Args:
            audio_data: Stereo audio data [frames, 2]

        Returns:
            Direction in degrees (0-360, 0=front, 90=right, 180=back, 270=left)
        """
        try:
            left = audio_data[:, 0]
            right = audio_data[:, 1]

            # Calculate cross-correlation to find time delay
            correlation = signal.correlate(right, left, mode='full')
            delay_samples = np.argmax(correlation) - (len(left) - 1)

            # Convert delay to angle
            # Assuming ear spacing of ~0.2m and speed of sound ~343 m/s
            max_delay_samples = int(0.2 * self.sample_rate / 343)

            if max_delay_samples > 0:
                # Normalize delay to [-1, 1]
                delay_normalized = delay_samples / max_delay_samples
                delay_normalized = np.clip(delay_normalized, -1, 1)

                # Convert to angle (simple model)
                # Negative delay means sound from left, positive from right
                angle = np.arcsin(delay_normalized) * 180 / np.pi  # -90 to 90

                # Also consider amplitude difference
                rms_left = np.sqrt(np.mean(left ** 2))
                rms_right = np.sqrt(np.mean(right ** 2))

                if rms_left + rms_right > 0:
                    amplitude_ratio = (rms_right - rms_left) / (rms_right + rms_left)
                else:
                    amplitude_ratio = 0

                # Combine time delay and amplitude for better estimate
                angle = 0.7 * angle + 0.3 * (amplitude_ratio * 90)

                # Convert to 0-360 range (0=front, 90=right, 180=back, 270=left)
                if angle >= 0:
                    direction = 90 + angle  # Right side
                else:
                    direction = 270 + angle  # Left side

                direction = direction % 360

            else:
                # Fallback to amplitude-based estimation
                rms_left = np.sqrt(np.mean(left ** 2))
                rms_right = np.sqrt(np.mean(right ** 2))

                if rms_right > rms_left:
                    direction = 90  # Right
                else:
                    direction = 270  # Left

            return float(direction)

        except Exception as e:
            self.logger.error(f"Error estimating direction", e)
            return 0.0

    def _estimate_distance(self, audio_data: np.ndarray, sound_type: SoundType) -> float:
        """
        Estimate distance to sound source based on amplitude and sound type.

        Args:
            audio_data: Audio data
            sound_type: Type of detected sound

        Returns:
            Estimated distance in meters
        """
        try:
            # Calculate RMS amplitude
            mono = np.mean(audio_data, axis=1)
            rms = np.sqrt(np.mean(mono ** 2))

            # Distance estimation based on inverse square law
            # Reference: RMS of 0.5 at 1 meter

            # Sound type specific calibration
            if sound_type == SoundType.SHOOTING:
                reference_rms = 0.8  # Gunshots are loud
                reference_distance = 5.0  # meters
            elif sound_type == SoundType.RUNNING:
                reference_rms = 0.25
                reference_distance = 3.0
            else:  # WALKING
                reference_rms = 0.08
                reference_distance = 2.0

            # Calculate distance using inverse square law
            if rms > 0:
                distance = reference_distance * np.sqrt(reference_rms / rms)
            else:
                distance = 100.0  # Very far if no signal

            # Clamp to reasonable range
            distance = np.clip(distance, 0.5, 100.0)

            return float(distance)

        except Exception as e:
            self.logger.error(f"Error estimating distance", e)
            return 10.0  # Default distance

    def _calculate_velocity(self, current_direction: float, current_distance: float) -> float:
        """
        Calculate radial velocity (approaching/retreating).

        Args:
            current_direction: Current direction in degrees
            current_distance: Current distance in meters

        Returns:
            Velocity in m/s (positive=approaching, negative=retreating)
        """
        if self.previous_detection is None:
            return 0.0

        try:
            # Time delta
            time_delta = time.time() - self.previous_detection.timestamp

            if time_delta < 0.01:  # Too short
                return 0.0

            # Distance delta
            distance_delta = self.previous_detection.distance - current_distance

            # Velocity (positive = approaching)
            velocity = distance_delta / time_delta

            # Smooth velocity estimate
            velocity = np.clip(velocity, -10.0, 10.0)

            return float(velocity)

        except Exception as e:
            self.logger.error(f"Error calculating velocity", e)
            return 0.0

    def get_detection_summary(self) -> Dict:
        """
        Get summary of recent detections.

        Returns:
            Dictionary with detection statistics
        """
        if not self.detection_history:
            return {
                'total_detections': 0,
                'walking': 0,
                'running': 0,
                'shooting': 0,
                'average_distance': 0.0,
                'average_confidence': 0.0
            }

        walking = sum(1 for d in self.detection_history if d.sound_type == SoundType.WALKING)
        running = sum(1 for d in self.detection_history if d.sound_type == SoundType.RUNNING)
        shooting = sum(1 for d in self.detection_history if d.sound_type == SoundType.SHOOTING)

        avg_distance = np.mean([d.distance for d in self.detection_history])
        avg_confidence = np.mean([d.confidence for d in self.detection_history])

        return {
            'total_detections': len(self.detection_history),
            'walking': walking,
            'running': running,
            'shooting': shooting,
            'average_distance': float(avg_distance),
            'average_confidence': float(avg_confidence)
        }
