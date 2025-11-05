"""Sound analysis routines for the Audio Radar project.

This module contains functions that operate on chunks of audio samples to
determine whether certain events of interest have occurred. The goal is
to detect footsteps and gunshots in the audio stream produced by a
game, ignoring other background noise. The implementation here uses
simple heuristic methods based on amplitude statistics; users with
deep learning experience may wish to replace or augment these
functions with a machine learning model trained on representative
audio data.
"""

from __future__ import annotations

from typing import Optional, Dict, Any, Tuple
import time

try:
    import numpy as np  # type: ignore
except ImportError:
    np = None  # type: ignore

try:
    from scipy import signal  # type: ignore
except ImportError:
    signal = None  # type: ignore

# Default thresholds for heuristic detection. These values were chosen to work
# reasonably across a variety of games but may need adjusting for
# particular titles. You can experiment with these by editing
# ``config.json`` or by tweaking them here.
SHOT_PEAK_THRESHOLD = 0.6  # relative peak amplitude above which a block is considered a gunshot
FOOTSTEP_STD_THRESHOLD = 0.05  # standard deviation threshold for step detection

# Global configuration dictionary that can be updated by main module
_detection_config: Dict[str, Any] = {
    "shot_peak_threshold": SHOT_PEAK_THRESHOLD,
    "footstep_std_threshold": FOOTSTEP_STD_THRESHOLD,
    "enable_bandpass_filter": True,
    "footstep_freq_range": [2000, 8000],
    "shot_freq_range": [200, 12000],
    "samplerate": 48000,
}

# Background noise estimation
_background_level = 0.01
_last_update_time = time.time()


def set_detection_config(config: Dict[str, Any]) -> None:
    """Update detection configuration parameters.
    
    Parameters
    ----------
    config : dict
        Dictionary containing detection parameters such as thresholds,
        filter settings, and samplerate.
    """
    global _detection_config
    _detection_config.update(config)


def apply_bandpass_filter(samples: np.ndarray, lowcut: float, highcut: float, 
                          samplerate: int, order: int = 4) -> np.ndarray:
    """Apply a Butterworth bandpass filter to the audio samples.
    
    Parameters
    ----------
    samples : ndarray
        Audio samples to filter (mono signal).
    lowcut : float
        Lower frequency bound in Hz.
    highcut : float
        Upper frequency bound in Hz.
    samplerate : int
        Sampling rate in Hz.
    order : int
        Filter order (higher = sharper cutoff).
        
    Returns
    -------
    ndarray
        Filtered audio samples.
    """
    if signal is None:
        return samples
    
    nyquist = samplerate / 2.0
    low = lowcut / nyquist
    high = highcut / nyquist
    
    # Ensure frequencies are in valid range
    low = max(0.01, min(low, 0.99))
    high = max(low + 0.01, min(high, 0.99))
    
    try:
        b, a = signal.butter(order, [low, high], btype='band')
        filtered = signal.filtfilt(b, a, samples)
        return filtered
    except Exception:
        # If filtering fails, return original samples
        return samples


def estimate_distance(amplitude: float, background: float = 0.01) -> float:
    """Estimate relative distance based on amplitude.
    
    Parameters
    ----------
    amplitude : float
        Peak amplitude of the detected sound.
    background : float
        Background noise level.
        
    Returns
    -------
    float
        Relative distance estimate (0.0 = very close, 1.0 = far).
    """
    # Normalize amplitude relative to background
    if amplitude < background:
        return 1.0
    
    # Logarithmic distance estimation
    # Louder sounds = closer (lower distance value)
    ratio = amplitude / max(background, 0.001)
    distance = 1.0 / (1.0 + np.log10(max(ratio, 1.0)))
    return np.clip(distance, 0.0, 1.0)


def update_background_level(rms: float, alpha: float = 0.01) -> None:
    """Update background noise level estimation using exponential smoothing.
    
    Parameters
    ----------
    rms : float
        Current RMS level of the audio.
    alpha : float
        Smoothing factor (0 = no update, 1 = full update).
    """
    global _background_level, _last_update_time
    current_time = time.time()
    
    # Only update if more than 0.5 seconds have passed
    if current_time - _last_update_time > 0.5:
        _background_level = alpha * rms + (1 - alpha) * _background_level
        _last_update_time = current_time


def detect_event(samples: np.ndarray) -> Optional[str]:
    """Analyse a block of audio samples and detect a sound event.

    Parameters
    ----------
    samples : ndarray
        A 2‑D NumPy array of shape (frames, channels) containing the
        captured audio for this block. Channels are averaged to mono
        before analysis.

    Returns
    -------
    str or None
        Returns ``'shot'`` if a gunshot is detected, ``'footstep'`` if
        a footstep is detected and ``None`` if no event is recognised.

    Notes
    -----
    This function uses amplitude heuristics combined with optional
    bandpass filtering. It computes the maximum absolute amplitude in
    the block to look for gunshots and uses the standard deviation of
    the signal to detect footsteps. Because games vary widely in their
    audio mixes and loudness ranges, you may need to adjust the
    thresholds in the configuration.
    """
    if np is None:
        return None
    if samples.size == 0:
        return None
    
    # Convert multi‑channel audio to mono by averaging channels
    if samples.ndim == 2 and samples.shape[1] > 1:
        mono = samples.mean(axis=1)
    else:
        mono = samples.ravel()
    
    # Normalise to range [-1, 1] if values are integer types
    if np.issubdtype(mono.dtype, np.integer):
        # 16‑bit audio: int16 ranges from -32768 to 32767
        info = np.iinfo(mono.dtype)
        mono = mono.astype(np.float32) / max(abs(info.min), info.max)
    
    # Update background noise estimate
    rms = np.sqrt(np.mean(mono ** 2))
    update_background_level(rms)
    
    # Get configuration parameters
    shot_threshold = _detection_config.get("shot_peak_threshold", SHOT_PEAK_THRESHOLD)
    footstep_threshold = _detection_config.get("footstep_std_threshold", FOOTSTEP_STD_THRESHOLD)
    enable_filter = _detection_config.get("enable_bandpass_filter", True)
    samplerate = _detection_config.get("samplerate", 48000)
    
    # Compute statistics on original signal
    peak = np.max(np.abs(mono))
    
    # Check for gunshot first (very loud, sharp peaks)
    if peak > shot_threshold:
        # Optional: Apply shot-specific bandpass filter for verification
        if enable_filter and signal is not None:
            shot_freq = _detection_config.get("shot_freq_range", [200, 12000])
            filtered_shot = apply_bandpass_filter(mono, shot_freq[0], shot_freq[1], samplerate)
            filtered_peak = np.max(np.abs(filtered_shot))
            # Verify that filtered signal still shows strong peak
            if filtered_peak > shot_threshold * 0.7:
                return 'shot'
        else:
            return 'shot'
    
    # Check for footsteps (moderate variation in specific frequency range)
    if enable_filter and signal is not None:
        footstep_freq = _detection_config.get("footstep_freq_range", [2000, 8000])
        filtered_footstep = apply_bandpass_filter(mono, footstep_freq[0], footstep_freq[1], samplerate)
        std_filtered = np.std(filtered_footstep)
        
        # Use filtered standard deviation for footstep detection
        if std_filtered > footstep_threshold:
            return 'footstep'
    else:
        # Fallback to unfiltered detection
        std = np.std(mono)
        if std > footstep_threshold:
            return 'footstep'
    
    return None


def detect_event_with_direction(samples: np.ndarray) -> Optional[Tuple[str, int, float]]:
    """Analyse multi-channel audio and detect event with direction.
    
    This function processes multi-channel audio (stereo, 5.1, 7.1) to
    determine not only the event type but also the approximate direction.
    
    Parameters
    ----------
    samples : ndarray
        A 2‑D NumPy array of shape (frames, channels) containing the
        captured audio for this block.
        
    Returns
    -------
    tuple or None
        Returns (event_type, direction_degrees, distance) where:
        - event_type is 'shot' or 'footstep'
        - direction_degrees is 0-359 (0 = front, 90 = right, 180 = back, 270 = left)
        - distance is 0.0-1.0 (0 = very close, 1 = far)
        Returns None if no event is detected.
    """
    if np is None:
        return None
    if samples.size == 0:
        return None
    
    # First detect if there's any event
    event_type = detect_event(samples)
    if event_type is None:
        return None
    
    # Analyze per-channel energy to determine direction
    num_channels = samples.shape[1] if samples.ndim == 2 else 1
    
    if num_channels == 1:
        # Mono: no direction info, default to front
        amplitude = np.max(np.abs(samples))
        distance = estimate_distance(amplitude, _background_level)
        return (event_type, 0, distance)
    
    # Calculate RMS per channel
    channel_energy = np.array([np.sqrt(np.mean(samples[:, i] ** 2)) 
                               for i in range(num_channels)])
    
    # Calculate overall amplitude for distance estimation
    max_amplitude = np.max(channel_energy)
    distance = estimate_distance(max_amplitude, _background_level)
    
    if num_channels == 2:
        # Stereo: simple left/right detection
        left, right = channel_energy[0], channel_energy[1]
        if left > right * 1.2:
            direction = 270  # Left
        elif right > left * 1.2:
            direction = 90   # Right
        else:
            direction = 0    # Center/Front
    elif num_channels >= 6:
        # 5.1 or 7.1 surround sound
        # Standard channel mapping: FL, FR, C, LFE, RL, RR, (SL, SR for 7.1)
        # Map channels to angles
        channel_angles = {
            0: 330,   # Front Left (FL) = -30°
            1: 30,    # Front Right (FR) = +30°
            2: 0,     # Center (C) = 0°
            3: 0,     # LFE (subwoofer, ignore for direction)
            4: 210,   # Rear Left (RL) = -150°
            5: 150,   # Rear Right (RR) = +150°
        }
        if num_channels >= 8:
            channel_angles[6] = 270  # Side Left (SL) = -90°
            channel_angles[7] = 90   # Side Right (SR) = +90°
        
        # Find dominant direction using weighted average
        total_energy = 0
        weighted_x = 0
        weighted_y = 0
        
        for ch_idx, angle in channel_angles.items():
            if ch_idx >= num_channels or ch_idx == 3:  # Skip LFE
                continue
            energy = channel_energy[ch_idx]
            total_energy += energy
            # Convert angle to radians and accumulate vector components
            rad = np.deg2rad(angle)
            weighted_x += energy * np.cos(rad)
            weighted_y += energy * np.sin(rad)
        
        if total_energy > 0:
            # Calculate resulting angle
            direction = int(np.rad2deg(np.arctan2(weighted_y, weighted_x))) % 360
        else:
            direction = 0
    else:
        # Unknown channel configuration, default to front
        direction = 0
    
    return (event_type, direction, distance)