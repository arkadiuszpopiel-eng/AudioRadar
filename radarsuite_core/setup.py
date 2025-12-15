"""
RadarSuite Core - Shared Module Package
Setup script for pip installation
"""

from setuptools import setup, find_packages

setup(
    name="radarsuite_core",
    version="4.2.0",
    description="RadarSuite shared platform-independent modules",
    author="RadarSuite Team",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "psutil>=5.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
)
