"""Launcher script for Audio Radar GUI.

This script provides an easy entry point to launch the PyQt5-based
GUI for Audio Radar with gain and threshold controls.
"""

import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from gui import main
except ImportError:
    print("ERROR: Could not import GUI module.")
    print("Make sure gui.py is in the same directory.")
    sys.exit(1)

if __name__ == "__main__":
    sys.exit(main())
