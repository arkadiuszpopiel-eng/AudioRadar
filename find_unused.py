#!/usr/bin/env python3
"""Find unused Python modules in the project"""
import os
import subprocess
from pathlib import Path

def find_unused_modules(project_dir):
    """Find Python modules that are never imported"""
    project_path = Path(project_dir)
    app_path = project_path / "app"

    # Get all Python files (excluding tests, __init__, main, run_tests)
    python_files = []
    for py_file in app_path.rglob("*.py"):
        rel_path = py_file.relative_to(app_path)
        # Skip tests, __init__, main files
        if ("tests" in rel_path.parts or
            py_file.name == "__init__.py" or
            py_file.name == "main.py" or
            py_file.name == "run_tests.py" or
            py_file.name.startswith("test_")):
            continue
        python_files.append(py_file)

    unused = []
    for py_file in python_files:
        rel_path = py_file.relative_to(app_path)
        # Convert path to module name (e.g., core/logger.py -> core.logger)
        module_name = str(rel_path).replace(os.sep, ".").replace(".py", "")

        # Search for imports of this module
        result = subprocess.run(
            ["grep", "-r", f"from {module_name}\\|import {module_name}",
             str(app_path), "--include=*.py"],
            capture_output=True,
            text=True
        )

        import_count = len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0

        if import_count == 0:
            unused.append((module_name, str(rel_path)))

    return unused

if __name__ == "__main__":
    project_dir = "/home/user/AudioRadar/RadarSuite_Windows_V4.2"
    unused = find_unused_modules(project_dir)

    if unused:
        print(f"Found {len(unused)} potentially unused modules:\n")
        for module, path in unused:
            print(f"  - {module} ({path})")
    else:
        print("No unused modules found!")
