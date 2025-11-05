#!/usr/bin/env python
"""Setup script for Audio Radar."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read version from the audio_radar_v10 package
version_file = Path(__file__).parent / "audio_radar_v10" / "audio_radar" / "VERSION.txt"
version = "0.10.0"
if version_file.exists():
    version_content = version_file.read_text(encoding="utf-8").strip()
    if version_content:
        version = version_content

setup(
    name="audio-radar",
    version=version,
    description="Real-time audio direction detection for gaming",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Arkadiusz Popiel",
    author_email="arkadiusz.popiel@example.com",
    url="https://github.com/arkadiuszpopiel-eng/AudioRadar",
    packages=find_packages(where="audio_radar_v10"),
    package_dir={"": "audio_radar_v10"},
    python_requires=">=3.8",
    install_requires=[
        "sounddevice>=0.4.6",
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "pygame>=2.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "mypy>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "audio-radar=audio_radar.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
    ],
    keywords="audio gaming radar sound detection accessibility",
)
