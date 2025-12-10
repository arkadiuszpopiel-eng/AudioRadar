#!/usr/bin/env python3
"""
Radar Games ML v4.3.0 - Entry Point
Simple launcher that imports and runs the main application
"""

import sys
from pathlib import Path

# Add app directory to Python path
app_dir = Path(__file__).parent / "app"
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

# Import and run main application
from app.main import main

if __name__ == "__main__":
    sys.exit(main())
