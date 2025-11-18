"""
Audio Device Manager for AudioRadar PyQt5
Handles audio device detection, selection, and capture with Sound Blaster Z SE optimization.
"""

import numpy as np
import sounddevice as sd
from typing import List, Tuple, Optional, Callable
from dataclasses import dataclass
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import time

from logger import get_logger


@dataclass
class AudioDevice:
    """Represents an audio device."""
    index: int
    name: str
    channels: int
    sample_rate: float
    is_input: bool
    is_output: bool
    is_default: bool
    hostapi: str


class AudioManager(QObject):
    """
    Manages audio device detection, selection, and capture.
    Optimized for Sound Blaster Z SE card.
    """

    # Signals
    device_list_updated = pyqtSignal(list)
    audio_data_ready = pyqtSignal(np.ndarray, float)  # audio samples, sample_rate
    audio_level_changed = pyqtSignal(float)  # RMS level
    audio_quality_changed = pyqtSignal(dict)  # quality metrics
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.logger = get_logger()
        self.logger.info("Initializing Audio Manager")

        self.current_device: Optional[AudioDevice] = None
        self.stream: Optional[sd.InputStream] = None
        self.is_capturing = False

        # Audio settings
        self.sample_rate = 48000  # Default for Sound Blaster Z SE
        self.block_size = 2048
        self.channels = 2

        # Audio quality metrics
        self.quality_metrics = {
            'rms_level': 0.0,
            'peak_level': 0.0,
            'noise_floor': 0.0,
            'snr': 0.0,
            'clipping': 0.0
        }

        # Quality monitoring timer
        self.quality_timer = QTimer()
        self.quality_timer.timeout.connect(self._emit_quality_metrics)
        self.quality_timer.setInterval(100)  # Update every 100ms

        self.logger.info("Audio Manager initialized successfully")

    def get_audio_devices(self) -> List[AudioDevice]:
        """Get list of all available audio devices."""
        self.logger.info("Scanning for audio devices...")
        devices = []

        try:
            device_list = sd.query_devices()
            default_input = sd.default.device[0]
            default_output = sd.default.device[1]

            for idx, dev in enumerate(device_list):
                device = AudioDevice(
                    index=idx,
                    name=dev['name'],
                    channels=max(dev.get('max_input_channels', 0), dev.get('max_output_channels', 0)),
                    sample_rate=dev.get('default_samplerate', 44100),
                    is_input=dev.get('max_input_channels', 0) > 0,
                    is_output=dev.get('max_output_channels', 0) > 0,
                    is_default=(idx == default_input or idx == default_output),
                    hostapi=sd.query_hostapis(dev['hostapi'])['name']
                )
                devices.append(device)

                # Log device info
                self.logger.log_audio_device({
                    'Index': idx,
                    'Name': device.name,
                    'Channels': device.channels,
                    'Sample Rate': device.sample_rate,
                    'Type': 'Input' if device.is_input else 'Output',
                    'Default': device.is_default,
                    'Host API': device.hostapi
                })

            self.logger.info(f"Found {len(devices)} audio devices")
            self.device_list_updated.emit(devices)

        except Exception as e:
            self.logger.error(f"Error scanning audio devices", e)
            self.error_occurred.emit(f"Error scanning devices: {str(e)}")

        return devices

    def get_input_devices(self) -> List[AudioDevice]:
        """Get list of input devices only."""
        return [dev for dev in self.get_audio_devices() if dev.is_input]

    def select_device(self, device: AudioDevice):
        """Select an audio device for capture."""
        self.logger.info(f"Selecting audio device: {device.name} (index: {device.index})")

        # Stop current stream if running
        if self.is_capturing:
            self.stop_capture()

        self.current_device = device
        self.sample_rate = int(device.sample_rate)
        self.channels = device.channels

        self.logger.info(f"Device selected: {device.name}, Sample Rate: {self.sample_rate} Hz")

    def start_capture(self):
        """Start audio capture."""
        if self.is_capturing:
            self.logger.warning("Audio capture already running")
            return

        if self.current_device is None:
            self.logger.warning("No device selected, using default input")
            devices = self.get_input_devices()
            if devices:
                self.current_device = devices[0]
            else:
                self.error_occurred.emit("No input devices available")
                return

        self.logger.info(f"Starting audio capture on device: {self.current_device.name}")

        try:
            self.stream = sd.InputStream(
                device=self.current_device.index,
                channels=self.channels,
                samplerate=self.sample_rate,
                blocksize=self.block_size,
                callback=self._audio_callback
            )
            self.stream.start()
            self.is_capturing = True
            self.quality_timer.start()

            self.logger.info("Audio capture started successfully")

        except Exception as e:
            self.logger.error(f"Error starting audio capture", e)
            self.error_occurred.emit(f"Error starting capture: {str(e)}")

    def stop_capture(self):
        """Stop audio capture."""
        if not self.is_capturing:
            return

        self.logger.info("Stopping audio capture")

        try:
            self.quality_timer.stop()
            if self.stream:
                self.stream.stop()
                self.stream.close()
                self.stream = None
            self.is_capturing = False

            self.logger.info("Audio capture stopped successfully")

        except Exception as e:
            self.logger.error(f"Error stopping audio capture", e)

    def _audio_callback(self, indata, frames, time_info, status):
        """Callback for audio stream."""
        if status:
            self.logger.warning(f"Audio stream status: {status}")

        try:
            # Copy audio data
            audio_data = indata.copy()

            # Calculate quality metrics
            self._calculate_quality_metrics(audio_data)

            # Emit audio data
            self.audio_data_ready.emit(audio_data, self.sample_rate)

            # Emit RMS level
            rms = np.sqrt(np.mean(audio_data ** 2))
            self.audio_level_changed.emit(float(rms))

        except Exception as e:
            self.logger.error(f"Error in audio callback", e)

    def _calculate_quality_metrics(self, audio_data: np.ndarray):
        """Calculate audio quality metrics."""
        try:
            # RMS level
            rms = np.sqrt(np.mean(audio_data ** 2))
            self.quality_metrics['rms_level'] = float(rms)

            # Peak level
            peak = np.max(np.abs(audio_data))
            self.quality_metrics['peak_level'] = float(peak)

            # Check for clipping
            clipping_threshold = 0.99
            clipping_samples = np.sum(np.abs(audio_data) > clipping_threshold)
            clipping_ratio = clipping_samples / audio_data.size
            self.quality_metrics['clipping'] = float(clipping_ratio)

            # Estimate noise floor (use 10th percentile of absolute values)
            noise_floor = np.percentile(np.abs(audio_data), 10)
            self.quality_metrics['noise_floor'] = float(noise_floor)

            # SNR estimate (dB)
            if noise_floor > 0:
                snr = 20 * np.log10(rms / noise_floor) if rms > 0 else 0
                self.quality_metrics['snr'] = float(snr)
            else:
                self.quality_metrics['snr'] = 0.0

        except Exception as e:
            self.logger.error(f"Error calculating quality metrics", e)

    def _emit_quality_metrics(self):
        """Emit quality metrics signal."""
        self.audio_quality_changed.emit(self.quality_metrics.copy())

    def test_audio_quality(self, duration: float = 2.0) -> dict:
        """
        Test audio quality for a specified duration.

        Args:
            duration: Test duration in seconds

        Returns:
            Dictionary with quality test results
        """
        self.logger.info(f"Starting audio quality test ({duration}s)")

        results = {
            'success': False,
            'duration': duration,
            'average_rms': 0.0,
            'average_peak': 0.0,
            'noise_floor': 0.0,
            'snr': 0.0,
            'clipping_detected': False,
            'message': ''
        }

        try:
            # Collect metrics
            rms_values = []
            peak_values = []
            noise_values = []

            was_capturing = self.is_capturing
            if not was_capturing:
                self.start_capture()

            # Collect data for specified duration
            start_time = time.time()
            while time.time() - start_time < duration:
                time.sleep(0.1)
                rms_values.append(self.quality_metrics['rms_level'])
                peak_values.append(self.quality_metrics['peak_level'])
                noise_values.append(self.quality_metrics['noise_floor'])

            if not was_capturing:
                self.stop_capture()

            # Calculate averages
            results['average_rms'] = float(np.mean(rms_values))
            results['average_peak'] = float(np.mean(peak_values))
            results['noise_floor'] = float(np.mean(noise_values))

            # Calculate SNR
            if results['noise_floor'] > 0:
                results['snr'] = 20 * np.log10(results['average_rms'] / results['noise_floor'])
            else:
                results['snr'] = 0.0

            # Check for clipping
            results['clipping_detected'] = any(p > 0.99 for p in peak_values)

            # Determine quality message
            if results['clipping_detected']:
                results['message'] = "WARNING: Clipping detected! Reduce input volume."
            elif results['snr'] > 40:
                results['message'] = "Excellent audio quality"
            elif results['snr'] > 30:
                results['message'] = "Good audio quality"
            elif results['snr'] > 20:
                results['message'] = "Fair audio quality"
            else:
                results['message'] = "Poor audio quality - check microphone/input"

            results['success'] = True

            self.logger.info(f"Audio quality test completed: {results['message']}")
            self.logger.info(f"  RMS: {results['average_rms']:.4f}, SNR: {results['snr']:.2f} dB")

        except Exception as e:
            results['message'] = f"Test failed: {str(e)}"
            self.logger.error(f"Audio quality test failed", e)

        return results

    def optimize_for_sound_blaster_z(self):
        """Apply optimal settings for Sound Blaster Z SE card."""
        self.logger.info("Applying Sound Blaster Z SE optimizations")

        # Sound Blaster Z SE optimal settings
        self.sample_rate = 48000  # Native sample rate
        self.block_size = 2048  # Good balance between latency and performance
        self.channels = 2  # Stereo

        self.logger.info(f"Optimized settings: {self.sample_rate} Hz, {self.block_size} samples, {self.channels} channels")
