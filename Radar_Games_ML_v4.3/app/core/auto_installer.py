"""
Automatic Dependency Installer for Radar Games ML
FIXED v4.3.1-k0013: Auto-installs missing ML dependencies without user intervention

This module automatically detects and installs missing Python packages:
- joblib (ML model persistence)
- scikit-learn (ML training)
- numpy, scipy (if somehow missing)

Runs at application startup, downloads from PyPI if needed.
"""

import subprocess
import sys
import importlib.util
from typing import List, Tuple


def check_package_installed(package_name: str) -> bool:
    """
    Check if a Python package is installed.

    Args:
        package_name: Name of the package to check (e.g., 'joblib', 'sklearn')

    Returns:
        True if installed, False otherwise
    """
    spec = importlib.util.find_spec(package_name)
    return spec is not None


def install_package(package_name: str, pip_name: str = None) -> Tuple[bool, str]:
    """
    Install a Python package using pip.

    Args:
        package_name: Name to check with importlib (e.g., 'sklearn')
        pip_name: Name to install with pip (e.g., 'scikit-learn'), defaults to package_name

    Returns:
        Tuple of (success: bool, message: str)
    """
    if pip_name is None:
        pip_name = package_name

    try:
        # Use sys.executable to ensure we use the correct Python interpreter
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet", pip_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True, f"Successfully installed {pip_name}"
    except subprocess.CalledProcessError as e:
        return False, f"Failed to install {pip_name}: {e}"
    except Exception as e:
        return False, f"Unexpected error installing {pip_name}: {e}"


def ensure_ml_dependencies() -> List[str]:
    """
    Ensure all ML dependencies are installed. Auto-installs missing packages.

    Returns:
        List of installation messages (empty if all already installed)
    """
    messages = []

    # Define required packages: (import_name, pip_name)
    required_packages = [
        ('joblib', 'joblib'),
        ('sklearn', 'scikit-learn'),
        ('numpy', 'numpy'),
        ('scipy', 'scipy'),
    ]

    for import_name, pip_name in required_packages:
        if not check_package_installed(import_name):
            messages.append(f"⬇️ Installing {pip_name} from PyPI...")
            success, msg = install_package(import_name, pip_name)
            messages.append(f"  {'✅' if success else '❌'} {msg}")

            if not success:
                messages.append(f"  ⚠️ WARNING: {import_name} installation failed!")
                messages.append(f"  💡 Try manually: pip install {pip_name}")

    if not messages:
        messages.append("✅ All ML dependencies already installed")

    return messages


def ensure_all_dependencies() -> List[str]:
    """
    Ensure ALL application dependencies are installed.

    This is called at application startup to guarantee all required packages exist.
    Downloads from internet (PyPI) if needed.

    Returns:
        List of installation messages
    """
    all_messages = []

    # Header
    all_messages.append("=" * 70)
    all_messages.append("Radar Games ML - Automatic Dependency Check")
    all_messages.append("=" * 70)

    # Check and install ML dependencies
    ml_messages = ensure_ml_dependencies()
    all_messages.extend(ml_messages)

    # Footer
    all_messages.append("=" * 70)
    all_messages.append("Dependency check complete!")
    all_messages.append("")

    return all_messages


if __name__ == "__main__":
    # Test the auto-installer
    messages = ensure_all_dependencies()
    for msg in messages:
        print(msg)
