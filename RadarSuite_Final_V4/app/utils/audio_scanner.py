"""
RadarSuite v3.5.0 - Audio Source Scanner
Scans and filters audio sources (games vs launchers)
"""

import psutil

from core.logger import log


class AudioSourceScanner:
    """
    Scans system for active and inactive audio sources
    Provides visualization: green = active, red = inactive
    Lists all available audio devices with real-time status

    v3.4.1: Dodano filtrowanie audio od launcherów (ignoruj Steam, Discord, etc.)
    """

    def __init__(self, platform_detector=None):
        log("AudioSourceScanner.__init__", "INFO")

        self.active_sources = []
        self.inactive_sources = []
        self.last_scan_time = 0.0
        self.scan_interval = 2.0  # Scan every 2 seconds
        self.platform_detector = platform_detector  # v3.4.1: filtrowanie launcherów

    def scan_audio_sources(self):
        """
        Scan for active and inactive audio sources
        Returns: dict with active/inactive lists and status
        """
        try:
            current_time = time.time()

            # Don't scan too frequently
            if current_time - self.last_scan_time < self.scan_interval:
                return {
                    'active': self.active_sources,
                    'inactive': self.inactive_sources,
                    'total': len(self.active_sources) + len(self.inactive_sources)
                }

            self.last_scan_time = current_time

            active = []
            inactive = []

            # Scan sounddevice sources
            if sd:
                try:
                    devices = sd.query_devices()
                    for i, dev in enumerate(devices):
                        dev_info = {
                            'name': dev['name'],
                            'index': i,
                            'channels': dev['max_input_channels'],
                            'samplerate': int(dev['default_samplerate']),
                            'backend': 'sounddevice',
                            'type': 'input' if dev['max_input_channels'] > 0 else 'output'
                        }

                        # Check if device is default (likely active)
                        try:
                            default_device = sd.query_devices(kind='input')
                            is_active = (dev['name'] == default_device['name'])
                        except (KeyError, Exception) as e:
                            log(f"Error checking default device: {e}", level="DEBUG")
                            is_active = False

                        if is_active or dev['max_input_channels'] > 0:
                            active.append(dev_info)
                        else:
                            inactive.append(dev_info)

                except Exception as e:
                    log(f"Error scanning sounddevice: {e}", "ERROR")

            # Scan soundcard loopback sources
            if sc:
                try:
                    speakers = sc.all_speakers()
                    for speaker in speakers:
                        dev_info = {
                            'name': speaker.name,
                            'index': speaker.id,
                            'channels': speaker.channels,
                            'samplerate': 48000,  # Default
                            'backend': 'soundcard',
                            'type': 'loopback'
                        }

                        # Loopback devices are considered active if they exist
                        active.append(dev_info)

                except Exception as e:
                    log(f"Error scanning soundcard: {e}", "ERROR")

            self.active_sources = active
            self.inactive_sources = inactive

            return {
                'active': self.active_sources,
                'inactive': self.inactive_sources,
                'total': len(active) + len(inactive)
            }

        except Exception as e:
            log(f"Error in AudioSourceScanner.scan_audio_sources: {e}", "ERROR")
            return {
                'active': [],
                'inactive': [],
                'total': 0
            }


# ============================================================================
# HUMAN VOICE DETECTOR (v3.0)
# ============================================================================
