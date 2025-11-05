# Audio Radar - Installation Guide

This guide provides detailed installation instructions for Audio Radar on Windows 11.

## System Requirements

- **Operating System**: Windows 11 or Windows 10 (64-bit)
- **Python**: Version 3.8 or newer
- **RAM**: 4 GB minimum, 8 GB recommended
- **Sound Card**: Any with loopback capability
  - Sound Blaster Z SE (recommended)
  - Realtek HD Audio with Stereo Mix
  - Any WASAPI-compatible audio device

## Step-by-Step Installation

### 1. Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check "Add Python to PATH" during installation
4. Verify installation:
```bash
python --version
```

### 2. Enable Audio Loopback

#### For Sound Blaster Z SE:
1. Open Sound Blaster Control Panel
2. Go to "Recording" settings
3. Enable "What U Hear" or "Stereo Mix"
4. Set it as the default recording device

#### For Windows Built-in Audio:
1. Right-click the speaker icon in the system tray
2. Select "Sounds"
3. Go to the "Recording" tab
4. Right-click in the empty area and select "Show Disabled Devices"
5. Right-click "Stereo Mix" and select "Enable"
6. Right-click "Stereo Mix" again and select "Set as Default Device"

### 3. Clone or Download Audio Radar

#### Option A: Using Git
```bash
git clone https://github.com/arkadiuszpopiel-eng/AudioRadar.git
cd AudioRadar
```

#### Option B: Download ZIP
1. Go to the GitHub repository
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file to your desired location
4. Open Command Prompt or PowerShell in that folder

### 4. Install Dependencies

#### Option A: Using requirements.txt
```bash
pip install -r requirements.txt
```

#### Option B: Using the provided script
```bash
cd audio_radar_v10\audio_radar
RUN_BUILD_ALL.cmd
```

#### Option C: Manual installation
```bash
pip install sounddevice>=0.4.6
pip install numpy>=1.21.0
pip install scipy>=1.7.0
pip install pygame>=2.5.0
```

### 5. Verify Installation

```bash
cd audio_radar_v10\audio_radar
python main.py --list-devices
```

You should see a list of available audio input and output devices.

## Configuration

### 1. Find Your Loopback Device

Run:
```bash
python main.py --list-devices
```

Look for your loopback device (e.g., "Stereo Mix", "What U Hear") and note its index number.

### 2. Edit Configuration

Open `audio_radar_v10\audio_radar\config.json` in a text editor and set:

```json
{
  "input_device": 5,  // Replace 5 with your device index
  ...
}
```

### 3. Test Audio Radar

1. Start your favorite game with audio enabled
2. Run Audio Radar:
```bash
python main.py
```
3. You should see the radar window appear
4. Make sounds in the game (footsteps, gunshots) and watch the radar light up

## Troubleshooting

### Python Not Found
**Problem**: `'python' is not recognized as an internal or external command`

**Solution**: 
1. Reinstall Python and check "Add Python to PATH"
2. Or use the full path: `C:\Python311\python.exe`

### Module Not Found Errors
**Problem**: `ModuleNotFoundError: No module named 'sounddevice'`

**Solution**:
```bash
pip install sounddevice numpy scipy pygame
```

### No Audio Devices Listed
**Problem**: `--list-devices` shows no input devices

**Solution**:
1. Ensure loopback is enabled in Windows Sound settings
2. Try running Command Prompt as Administrator
3. Restart your computer after enabling Stereo Mix

### Audio Not Detected
**Problem**: Radar window opens but doesn't respond to game audio

**Solution**:
1. Verify loopback device is set as default recording device
2. Test loopback with Windows Voice Recorder:
   - Open Voice Recorder
   - Record while playing game audio
   - Play back - you should hear the game audio
3. Check game audio is not muted
4. Try lowering detection thresholds in config.json:
```json
{
  "detection": {
    "shot_peak_threshold": 0.4,
    "footstep_std_threshold": 0.03
  }
}
```

### High False Positive Rate
**Problem**: Radar lights up constantly even without footsteps/shots

**Solution**:
1. Increase detection thresholds in config.json:
```json
{
  "detection": {
    "shot_peak_threshold": 0.7,
    "footstep_std_threshold": 0.08
  }
}
```
2. Enable bandpass filtering:
```json
{
  "detection": {
    "enable_bandpass_filter": true
  }
}
```

### Performance Issues
**Problem**: Audio Radar uses too much CPU

**Solution**:
1. Increase blocksize in config.json:
```json
{
  "audio": {
    "blocksize": 2048
  }
}
```
2. Disable bandpass filtering if not needed
3. Close other audio applications

## Advanced Setup

### Multi-Channel Audio (5.1/7.1)

For best directional accuracy:

1. Configure your game to output 5.1 or 7.1 surround sound
2. In Windows Sound settings, set your output device to 5.1 or 7.1
3. Ensure loopback captures all channels
4. Update config.json:
```json
{
  "audio": {
    "channels": 6  // 6 for 5.1, 8 for 7.1
  }
}
```

### Running as Startup Application

To run Audio Radar automatically when Windows starts:

1. Create a shortcut to the batch file:
```
audio_radar_v10\audio_radar\RUN_BUILD_ALL.cmd
```

2. Press `Win+R`, type `shell:startup`, press Enter

3. Copy the shortcut to the Startup folder

## Getting Help

If you continue to experience issues:

1. Check the log file: `audio_radar_v10\audio_radar\log_v10.txt`
2. Open an issue on GitHub with:
   - Your Python version (`python --version`)
   - Your Windows version
   - The contents of the log file
   - Description of the problem
3. Review existing issues on GitHub

## Updating Audio Radar

To update to the latest version:

```bash
cd AudioRadar
git pull origin main
pip install -r requirements.txt --upgrade
```

Or download the latest release from GitHub and repeat the installation steps.

## Uninstallation

To remove Audio Radar:

1. Delete the AudioRadar folder
2. (Optional) Uninstall Python packages:
```bash
pip uninstall sounddevice numpy scipy pygame
```
3. (Optional) Disable Stereo Mix in Windows Sound settings

---

For more information, see the main [README.md](README.md) or visit the [GitHub repository](https://github.com/arkadiuszpopiel-eng/AudioRadar).
