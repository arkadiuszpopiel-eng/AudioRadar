"""
RadarSuite Centralized Version Management

FIXED v4.2.0: Single source of truth for version across all modules
- Build scripts import from here
- Runtime displays this version
- Consistent versioning eliminates discrepancies
"""

# Main version
__version__ = "4.2.1"

# Full version string with game-specific suffix
__version_full__ = "4.2.1-ARC-Raiders"

# Version components
VERSION_MAJOR = 4
VERSION_MINOR = 2
VERSION_PATCH = 1

# Build metadata
BUILD_TARGET = "ARC Raiders"
BUILD_PLATFORM = "Windows"  # or "Linux" depending on build

# Version history (for reference)
VERSION_HISTORY = {
    "4.2.1": "Deep static analysis fixes, import path corrections, exception handling improvements",
    "4.2.0": "ARC Raiders Edition - MFCC features, shot detection, surface classification, machine detection",
    "4.1.2": "Adaptive noise floor, type-aware tracking, detached window cleanup",
    "4.1.0": "Multi-target tracking improvements, UI enhancements",
    "4.0.0": "Major architecture refactor, modular detection pipeline",
    "3.4.1": "Platform gaming integration (Steam, Epic, etc.)",
    "3.1.0": "Auto-suggestion for loopback mode",
    "2.3.0": "Initial stable release"
}

def get_version_string(include_suffix=True):
    """
    Get formatted version string

    Args:
        include_suffix: If True, includes game-specific suffix

    Returns:
        str: Version string (e.g., "4.2.0-ARC-Raiders" or "4.2.0")
    """
    if include_suffix:
        return __version_full__
    else:
        return __version__

def get_version_tuple():
    """
    Get version as tuple for comparisons

    Returns:
        tuple: (major, minor, patch)
    """
    return (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)

def get_build_info():
    """
    Get complete build information dictionary

    Returns:
        dict: Build metadata
    """
    return {
        'version': __version__,
        'version_full': __version_full__,
        'major': VERSION_MAJOR,
        'minor': VERSION_MINOR,
        'patch': VERSION_PATCH,
        'target': BUILD_TARGET,
        'platform': BUILD_PLATFORM
    }

if __name__ == "__main__":
    # Display version when run directly
    print(f"RadarSuite Version: {__version_full__}")
    print(f"Target: {BUILD_TARGET}")
    print(f"Platform: {BUILD_PLATFORM}")
    print(f"\nVersion History:")
    for ver, desc in VERSION_HISTORY.items():
        print(f"  {ver}: {desc}")
