# RadarSuite Final v3.5.0 - Build Instructions

## Platform-Specific Build Scripts

RadarSuite uses **platform-specific build scripts** to ensure clean, optimized builds for each operating system.

### Windows Build (Windows x64 only)

**Script:** `RUN_BUILD_ALL_Win.cmd`
**Platform:** Windows 10/11 x64
**Output:** `RadarSuite_Final_v3.5.0_Windows-x64_YYYYMMDD_HHMMSS.zip`

**Requirements:**
- Windows 10/11 (64-bit)
- Python 3.11 (installed via `py -3.11` launcher)
- PowerShell (for ZIP packaging)

**Usage:**
```cmd
RUN_BUILD_ALL_Win.cmd
```

**What it builds:**
- Windows executable (.exe)
- All DLL dependencies
- Platform-specific optimizations
- Does NOT build Linux version

---

### Linux Build (Linux x64 only)

**Script:** `RUN_BUILD_ALL_Linux.sh`
**Platform:** Linux x64 (Ubuntu, Debian, Fedora, etc.)
**Output:** `RadarSuite_Final_v3.5.0_Linux-x64_YYYYMMDD_HHMMSS.zip`

**Requirements:**
- Linux x64 distribution
- Python 3.11
- zip utility (`sudo apt install zip`)

**Usage:**
```bash
chmod +x RUN_BUILD_ALL_Linux.sh
./RUN_BUILD_ALL_Linux.sh
```

**What it builds:**
- Linux binary executable
- All .so dependencies
- Platform-specific optimizations
- Does NOT build Windows version

---

## Why Separate Scripts?

### Benefits of Platform-Specific Builds:

1. **No Cross-Compilation Issues**
   - Each platform builds natively
   - No compatibility problems
   - Optimal binary performance

2. **Smaller Package Size**
   - Only platform-specific files included
   - No unnecessary binaries for other OS

3. **Faster Build Times**
   - Builds only one platform at a time
   - No wasted compilation effort

4. **Clear Separation**
   - Windows developers use Windows script
   - Linux developers use Linux script
   - No confusion about which version to run

5. **Platform Optimizations**
   - Windows: Uses PowerShell, .exe format
   - Linux: Uses bash, ELF format
   - Each optimized for target platform

---

## File Naming Convention

### Windows Build Output:
```
RadarSuite_Final_v3.5.0_Windows-x64_20251119_143052.zip
                        └─────┬────┘ └──────┬──────┘
                         Platform    Date & Time
```

### Linux Build Output:
```
RadarSuite_Final_v3.5.0_Linux-x64_20251119_143052.zip
                        └────┬───┘ └──────┬──────┘
                        Platform   Date & Time
```

This makes it immediately clear which package is for which platform.

---

## Build Process Overview

### Both Scripts Follow Same 7 Steps:

1. **Check Python 3.11** - Verify correct Python version
2. **Create Virtual Environment** - Isolated dependencies
3. **Install Requirements** - Install all packages
4. **Run Tests** - Execute test suite (optional)
5. **Clean Build Directory** - Remove old builds
6. **Build with PyInstaller** - Create executable
7. **Package to ZIP** - Create distribution archive

### Platform-Specific Differences:

| Feature | Windows | Linux |
|---------|---------|-------|
| Python Command | `py -3.11` | `python3.11` / `python3` |
| Virtual Env | `.venv\Scripts\activate.bat` | `source .venv/bin/activate` |
| Executable Extension | `.exe` | (none) |
| Package Tool | PowerShell `Compress-Archive` | `zip -r` |
| Binary Format | PE32+ | ELF 64-bit |

---

## Development Workflow

### For Windows Developers:
```cmd
# Build Windows version
RUN_BUILD_ALL_Win.cmd

# Output will be in dist/
# RadarSuite_Final_v3.5.0_Windows-x64_YYYYMMDD_HHMMSS.zip
```

### For Linux Developers:
```bash
# Build Linux version
chmod +x RUN_BUILD_ALL_Linux.sh
./RUN_BUILD_ALL_Linux.sh

# Output will be in dist/
# RadarSuite_Final_v3.5.0_Linux-x64_YYYYMMDD_HHMMSS.zip
```

### For Cross-Platform Distribution:
```
1. Build on Windows machine → Get Windows package
2. Build on Linux machine → Get Linux package
3. Distribute both packages to users
4. Users download appropriate package for their OS
```

---

## Troubleshooting

### Windows Issues:

**"Python 3.11 not found"**
```cmd
# Install Python 3.11 from python.org
# Make sure to check "Add Python to PATH"
py -3.11 --version
```

**"PowerShell not found"**
- PowerShell is built into Windows 10/11
- Check: `where powershell`

### Linux Issues:

**"python3.11 not found"**
```bash
# Ubuntu/Debian
sudo apt install python3.11 python3.11-venv

# Fedora
sudo dnf install python3.11
```

**"zip command not found"**
```bash
# Ubuntu/Debian
sudo apt install zip

# Fedora
sudo dnf install zip
```

---

## Build Output Structure

```
dist/
├── RadarSuite_Final_v3.5.0_Windows-x64_YYYYMMDD_HHMMSS.zip
│   └── RadarSuite_Final_v3.5.0_win.exe
│       + DLL files
│       + Python runtime
│       + Dependencies
│
└── RadarSuite_Final_v3.5.0_Linux-x64_YYYYMMDD_HHMMSS.zip
    └── RadarSuite_Final_v3.5.0_linux
        + .so files
        + Python runtime
        + Dependencies
```

---

## Version Information

- **Current Version:** v3.5.0
- **Windows Script:** RUN_BUILD_ALL_Win.cmd
- **Linux Script:** RUN_BUILD_ALL_Linux.sh
- **PyInstaller Version:** 6.0+
- **Python Version:** 3.11

---

## Questions?

**Q: Can I build Windows version on Linux?**
A: No, use platform-specific scripts. Build Windows on Windows, Linux on Linux.

**Q: Why not one universal build script?**
A: Platform-specific scripts ensure optimal builds, smaller packages, and no cross-compilation issues.

**Q: Which package should I download?**
A: Download the package matching your operating system:
   - Windows users: `*_Windows-x64_*.zip`
   - Linux users: `*_Linux-x64_*.zip`

**Q: Can I run Windows build on Linux (via Wine)?**
A: Not recommended. Use native Linux build for best performance.

---

**Last Updated:** 2025-11-19
**RadarSuite Version:** v3.5.0
