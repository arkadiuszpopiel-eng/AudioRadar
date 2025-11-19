#!/bin/bash
# ============================================================================
# RadarSuite Linux V4 - Linux Build Script
# Builds standalone Linux executable using PyInstaller
# Platform: Linux x64 ONLY
# Requires: Python 3.11 + Linux system libraries
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Set version
VERSION="v4.0.0"
PLATFORM="Linux64"
BUILD_DATE=$(date +"%Y-%m-%d")
BUILD_TIME=$(date +"%H:%M:%S")

# Log file - SEPARATE FOR LINUX VERSION
LOG_FILE="build_linux.log"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Function to print step headers
print_step() {
    echo -e "${BLUE}$1${NC}"
    log "$1"
}

# Function to print success
print_success() {
    echo -e "${GREEN}   - $1${NC}"
    log "$1"
}

# Function to print error
print_error() {
    echo -e "${RED}[ERROR] $1${NC}"
    log "[ERROR] $1"
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
    log "[WARNING] $1"
}

# Start logging
echo ""
echo "========================================================================"
echo "  RadarSuite Linux V4 - Build System"
echo "  Building Linux standalone executable with PyInstaller"
echo "  Platform: Linux x64 ONLY"
echo "========================================================================"
log "============================================================"
log "BUILD STARTED - RadarSuite Linux V4"
log "============================================================"
log "Version: $VERSION"
log "Script Directory: $SCRIPT_DIR"
log "Build Date: $BUILD_DATE"
log "Build Time: $BUILD_TIME"
echo ""

echo "========================================================================"
echo "  RadarSuite Linux V4 - Dedicated Linux Build"
echo "  This version builds ONLY for Linux x64"
echo "========================================================================"
echo ""

echo -e "${YELLOW}[INFO] This is the LINUX-ONLY version${NC}"
echo "   Windows builds: Use RadarSuite_Windows_V4 directory"
echo "   All builds are separate and won't interfere"
log "[INFO] Platform: Linux x64 only - separate build directory"
echo ""

# ============================================================================
# STEP 1: Check Python 3.11
# ============================================================================
print_step "[STEP 1/7] Checking Python 3.11 installation..."

# Try different Python commands
PYTHON_CMD=""
for cmd in python3.11 python3 python; do
    if command -v $cmd &> /dev/null; then
        VERSION_OUTPUT=$($cmd --version 2>&1)
        if [[ $VERSION_OUTPUT == *"Python 3.11"* ]]; then
            PYTHON_CMD=$cmd
            print_success "Found: $VERSION_OUTPUT"
            log "Found: $VERSION_OUTPUT (command: $cmd)"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    print_error "Python 3.11 is not installed or not in PATH!"
    echo ""
    echo "Please install Python 3.11:"
    echo "  Ubuntu/Debian: sudo apt install python3.11 python3.11-venv"
    echo "  Fedora: sudo dnf install python3.11"
    echo "  macOS: brew install python@3.11"
    exit 1
fi
echo ""

# ============================================================================
# STEP 2: Create/Activate virtual environment
# ============================================================================
print_step "[STEP 2/7] Creating/Activating virtual environment..."

if [ ! -d ".venv" ]; then
    print_success "Creating new venv..."
    $PYTHON_CMD -m venv .venv >> "$LOG_FILE" 2>&1
    if [ $? -ne 0 ]; then
        print_error "Failed to create virtual environment"
        exit 1
    fi
else
    print_success "Using existing venv"
fi

# Activate virtual environment
source .venv/bin/activate
if [ $? -ne 0 ]; then
    print_error "Failed to activate virtual environment"
    exit 1
fi

print_success "Virtual environment activated"
echo ""

# ============================================================================
# STEP 3: Upgrade pip
# ============================================================================
print_step "[STEP 3/7] Upgrading pip, setuptools, wheel..."

python -m pip install --upgrade pip setuptools wheel >> "$LOG_FILE" 2>&1
if [ $? -ne 0 ]; then
    print_warning "pip upgrade had issues, continuing..."
else
    print_success "pip upgraded"
fi
echo ""

# ============================================================================
# STEP 4: Install requirements
# ============================================================================
print_step "[STEP 4/7] Installing requirements..."
echo ""

# Check for Linux system dependencies first
echo -e "${YELLOW}Checking Linux system dependencies...${NC}"
missing_libs=()

# Check for PulseAudio
if ! ldconfig -p | grep -q libpulse.so; then
    missing_libs+=("libpulse0 (PulseAudio)")
fi

# Check for PortAudio
if ! ldconfig -p | grep -q libportaudio.so; then
    missing_libs+=("portaudio19-dev")
fi

# Check for XCB libraries
for lib in libxcb-xinerama libxcb-image libxcb-icccm libxcb-keysyms libxkbcommon-x11; do
    if ! ldconfig -p | grep -q "$lib.so"; then
        missing_libs+=("$lib")
    fi
done

if [ ${#missing_libs[@]} -gt 0 ]; then
    print_warning "Missing system libraries detected:"
    for lib in "${missing_libs[@]}"; do
        echo "     - $lib"
    done
    echo ""
    echo "Install with:"
    echo "  Ubuntu/Debian: sudo apt install libpulse0 portaudio19-dev libxcb-xinerama0 libxcb-image0 libxcb-icccm4 libxcb-keysyms1 libxkbcommon-x11-0"
    echo "  Fedora/RHEL: sudo dnf install pulseaudio-libs portaudio-devel libxcb xcb-util-image xcb-util-wm xcb-util-keysyms libxkbcommon-x11"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install from requirements-linux.txt (LINUX-SPECIFIC)
if [ -f "requirements-linux.txt" ]; then
    print_success "Installing from requirements-linux.txt (Linux optimized)..."
    pip install -r requirements-linux.txt >> "$LOG_FILE" 2>&1
    if [ $? -ne 0 ]; then
        print_error "Failed to install requirements from requirements-linux.txt"
        echo "Check $LOG_FILE for details"
        exit 1
    fi
elif [ -f "requirements.txt" ]; then
    print_success "Installing from requirements.txt..."
    pip install -r requirements.txt >> "$LOG_FILE" 2>&1
    if [ $? -ne 0 ]; then
        print_error "Failed to install requirements from requirements.txt"
        echo "Check $LOG_FILE for details"
        exit 1
    fi
else
    print_error "No requirements file found!"
    exit 1
fi

print_success "All Python requirements installed"
echo ""

# ============================================================================
# STEP 5: Verify installation
# ============================================================================
print_step "[STEP 5/7] Verifying installation..."

# Verify modules without initializing native libraries (sounddevice/soundcard)
python -c "
import sys
import importlib.util

modules = ['PyQt5', 'pyqtgraph', 'OpenGL', 'numpy', 'scipy', 'sounddevice', 'soundcard', 'psutil', 'PyInstaller']
failed = []

for module_name in modules:
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        failed.append(module_name)
    else:
        print(f'✓ {module_name}')

if failed:
    print(f'Failed to find modules: {failed}', file=sys.stderr)
    sys.exit(1)
else:
    print('All modules installed OK')
" >> "$LOG_FILE" 2>&1

if [ $? -ne 0 ]; then
    print_error "Module verification failed!"
    echo ""
    echo "Some required modules could not be imported."
    echo "Please check $LOG_FILE for details."
    echo ""
    echo "Common fixes:"
    echo "  - Install system dependencies: sudo apt install portaudio19-dev (Ubuntu/Debian)"
    echo "  - Install libGL: sudo apt install libgl1-mesa-glx (for PyOpenGL)"
    exit 1
fi

print_success "All modules verified successfully (package check only)"
print_warning "Note: sounddevice/soundcard require PortAudio at runtime"
echo ""

# Verify PyInstaller command
pyinstaller --version >> "$LOG_FILE" 2>&1
if [ $? -ne 0 ]; then
    print_error "PyInstaller not available!"
    echo ""
    echo "PyInstaller was installed but the command is not found."
    echo "This might be a PATH issue. Try:"
    echo "  1. Deactivate and reactivate the virtual environment:"
    echo "     deactivate && source .venv/bin/activate"
    echo "  2. Or run PyInstaller directly:"
    echo "     python -m PyInstaller"
    exit 1
fi

PYINSTALLER_VERSION=$(pyinstaller --version 2>&1 | head -1)
print_success "PyInstaller $PYINSTALLER_VERSION is available"
echo ""

# ============================================================================
# STEP 6: Build EXE with PyInstaller
# ============================================================================
print_step "[STEP 6/7] Building executable with PyInstaller..."
echo ""

# Clean previous build
if [ -d "build" ]; then
    print_success "Cleaning old build directory..."
    rm -rf build
fi

if [ -d "dist" ]; then
    print_success "Cleaning old dist directory..."
    rm -rf dist
fi

print_success "Running PyInstaller..."
log "Running PyInstaller with spec file..."

# Set Qt platform to offscreen mode (no GUI needed during build)
export QT_QPA_PLATFORM=offscreen

pyinstaller --clean --noconfirm build_tools/radarsuite_linux.spec >> "$LOG_FILE" 2>&1

if [ $? -ne 0 ]; then
    print_error "PyInstaller build failed!"
    echo ""
    echo "Build failed. Check $LOG_FILE for details."
    echo ""
    echo "Last 20 lines of log:"
    tail -20 "$LOG_FILE"
    exit 1
fi

echo ""
print_success "Executable built successfully!"

# Verify executable exists
APP_DIR="dist/RadarSuite_Linux"
if [ ! -f "$APP_DIR/RadarSuite_Final" ]; then
    print_error "Executable not found in dist!"
    exit 1
fi

# Make executable
chmod +x "$APP_DIR/RadarSuite_Final"

print_success "Executable location: $APP_DIR/RadarSuite_Final"

# Get executable size
EXE_SIZE=$(stat -f%z "$APP_DIR/RadarSuite_Linux" 2>/dev/null || stat -c%s "$APP_DIR/RadarSuite_Linux" 2>/dev/null)
print_success "Executable size: $EXE_SIZE bytes"
echo ""

# ============================================================================
# STEP 7: Package to ZIP
# ============================================================================
print_step "[STEP 7/7] Packaging to ZIP (Linux x64 only)..."

# Create unique archive name with timestamp and platform
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ZIP_NAME="RadarSuite_Linux_V4_${VERSION}_Linux-x64_${TIMESTAMP}.zip"

print_success "Archive name: $ZIP_NAME"
log "Creating Linux archive: $ZIP_NAME"

# Check if zip command is available
if ! command -v zip &> /dev/null; then
    print_warning "zip command not found, skipping ZIP creation"
    echo "  Install zip: sudo apt install zip (Ubuntu/Debian)"
else
    # Remove old archive if exists
    if [ -f "dist/$ZIP_NAME" ]; then
        print_success "Removing old archive..."
        rm -f "dist/$ZIP_NAME"
    fi

    # Create ZIP
    print_success "Compressing..."
    cd "$APP_DIR"
    zip -r "../$ZIP_NAME" . >> "$SCRIPT_DIR/$LOG_FILE" 2>&1
    cd "$SCRIPT_DIR"

    if [ $? -ne 0 ]; then
        print_warning "ZIP creation failed"
    else
        print_success "ZIP created successfully!"

        # Get ZIP size
        ZIP_SIZE=$(stat -f%z "dist/$ZIP_NAME" 2>/dev/null || stat -c%s "dist/$ZIP_NAME" 2>/dev/null)
        print_success "ZIP size: $ZIP_SIZE bytes"
    fi
fi

echo ""
echo "========================================================================"
echo "  BUILD COMPLETED SUCCESSFULLY!"
echo "========================================================================"
echo ""
echo "Build Information:"
echo "  - Version: $VERSION"
echo "  - Date: $BUILD_DATE"
echo "  - Time: $BUILD_TIME"
echo "  - Python: $(python --version 2>&1)"
echo ""
echo "Output:"
echo "  - Executable Directory: $APP_DIR"
echo "  - Executable File: RadarSuite_Linux"
echo "  - Executable Size: $EXE_SIZE bytes"
if [ -f "dist/$ZIP_NAME" ]; then
    echo "  - ZIP Archive: dist/$ZIP_NAME"
    echo "  - ZIP Size: $ZIP_SIZE bytes"
fi
echo ""
echo "Logs:"
echo "  - Build Log: $LOG_FILE"
echo "  - Runtime log will be created as super_log.txt when you run the app"
echo ""
echo "To run the application:"
echo "  1. Go to: $APP_DIR"
echo "  2. Run: ./RadarSuite_Final"
echo ""
if [ -f "dist/$ZIP_NAME" ]; then
    echo "Or from the ZIP:"
    echo "  1. Extract: dist/$ZIP_NAME"
    echo "  2. Run: ./RadarSuite_Final"
fi
echo ""
echo "========================================================================"

log "============================================================"
log "BUILD COMPLETED SUCCESSFULLY"
log "============================================================"
echo ""
