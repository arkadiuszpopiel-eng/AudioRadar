"""
Radar Games ML - Centralized Version Management

FIXED v4.2.0: Single source of truth for version across all modules
MAJOR v4.3.0: Rebranded to Radar Games ML with ML inference, graceful shutdown, live feedback
- Build scripts import from here
- Runtime displays this version
- Consistent versioning eliminates discrepancies
"""

# Main version
__version__ = "4.3.0"

# Build number (k = kompilacja/compilation)
BUILD_NUMBER = "k0001"

# Full version string with build number
__version_full__ = f"4.3.0-{BUILD_NUMBER}"

# Full version string with game-specific suffix
__version_full_target__ = f"4.3.0-{BUILD_NUMBER}-ML"

# Version components
VERSION_MAJOR = 4
VERSION_MINOR = 3
VERSION_PATCH = 0

# Build metadata
BUILD_TARGET = "Radar Games ML"
BUILD_PLATFORM = "Windows"  # or "Linux" depending on build

# Version history (for reference)
VERSION_HISTORY = {
    "4.3.0-k0001": "MAJOR RELEASE - Radar Games ML: (1) Graceful shutdown with AsyncSessionWorker cleanup, session integrity validator, auto-recovery for corrupted sessions. (2) ML Training live feedback: toast notifications, FSM state indicators, progress bars for all async operations. (3) ML Model auto-load & real-time inference: ModelRegistry, auto-load best model at startup, MLFootstepDetector integration, model management UI. Rebranded from RadarSuite to Radar Games ML.",
    "4.2.1-k0009": "CRITICAL ML Training fix - GUI freeze resolved: Implemented async session worker (background thread) for non-blocking I/O operations (directory creation, JSON/numpy saves). Added FSM (Finite State Machine) for recording states (IDLE→STARTING→RECORDING→STOPPING→IDLE). Fixed ML overlay frameless mode background rendering with custom paintEvent. Prevents Windows antivirus/disk I/O from blocking GUI thread during ML session saves.",
    "4.2.1-k0008": "Infrastructure improvements: Fixed QTimer import in military_3d.py, centralized log/report directories (log/ and raport/), migrated legacy super_log.txt, updated build scripts. All logs now in log/, all reports in raport/, both in dev and EXE modes.",
    "4.2.1-k0007": "GRADE A+ ACHIEVED: Split widgets/radar.py from 1674 lines into 7 focused modules (target_state, military_hud, minimal_radar, detachable_radar, radar_widget, military_3d, radar_3d). Maintained 100% backward compatibility via re-export layer. Improved maintainability and single responsibility principle.",
    "4.2.1-k0006": "GRADE A ACHIEVED: Major code quality improvements - refactored analyze_footstep() from 285 to 85 lines (70% reduction), added 8 modular helper methods with full docstrings, removed unused imports, fixed bare except clauses. Maintainability index significantly improved.",
    "4.2.1-k0005": "GRADE A PUSH: Fixed ALL 3 CRITICAL thread safety issues (AudioEngine, HumanFootstepDetector, SoundClassifier) - eliminated race conditions",
    "4.2.1-k0004": "Automated QA: Fixed CRITICAL AudioEngine thread safety, deep analysis (174 issues), comprehensive test plan, security scan passed",
    "4.2.1-k0003": "Critical ML Panel freeze fix - corrected import errors in ui/builder.py, waveform_timeline.py, ml_waveform.py",
    "4.2.1-k0002": "Fixed k0001 disaster - restored original ML widgets, fixed only imports (not functionality)",
    "4.2.1-k0001": "FAILED - accidentally removed ML widgets content",
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
        'version_full_target': __version_full_target__,
        'build_number': BUILD_NUMBER,
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
