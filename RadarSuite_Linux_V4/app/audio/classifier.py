"""
RadarSuite v3.5.0 - Sound Classifier
Weapon/vehicle identification via spectral fingerprinting
"""

import numpy as np
from collections import deque

from core.logger import log


class SoundClassifier:
    """
    Advanced sound classification system
    Identifies weapon types, vehicles, environmental sounds
    Uses spectral fingerprinting and pattern matching
    """

    def __init__(self):
        log("SoundClassifier.__init__", "INFO")

        # Sound signatures (frequency patterns and characteristics)
        self.signatures = {
            # Weapons
            'rifle': {
                'freq_peak': (1500, 4000),
                'duration': (0.05, 0.15),
                'sharpness': 'high',
                'decay': 'fast'
            },
            'pistol': {
                'freq_peak': (2000, 5000),
                'duration': (0.03, 0.1),
                'sharpness': 'very_high',
                'decay': 'very_fast'
            },
            'shotgun': {
                'freq_peak': (500, 2000),
                'duration': (0.1, 0.25),
                'sharpness': 'medium',
                'decay': 'medium'
            },
            'sniper': {
                'freq_peak': (3000, 6000),
                'duration': (0.08, 0.2),
                'sharpness': 'very_high',
                'decay': 'fast'
            },
            # Vehicles
            'car_engine': {
                'freq_peak': (80, 250),
                'duration': (1.0, 10.0),
                'sharpness': 'low',
                'decay': 'sustained'
            },
            'helicopter': {
                'freq_peak': (50, 150),
                'duration': (2.0, 20.0),
                'sharpness': 'low',
                'decay': 'sustained'
            },
            # Explosions
            'explosion': {
                'freq_peak': (30, 500),
                'duration': (0.2, 1.0),
                'sharpness': 'very_low',
                'decay': 'slow'
            },
            'grenade': {
                'freq_peak': (50, 800),
                'duration': (0.15, 0.5),
                'sharpness': 'low',
                'decay': 'medium'
            }
        }

        # Classification history
        self.recent_classifications = []
        self.max_history = 20

    def classify_sound(self, block, sample_rate, fft_cache=None):
        """
        Classify sound type based on spectral characteristics (Module 12: optimized with FFT caching)

        Returns: dict with type, confidence, details
        """
        try:
            if block is None or len(block) == 0:
                return {'type': 'unknown', 'confidence': 0, 'details': {}}

            # Use cached FFT if available (Module 12 - Performance Optimization)
            if fft_cache is not None:
                fft_data = fft_cache['fft_data']
                freqs = fft_cache['freqs']
                power = fft_cache['power']
                mono = fft_cache['mono']
            else:
                # Fallback: compute FFT (legacy mode)
                # Convert to mono
                if block.ndim == 2:
                    mono = np.mean(block, axis=1)
                else:
                    mono = block.ravel()

                # FFT analysis
                fft_data = np.fft.rfft(mono * np.hanning(len(mono)))
                freqs = np.fft.rfftfreq(len(mono), d=1.0/sample_rate)
                power = np.abs(fft_data)

            # Find dominant frequency
            peak_idx = np.argmax(power)
            dominant_freq = freqs[peak_idx] if peak_idx < len(freqs) else 0

            # Calculate spectral characteristics
            total_power = np.sum(power)
            if total_power < 1e-10:
                return {'type': 'silence', 'confidence': 100, 'details': {}}

            # Spectral centroid (brightness)
            spectral_centroid = np.sum(freqs * power) / total_power

            # Spectral spread (bandwidth)
            spectral_spread = np.sqrt(np.sum(((freqs - spectral_centroid) ** 2) * power) / total_power)

            # Attack time (how quickly sound starts)
            envelope = np.abs(sp_signal.hilbert(mono))
            attack_time = self._estimate_attack_time(envelope, sample_rate)

            # Match against signatures
            best_match = 'unknown'
            best_confidence = 0

            for sound_type, sig in self.signatures.items():
                confidence = 0

                # Check frequency peak match
                if sig['freq_peak'][0] <= dominant_freq <= sig['freq_peak'][1]:
                    confidence += 40

                # Check sharpness (high frequency content)
                high_freq_mask = freqs > 2000
                high_freq_ratio = np.sum(power[high_freq_mask]) / total_power

                if sig['sharpness'] == 'very_high' and high_freq_ratio > 0.3:
                    confidence += 30
                elif sig['sharpness'] == 'high' and high_freq_ratio > 0.2:
                    confidence += 25
                elif sig['sharpness'] == 'medium' and 0.1 < high_freq_ratio < 0.3:
                    confidence += 20
                elif sig['sharpness'] == 'low' and high_freq_ratio < 0.1:
                    confidence += 20

                # Check attack time for decay type
                if sig['decay'] == 'very_fast' and attack_time < 0.05:
                    confidence += 30
                elif sig['decay'] == 'fast' and attack_time < 0.1:
                    confidence += 25
                elif sig['decay'] == 'medium' and 0.1 < attack_time < 0.3:
                    confidence += 20

                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = sound_type

            # Add to history
            classification = {
                'type': best_match,
                'confidence': best_confidence,
                'details': {
                    'dominant_freq': dominant_freq,
                    'centroid': spectral_centroid,
                    'spread': spectral_spread,
                    'attack_time': attack_time
                }
            }

            self.recent_classifications.append(classification)
            if len(self.recent_classifications) > self.max_history:
                self.recent_classifications.pop(0)

            return classification

        except Exception as e:
            log(f"Error in classify_sound: {e}", "ERROR")
            return {'type': 'unknown', 'confidence': 0, 'details': {}}

    def _estimate_attack_time(self, envelope, sample_rate):
        """Estimate how quickly sound reaches peak amplitude"""
        try:
            max_val = np.max(envelope)
            if max_val < 1e-10:
                return 0.0

            # Find time to reach 90% of maximum
            threshold = max_val * 0.9
            above_threshold = np.where(envelope >= threshold)[0]

            if len(above_threshold) > 0:
                attack_samples = above_threshold[0]
                attack_time = attack_samples / sample_rate
                return attack_time
            return 0.0

        except (ValueError, IndexError, ZeroDivisionError) as e:
            log(f"Attack time calculation error: {e}", level="WARNING")
            return 0.0

