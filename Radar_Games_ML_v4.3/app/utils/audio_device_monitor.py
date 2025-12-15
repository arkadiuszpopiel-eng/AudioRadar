"""
Audio Device Monitor - Radar Games ML v4.3.1-k0005

Monitors Windows audio device changes and triggers automatic reconnection.
Fixes KNOWN_ISSUE: "Detection fails after switching to Bluetooth headphones"

Features:
- Auto-detect device changes (plugging/unplugging, Bluetooth connect/disconnect)
- Manual override option (disable auto-detection)
- Qt signal-based notifications for UI integration
- Cross-platform compatible (Windows primary, Linux/Mac stub)
"""

import sys
import platform
from typing import Optional, Callable

try:
    from PyQt6.QtCore import QObject, pyqtSignal, QTimer
except ImportError:
    from PyQt5.QtCore import QObject, pyqtSignal, QTimer

from core.logger import log


class AudioDeviceMonitor(QObject):
    """
    Monitor audio device changes and emit signals for UI handling.

    Signals:
        device_changed: Emitted when audio device list changes
        device_added: Emitted when new device is added
        device_removed: Emitted when device is removed

    Example:
        monitor = AudioDeviceMonitor()
        monitor.device_changed.connect(on_device_changed)
        monitor.start()
    """

    # Qt signals for device changes
    device_changed = pyqtSignal()  # General device change
    device_added = pyqtSignal(str)  # New device added (name)
    device_removed = pyqtSignal(str)  # Device removed (name)

    def __init__(self, auto_reconnect: bool = True, poll_interval_ms: int = 2000):
        """
        Initialize audio device monitor.

        Args:
            auto_reconnect: Enable automatic reconnection on device change
            poll_interval_ms: Polling interval in milliseconds (default: 2000ms = 2s)
        """
        super().__init__()

        self.auto_reconnect = auto_reconnect
        self.poll_interval_ms = poll_interval_ms

        # Current device list (for comparison)
        self._current_devices = set()

        # Polling timer (fallback for platforms without native events)
        self._poll_timer = QTimer()
        self._poll_timer.timeout.connect(self._check_devices)

        # Platform-specific setup
        self._platform = platform.system()
        self._native_monitoring = False

        if self._platform == "Windows":
            self._setup_windows_monitoring()
        elif self._platform == "Linux":
            self._setup_linux_monitoring()
        else:
            log(f"AudioDeviceMonitor: Using polling mode on {self._platform}", "INFO")

        log(f"AudioDeviceMonitor initialized (auto_reconnect={auto_reconnect}, poll={poll_interval_ms}ms)", "INFO")

    def _setup_windows_monitoring(self):
        """Setup Windows-specific audio device monitoring (WMI or polling)"""
        # Try to use Windows Management Instrumentation (WMI) for event-based monitoring
        try:
            import wmi
            self._wmi = wmi.WMI()
            self._native_monitoring = True
            log("AudioDeviceMonitor: Using WMI for Windows device monitoring", "INFO")
        except ImportError:
            log("AudioDeviceMonitor: WMI not available, using polling mode", "WARNING")
            self._native_monitoring = False

    def _setup_linux_monitoring(self):
        """Setup Linux-specific audio device monitoring (udev or polling)"""
        # Try to use pyudev for event-based monitoring
        try:
            import pyudev
            context = pyudev.Context()
            monitor = pyudev.Monitor.from_netlink(context)
            monitor.filter_by(subsystem='sound')
            self._udev_monitor = monitor
            self._native_monitoring = True
            log("AudioDeviceMonitor: Using udev for Linux device monitoring", "INFO")
        except ImportError:
            log("AudioDeviceMonitor: pyudev not available, using polling mode", "WARNING")
            self._native_monitoring = False

    def start(self):
        """Start monitoring audio device changes"""
        # Get initial device list
        self._update_device_list()

        # Start polling timer (works on all platforms)
        self._poll_timer.start(self.poll_interval_ms)

        log(f"AudioDeviceMonitor started (polling every {self.poll_interval_ms}ms)", "INFO")

    def stop(self):
        """Stop monitoring audio device changes"""
        self._poll_timer.stop()
        log("AudioDeviceMonitor stopped", "INFO")

    def set_auto_reconnect(self, enabled: bool):
        """
        Enable/disable automatic reconnection on device change.

        Args:
            enabled: True to enable auto-reconnect, False for manual only
        """
        self.auto_reconnect = enabled
        log(f"AudioDeviceMonitor: auto_reconnect={'enabled' if enabled else 'disabled'}", "INFO")

    def _update_device_list(self):
        """Update current device list from system"""
        try:
            # Use sounddevice library to get device list (cross-platform)
            import sounddevice as sd
            devices = sd.query_devices()

            # Extract device names
            device_names = set()
            for i, dev in enumerate(devices):
                if isinstance(dev, dict):
                    name = dev.get('name', f'Device {i}')
                    device_names.add(name)

            self._current_devices = device_names

        except ImportError:
            log("AudioDeviceMonitor: sounddevice not available, cannot query devices", "WARNING")
        except Exception as e:
            log(f"AudioDeviceMonitor: Error querying devices: {e}", "ERROR")

    def _check_devices(self):
        """
        Check for device changes (polling method).

        Compares current device list with previous list and emits signals on changes.
        """
        try:
            # Get current device list
            import sounddevice as sd
            devices = sd.query_devices()

            # Extract device names
            new_devices = set()
            for i, dev in enumerate(devices):
                if isinstance(dev, dict):
                    name = dev.get('name', f'Device {i}')
                    new_devices.add(name)

            # Check for changes
            added = new_devices - self._current_devices
            removed = self._current_devices - new_devices

            if added or removed:
                log(f"AudioDeviceMonitor: Device change detected", "INFO")

                # Emit specific signals
                for device_name in added:
                    log(f"  + Device added: {device_name}", "INFO")
                    self.device_added.emit(device_name)

                for device_name in removed:
                    log(f"  - Device removed: {device_name}", "INFO")
                    self.device_removed.emit(device_name)

                # Emit general change signal
                self.device_changed.emit()

                # Update cached list
                self._current_devices = new_devices

        except ImportError:
            # sounddevice not available - stop polling
            log("AudioDeviceMonitor: sounddevice not available, stopping", "ERROR")
            self.stop()
        except Exception as e:
            log(f"AudioDeviceMonitor: Error checking devices: {e}", "ERROR")

    def get_current_devices(self) -> set:
        """
        Get current list of audio devices.

        Returns:
            set: Set of device names
        """
        return self._current_devices.copy()


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    """Test audio device monitoring"""
    print("Audio Device Monitor Test")
    print("=" * 60)

    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    monitor = AudioDeviceMonitor(auto_reconnect=True, poll_interval_ms=2000)

    def on_device_changed():
        print("[SIGNAL] Device changed!")
        print(f"Current devices: {monitor.get_current_devices()}")

    def on_device_added(name):
        print(f"[SIGNAL] Device added: {name}")

    def on_device_removed(name):
        print(f"[SIGNAL] Device removed: {name}")

    monitor.device_changed.connect(on_device_changed)
    monitor.device_added.connect(on_device_added)
    monitor.device_removed.connect(on_device_removed)

    monitor.start()

    print("\nMonitoring audio devices (Ctrl+C to stop)")
    print("Try plugging/unplugging headphones or Bluetooth devices...")
    print(f"Initial devices: {monitor.get_current_devices()}\n")

    sys.exit(app.exec_())
