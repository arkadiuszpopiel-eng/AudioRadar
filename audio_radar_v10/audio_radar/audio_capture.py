"""Audio capture utilities for the Audio Radar project.

This module wraps the ``sounddevice`` library to provide a simple
interface for listing audio devices and capturing audio in real time.
It exposes two helper functions to list input and output devices and
an ``AudioStream`` class that simplifies opening an input stream and
delivering blocks of audio samples via a callback. The class is
designed to work with NumPy arrays and uses a blocking or callback
style depending on configuration.

The module does not itself perform any analysis; callers should
subclass ``AudioStream`` or assign to its ``on_data`` attribute a
function that accepts a NumPy array of shape (frames, channels).

Note that this file does not depend on Pygame and can be used in
headless contexts. The user must install the ``sounddevice`` package
for this to function. On Windows you may need to install the
appropriate PortAudio binaries or use a wheel that bundles them.
"""

from __future__ import annotations

try:
    import sounddevice as sd
except ImportError:
    sd = None  # type: ignore

import numpy as np  # type: ignore

from typing import Callable, Iterable, List, Tuple, Optional


def list_audio_input_devices() -> List[Tuple[int, str]]:
    """Return a list of available audio input devices.

    Each entry in the returned list is a tuple of the device index and
    the human‑readable name. If ``sounddevice`` is not available an
    empty list is returned.
    """
    if sd is None:
        return []
    devices = sd.query_devices()
    results: List[Tuple[int, str]] = []
    for idx, dev in enumerate(devices):
        if dev.get("max_input_channels", 0) > 0:
            results.append((idx, dev.get("name", f"Device {idx}")))
    return results


def list_audio_output_devices() -> List[Tuple[int, str]]:
    """Return a list of available audio output devices.

    Each entry in the returned list is a tuple of the device index and
    the human‑readable name. If ``sounddevice`` is not available an
    empty list is returned.
    """
    if sd is None:
        return []
    devices = sd.query_devices()
    results: List[Tuple[int, str]] = []
    for idx, dev in enumerate(devices):
        if dev.get("max_output_channels", 0) > 0:
            results.append((idx, dev.get("name", f"Device {idx}")))
    return results


class AudioStream:
    """Capture audio from a specified input device and deliver blocks to a callback.

    Parameters
    ----------
    input_device : Optional[int]
        The index of the input device to use. If ``None`` the system
        default input is used.
    samplerate : int
        The sampling rate in samples per second. 44100 Hz is a good
        default for most PC sound cards and matches the typical output
        of games on Windows.
    blocksize : int
        The number of frames delivered to the callback at a time. A
        lower block size decreases latency but increases CPU usage.

    Notes
    -----
    The ``on_data`` attribute is a callback which is invoked with a
    NumPy array of shape ``(frames, channels)``. Assign a function to
    ``on_data`` to perform analysis on each block of samples. The
    callback should not block for long periods as it is executed in
    the PortAudio callback thread.
    """

    def __init__(self, input_device: Optional[int] = None, samplerate: int = 44100, blocksize: int = 1024) -> None:
        if sd is None:
            raise RuntimeError("sounddevice library is required for AudioStream")
        self.input_device = input_device
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.stream: Optional[sd.InputStream] = None
        self.on_data: Callable[[np.ndarray], None] = lambda data: None

    def start(self) -> None:
        """Open the stream and begin capturing audio.

        Audio blocks will be delivered to the ``on_data`` callback
        attribute. This call returns immediately – the stream runs in
        a separate thread managed by PortAudio. Use ``stop`` to close
        the stream when finished.
        """
        def callback(indata: np.ndarray, frames: int, time, status) -> None:
            # Convert input to a contiguous NumPy array and invoke callback
            if frames > 0:
                self.on_data(indata.copy())
        self.stream = sd.InputStream(
            device=self.input_device,
            channels=sd.query_devices(self.input_device, 'input')['max_input_channels'] if self.input_device is not None else 2,
            samplerate=self.samplerate,
            blocksize=self.blocksize,
            callback=callback,
        )
        self.stream.start()

    def stop(self) -> None:
        """Stop capturing audio and close the stream."""
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None