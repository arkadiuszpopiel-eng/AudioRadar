#!/bin/bash
# =============================================================================
#  BUILD_EXECUTABLE.sh
#
#  This script creates a standalone executable for AudioRadar using PyInstaller.
#  It will:
#  1. Create a virtual environment (if it doesn't exist)
#  2. Install all required dependencies including PyInstaller
#  3. Build the executable using PyInstaller
#  4. Place the result in the 'dist' folder
# =============================================================================

set -e

echo "========================================"
echo "AudioRadar Build Script (v10)"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 not found. Please install Python 3.11+ and add it to PATH."
    exit 1
fi

echo "Using Python: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[1/4] Creating virtual environment..."
    python3 -m venv venv
    echo "[OK] Virtual environment created."
else
    echo "[1/4] Virtual environment already exists."
fi

# Activate virtual environment
echo "[2/4] Activating virtual environment..."
source venv/bin/activate
echo "[OK] Virtual environment activated."

# Install dependencies
echo "[3/4] Installing dependencies (this may take a few minutes)..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies."
    exit 1
fi
echo "[OK] Dependencies installed."

# Check if PyInstaller is available
python -c "import PyInstaller" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[ERROR] PyInstaller not available even after installation."
    echo "Please check the installation logs above for errors."
    exit 1
fi
echo "[OK] PyInstaller is available."

# Build executable
echo "[4/4] Building executable with PyInstaller..."
pyinstaller --clean --noconfirm audio_radar.spec
if [ $? -ne 0 ]; then
    echo "[ERROR] PyInstaller build failed."
    exit 1
fi

echo ""
echo "========================================"
echo "[SUCCESS] Build completed!"
echo "========================================"
echo ""
echo "The executable is located in: dist/AudioRadar/"
echo ""
echo "To run the application:"
echo "  1. Navigate to: dist/AudioRadar/"
echo "  2. Run: ./AudioRadar"
echo ""
echo "Note: Make sure to copy config.json to the same directory as the executable"
echo "      if you want to customize settings."
echo ""
