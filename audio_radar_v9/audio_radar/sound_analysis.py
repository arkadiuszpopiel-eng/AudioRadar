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

from typing import Optional

try:
    import numpy as np  # type: ignore
except ImportError:
    np = None  # type: ignore

# Thresholds for heuristic detection. These values were chosen to work
# reasonably across a variety of games but may need adjusting for
# particular titles. You can experiment with these by editing
# ``config.json`` or by tweaking them here.
SHOT_PEAK_THRESHOLD = 0.6  # relative peak amplitude above which a block is considered a gunshot
FOOTSTEP_STD_THRESHOLD = 0.05  # standard deviation threshold for step detection


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
    This function uses simple amplitude heuristics: it computes the
    maximum absolute amplitude in the block to look for gunshots and
    uses the standard deviation of the signal to detect footsteps.
    Because games vary widely in their audio mixes and loudness
    ranges, you may need to adjust the thresholds at the top of this
    module.
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
    # Compute statistics
    peak = np.max(np.abs(mono))
    std = np.std(mono)
    # Gunshot detection: very sharp, loud peaks
    if peak > SHOT_PEAK_THRESHOLD:
        return 'shot'
    # Footstep detection: moderate variation and repetitive pattern
    # Here we simply use standard deviation as a proxy for variation
    if std > FOOTSTEP_STD_THRESHOLD:
        return 'footstep'
    return None