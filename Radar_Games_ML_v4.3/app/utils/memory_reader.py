"""
Radar Games ML v4.3.1 - Game Memory Reader
ADDED v4.3.1: Player yaw detection from game process memory

Reads player rotation angle (yaw) from game memory to rotate radar display.
Supports manual offset configuration and automatic process detection.

SECURITY: Requires admin privileges for ReadProcessMemory on Windows.
"""

import ctypes
from ctypes import wintypes
import struct
import time
from typing import Optional, Tuple

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

from core.logger import log


class GameMemoryReader:
    """
    Read player yaw angle from game process memory (Windows only).

    Usage:
        reader = GameMemoryReader("ArcRaiders.exe")
        reader.set_manual_offset(0x12345678)  # Manual offset from Cheat Engine
        yaw = reader.read_player_yaw()  # 0-360 degrees

    Security:
        - Requires admin privileges (ReadProcessMemory)
        - Safe: Only reads memory, does not write
        - Game-specific: Offsets must be found via reverse engineering

    Limitations:
        - Windows only (uses kernel32.dll)
        - Offsets change with game updates (require manual update)
        - May trigger anti-cheat systems (use at own risk)
    """

    # Windows constants
    PROCESS_VM_READ = 0x0010
    PROCESS_QUERY_INFORMATION = 0x0400

    def __init__(self, process_name: str = "ArcRaiders.exe"):
        """
        Initialize memory reader for specific game process.

        Args:
            process_name: Game executable name (e.g., "ArcRaiders.exe")
        """
        self.process_name = process_name
        self.process_handle = None
        self.process_id = None
        self.base_address = None

        # Yaw offset configuration
        self.yaw_offset = None  # Must be set manually via set_manual_offset()
        self.yaw_cache = 0.0
        self.last_read_time = 0
        self.read_interval = 0.1  # Read every 100ms (10 FPS)

        # Status
        self.is_connected = False
        self.last_error = None

        # Stats
        self.total_reads = 0
        self.failed_reads = 0

        log(f"GameMemoryReader initialized for {process_name}", "INFO")

    def connect(self) -> bool:
        """
        Connect to game process and open handle.

        Returns:
            True if connection successful, False otherwise
        """
        if not PSUTIL_AVAILABLE:
            self.last_error = "psutil not available (pip install psutil)"
            log(self.last_error, "ERROR")
            return False

        try:
            # Find game process
            process_found = False
            for proc in psutil.process_iter(['name', 'pid']):
                try:
                    if proc.info['name'].lower() == self.process_name.lower():
                        self.process_id = proc.info['pid']
                        process_found = True
                        log(f"Found {self.process_name} (PID: {self.process_id})", "INFO")
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            if not process_found:
                self.last_error = f"{self.process_name} not running"
                log(self.last_error, "WARNING")
                return False

            # Open process handle with read permissions
            self.process_handle = ctypes.windll.kernel32.OpenProcess(
                self.PROCESS_VM_READ | self.PROCESS_QUERY_INFORMATION,
                False,
                self.process_id
            )

            if not self.process_handle:
                self.last_error = f"Failed to open process (admin required?)"
                log(self.last_error, "ERROR")
                return False

            # Get base address (module base)
            try:
                process = psutil.Process(self.process_id)
                # Main executable is usually first in memory_maps()
                for mmap in process.memory_maps():
                    if self.process_name.lower() in mmap.path.lower():
                        # Parse base address from memory map path
                        # Format: "path-to-exe [0x140000000-...]"
                        self.base_address = 0x140000000  # Typical UE5 base address
                        log(f"Base address: 0x{self.base_address:X}", "DEBUG")
                        break
            except Exception as e:
                log(f"Could not determine base address: {e}", "WARNING")
                self.base_address = 0x140000000  # Use typical default

            self.is_connected = True
            log(f"Connected to {self.process_name} (handle: {self.process_handle})", "INFO")
            return True

        except Exception as e:
            self.last_error = str(e)
            log(f"Failed to connect to {self.process_name}: {e}", "ERROR")
            return False

    def disconnect(self):
        """Close process handle and cleanup."""
        if self.process_handle:
            ctypes.windll.kernel32.CloseHandle(self.process_handle)
            self.process_handle = None
            self.is_connected = False
            log(f"Disconnected from {self.process_name}", "INFO")

    def set_manual_offset(self, offset: int):
        """
        Set manual yaw offset address (from Cheat Engine / ReClass).

        Args:
            offset: Memory offset for player yaw (e.g., 0x12345678)

        Example:
            # Offset found via Cheat Engine:
            reader.set_manual_offset(0x5C2A8F0)
        """
        self.yaw_offset = offset
        log(f"Manual yaw offset set: 0x{offset:X}", "INFO")

    def read_player_yaw(self, force_read: bool = False) -> float:
        """
        Read current player yaw angle from game memory.

        Args:
            force_read: Skip cache and read immediately

        Returns:
            Yaw angle in degrees (0-360), or 0.0 on failure

        Note:
            - Returns cached value if read_interval not elapsed
            - Automatically reconnects if process handle lost
            - Normalizes angle to 0-360 range
        """
        current_time = time.time()

        # Return cached value if interval not elapsed
        if not force_read and (current_time - self.last_read_time) < self.read_interval:
            return self.yaw_cache

        # Check prerequisites
        if not self.is_connected:
            if not self.connect():
                return 0.0

        if self.yaw_offset is None:
            if self.total_reads == 0:  # Log only once
                log("Yaw offset not configured - use set_manual_offset()", "WARNING")
            return 0.0

        # Calculate absolute address (base + offset)
        absolute_address = self.yaw_offset  # Could add base_address if relative

        try:
            # Read float (4 bytes) from memory
            buffer = ctypes.c_float()
            bytes_read = ctypes.c_size_t()

            success = ctypes.windll.kernel32.ReadProcessMemory(
                self.process_handle,
                ctypes.c_void_p(absolute_address),
                ctypes.byref(buffer),
                ctypes.sizeof(buffer),
                ctypes.byref(bytes_read)
            )

            if not success or bytes_read.value != ctypes.sizeof(buffer):
                self.failed_reads += 1
                if self.failed_reads % 100 == 1:  # Log every 100th failure
                    log(f"ReadProcessMemory failed (attempt {self.failed_reads})", "WARNING")
                return self.yaw_cache  # Return last known value

            # Extract yaw value
            raw_yaw = buffer.value

            # Normalize to 0-360 range
            normalized_yaw = raw_yaw % 360.0
            if normalized_yaw < 0:
                normalized_yaw += 360.0

            # Update cache
            self.yaw_cache = normalized_yaw
            self.last_read_time = current_time
            self.total_reads += 1

            # Log periodically (every 1000 reads)
            if self.total_reads % 1000 == 0:
                success_rate = (1 - self.failed_reads / max(1, self.total_reads)) * 100
                log(f"Yaw reading stats: {self.total_reads} reads, "
                    f"{success_rate:.1f}% success rate, "
                    f"current yaw={normalized_yaw:.1f}°", "VERBOSE")

            return normalized_yaw

        except Exception as e:
            self.failed_reads += 1
            self.last_error = str(e)
            if self.failed_reads % 100 == 1:
                log(f"Exception reading yaw: {e}", "ERROR")
            return self.yaw_cache

    def get_stats(self) -> dict:
        """
        Get reader statistics for diagnostics.

        Returns:
            Dict with keys: total_reads, failed_reads, success_rate, is_connected
        """
        success_rate = 0.0
        if self.total_reads > 0:
            success_rate = (1 - self.failed_reads / self.total_reads) * 100

        return {
            'total_reads': self.total_reads,
            'failed_reads': self.failed_reads,
            'success_rate': success_rate,
            'is_connected': self.is_connected,
            'last_yaw': self.yaw_cache,
            'last_error': self.last_error,
            'offset_configured': self.yaw_offset is not None
        }

    def __del__(self):
        """Cleanup on destruction."""
        self.disconnect()


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def create_arc_raiders_reader(manual_offset: Optional[int] = None) -> GameMemoryReader:
    """
    Create pre-configured reader for ARC Raiders.

    Args:
        manual_offset: Manual yaw offset (from Cheat Engine), or None to skip

    Returns:
        GameMemoryReader instance

    Example:
        # With manual offset:
        reader = create_arc_raiders_reader(0x5C2A8F0)

        # Without offset (will log warning):
        reader = create_arc_raiders_reader()
    """
    reader = GameMemoryReader("ArcRaiders.exe")

    if manual_offset is not None:
        reader.set_manual_offset(manual_offset)
    else:
        log("ARC Raiders reader created without offset - "
            "use reader.set_manual_offset() or configure in settings", "INFO")

    reader.connect()
    return reader


# ============================================================================
# TESTING / DIAGNOSTICS
# ============================================================================

if __name__ == "__main__":
    """Standalone test for GameMemoryReader."""
    print("GameMemoryReader Test")
    print("=" * 60)

    # Test basic functionality
    reader = GameMemoryReader("ArcRaiders.exe")

    if reader.connect():
        print(f"✓ Connected to process (PID: {reader.process_id})")

        # Set manual offset (example - REPLACE WITH ACTUAL OFFSET!)
        # reader.set_manual_offset(0x5C2A8F0)
        print("⚠ Manual offset not set - use Cheat Engine to find player yaw address")

        # Test reading (will return 0.0 without offset)
        for i in range(5):
            yaw = reader.read_player_yaw(force_read=True)
            print(f"  Read #{i+1}: {yaw:.2f}°")
            time.sleep(0.2)

        # Print stats
        stats = reader.get_stats()
        print(f"\nStats:")
        print(f"  Total reads: {stats['total_reads']}")
        print(f"  Failed reads: {stats['failed_reads']}")
        print(f"  Success rate: {stats['success_rate']:.1f}%")

        reader.disconnect()
    else:
        print(f"✗ Failed to connect: {reader.last_error}")
        print("  Make sure ArcRaiders.exe is running")
        print("  Make sure you have admin privileges")
