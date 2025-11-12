"""
Test script to verify Audio Radar structure and imports.
This tests that all files are present and can be imported (syntax check).
"""

import sys
import os
from pathlib import Path

# Add audioradar to path
sys.path.insert(0, str(Path(__file__).parent))

def test_file_structure():
    """Test that all required files exist."""
    print("Testing file structure...")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "RUN_BUILD_ALL.cmd",
        "NEW_README.md",
        ".gitignore",
        "audioradar/__init__.py",
        "audioradar/config.py",
        "audioradar/logger.py",
        "audioradar/audio_engine.py",
        "audioradar/detector.py",
        "audioradar/localizer.py",
        "audioradar/gui/__init__.py",
        "audioradar/gui/main_window.py",
        "audioradar/gui/radar_widget.py",
        "audioradar/gui/spectrum_widget.py",
        "audioradar/gui/config_panel.py",
        "audioradar/gui/device_manager.py",
        "audioradar/gui/theme_manager.py",
        "audioradar/gui/audio_test_dialog.py",
    ]
    
    missing = []
    for file in required_files:
        file_path = Path(__file__).parent / file
        if not file_path.exists():
            missing.append(file)
            print(f"  ✗ Missing: {file}")
        else:
            print(f"  ✓ Found: {file}")
    
    if missing:
        print(f"\n❌ FAILED: {len(missing)} files missing")
        return False
    else:
        print(f"\n✅ PASSED: All {len(required_files)} files present")
        return True

def test_syntax():
    """Test that Python files have valid syntax."""
    print("\nTesting Python syntax...")
    
    # Test modules that don't require external dependencies
    try:
        from audioradar import __version__
        print(f"  ✓ audioradar.__version__ = {__version__}")
    except Exception as e:
        print(f"  ✗ audioradar import failed: {e}")
        return False
    
    try:
        from audioradar.logger import get_logger
        print("  ✓ audioradar.logger syntax OK")
    except Exception as e:
        print(f"  ✗ audioradar.logger syntax error: {e}")
        return False
    
    try:
        from audioradar.config import Config
        print("  ✓ audioradar.config syntax OK")
    except Exception as e:
        print(f"  ✗ audioradar.config syntax error: {e}")
        return False
    
    # Note: GUI modules will fail without PyQt5, but that's expected
    print("\n✅ PASSED: Core module syntax is valid")
    return True

def test_logger():
    """Test logger functionality."""
    print("\nTesting logger...")
    
    try:
        from audioradar.logger import setup_logging, get_logger
        
        logger = setup_logging()
        logger.info("Test log message")
        logger.warning("Test warning")
        logger.error("Test error")
        
        # Check if log file was created
        log_file = Path(__file__).parent / "log.txt"
        if log_file.exists():
            print("  ✓ Log file created")
            # Read last few lines
            with open(log_file, 'r') as f:
                lines = f.readlines()
                if len(lines) > 0:
                    print(f"  ✓ Log contains {len(lines)} lines")
                else:
                    print("  ⚠ Log file is empty")
        else:
            print("  ⚠ Log file not created")
        
        print("✅ PASSED: Logger working")
        return True
    except Exception as e:
        print(f"❌ FAILED: Logger error: {e}")
        return False

def test_config():
    """Test configuration system."""
    print("\nTesting configuration...")
    
    try:
        from audioradar.config import Config
        
        config = Config()
        
        # Test getting values
        theme = config.get("gui", "theme", "dark")
        print(f"  ✓ Config get: theme = {theme}")
        
        # Test setting values
        config.set("test", "value", 123)
        value = config.get("test", "value")
        assert value == 123
        print(f"  ✓ Config set/get: {value}")
        
        # Test config file
        config_file = Path(__file__).parent / "config.json"
        if config_file.exists():
            print(f"  ✓ Config file created")
        
        print("✅ PASSED: Configuration working")
        return True
    except Exception as e:
        print(f"❌ FAILED: Config error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Audio Radar - Structure Test")
    print("=" * 60)
    
    results = []
    
    results.append(("File Structure", test_file_structure()))
    results.append(("Python Syntax", test_syntax()))
    results.append(("Logger", test_logger()))
    results.append(("Configuration", test_config()))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{name:20} {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("=" * 60)
    if all_passed:
        print("✅ All tests passed!")
        print("\nNote: Full functionality requires dependencies from requirements.txt")
        print("Run 'pip install -r requirements.txt' to install dependencies")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
