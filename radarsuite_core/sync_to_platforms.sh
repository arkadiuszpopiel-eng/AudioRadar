#!/bin/bash
# RadarSuite Core - Synchronization Script
# Copies shared modules to platform-specific versions
# Usage: ./sync_to_platforms.sh [windows|linux|both]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

WINDOWS_APP="$REPO_ROOT/RadarSuite_Windows_V4.2/app"
LINUX_APP="$REPO_ROOT/RadarSuite_Linux_V4.2/app"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

sync_to_windows() {
    echo -e "${YELLOW}Syncing to Windows V4.2...${NC}"

    if [ ! -d "$WINDOWS_APP" ]; then
        echo -e "${RED}Error: Windows app directory not found: $WINDOWS_APP${NC}"
        return 1
    fi

    # Sync detection modules
    cp -v "$SCRIPT_DIR/detection/footstep.py" "$WINDOWS_APP/detection/"
    cp -v "$SCRIPT_DIR/detection/shot.py" "$WINDOWS_APP/detection/"
    cp -v "$SCRIPT_DIR/detection/machine.py" "$WINDOWS_APP/detection/"
    cp -v "$SCRIPT_DIR/detection/spectral.py" "$WINDOWS_APP/detection/"
    cp -v "$SCRIPT_DIR/detection/worker.py" "$WINDOWS_APP/detection/"

    # Sync tracking modules
    cp -v "$SCRIPT_DIR/tracking/target.py" "$WINDOWS_APP/tracking/"
    cp -v "$SCRIPT_DIR/tracking/threat.py" "$WINDOWS_APP/tracking/"

    # Sync core modules (except platform-specific)
    cp -v "$SCRIPT_DIR/core/constants.py" "$WINDOWS_APP/core/"
    cp -v "$SCRIPT_DIR/core/config.py" "$WINDOWS_APP/core/"
    cp -v "$SCRIPT_DIR/core/confidence.py" "$WINDOWS_APP/core/"
    cp -v "$SCRIPT_DIR/core/di.py" "$WINDOWS_APP/core/"
    cp -v "$SCRIPT_DIR/core/logger.py" "$WINDOWS_APP/core/"
    cp -v "$SCRIPT_DIR/core/translations.py" "$WINDOWS_APP/core/"

    # Sync utils
    cp -v "$SCRIPT_DIR/utils/audio_scanner.py" "$WINDOWS_APP/utils/"
    cp -v "$SCRIPT_DIR/utils/game_detector.py" "$WINDOWS_APP/utils/"
    cp -v "$SCRIPT_DIR/utils/performance.py" "$WINDOWS_APP/utils/"

    echo -e "${GREEN}Windows sync complete!${NC}"
}

sync_to_linux() {
    echo -e "${YELLOW}Syncing to Linux V4.2...${NC}"

    if [ ! -d "$LINUX_APP" ]; then
        echo -e "${RED}Error: Linux app directory not found: $LINUX_APP${NC}"
        return 1
    fi

    # Sync detection modules
    cp -v "$SCRIPT_DIR/detection/footstep.py" "$LINUX_APP/detection/"
    cp -v "$SCRIPT_DIR/detection/shot.py" "$LINUX_APP/detection/"
    cp -v "$SCRIPT_DIR/detection/machine.py" "$LINUX_APP/detection/"
    cp -v "$SCRIPT_DIR/detection/spectral.py" "$LINUX_APP/detection/"
    cp -v "$SCRIPT_DIR/detection/worker.py" "$LINUX_APP/detection/"

    # Sync tracking modules
    cp -v "$SCRIPT_DIR/tracking/target.py" "$LINUX_APP/tracking/"
    cp -v "$SCRIPT_DIR/tracking/threat.py" "$LINUX_APP/tracking/"

    # Sync core modules (except platform-specific)
    cp -v "$SCRIPT_DIR/core/constants.py" "$LINUX_APP/core/"
    cp -v "$SCRIPT_DIR/core/config.py" "$LINUX_APP/core/"
    cp -v "$SCRIPT_DIR/core/confidence.py" "$LINUX_APP/core/"
    cp -v "$SCRIPT_DIR/core/di.py" "$LINUX_APP/core/"
    cp -v "$SCRIPT_DIR/core/logger.py" "$LINUX_APP/core/"
    cp -v "$SCRIPT_DIR/core/translations.py" "$LINUX_APP/core/"

    # Sync utils
    cp -v "$SCRIPT_DIR/utils/audio_scanner.py" "$LINUX_APP/utils/"
    cp -v "$SCRIPT_DIR/utils/game_detector.py" "$LINUX_APP/utils/"
    cp -v "$SCRIPT_DIR/utils/performance.py" "$LINUX_APP/utils/"

    echo -e "${GREEN}Linux sync complete!${NC}"
}

case "${1:-both}" in
    windows|win|w)
        sync_to_windows
        ;;
    linux|lin|l)
        sync_to_linux
        ;;
    both|all|a)
        sync_to_windows
        echo ""
        sync_to_linux
        ;;
    *)
        echo "Usage: $0 [windows|linux|both]"
        echo "  windows, win, w  - Sync to Windows V4.2 only"
        echo "  linux, lin, l    - Sync to Linux V4.2 only"
        echo "  both, all, a     - Sync to both platforms (default)"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Synchronization complete!${NC}"
echo "Note: Platform-specific files (audio/engine.py, version.py) were NOT synced."
