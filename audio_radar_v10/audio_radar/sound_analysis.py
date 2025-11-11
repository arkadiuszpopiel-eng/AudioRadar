"""Sound analysis routines for AudioRadar v10.2.

Simple event detection for shots and footsteps based on threshold
comparison with user-adjustable threshold parameter.
"""

from __future__ import annotations
from typing import Optional

try:
    import numpy as np
except ImportError:
    np = None


def detect_event(samples: np.ndarray, threshold: float = 0.3) -> Optional[str]:
    """Detect sound events in audio samples based on threshold.
    
    Parameters
    ----------
    samples : np.ndarray
        Audio samples array of shape (frames,) or (frames, channels).
    threshold : float
        Detection threshold (0.0 to 1.0). Higher values require louder sounds.
    
    Returns
    -------
    Optional[str]
        'shot' if gunshot detected, 'footstep' if footstep detected, None otherwise.
    
    Notes
    -----
    This is a simple threshold-based detector:
    - Peak above threshold*0.8: gunshot
    - Peak above threshold*0.4: footstep
    """
    if np is None or samples.size == 0:
        return None
    
    # Convert to mono if stereo
    if samples.ndim == 2 and samples.shape[1] > 1:
        mono = samples.mean(axis=1)
    else:
        mono = samples.ravel()
    
    # Compute peak level
    peak = np.max(np.abs(mono))
    
    # Threshold-based detection
    shot_threshold = threshold * 0.8
    footstep_threshold = threshold * 0.4
    
    if peak > shot_threshold:
        return 'shot'
    elif peak > footstep_threshold:
        return 'footstep'
    
    return None