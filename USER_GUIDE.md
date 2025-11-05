# Audio Radar - User Guide

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Calibration](#calibration)
4. [Advanced Configuration](#advanced-configuration)
5. [Tips and Tricks](#tips-and-tricks)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

## Getting Started

### First Time Setup

1. **Install Audio Radar** following the [INSTALL.md](INSTALL.md) guide

2. **Enable audio loopback** on your system:
   - Open Windows Sound settings (Right-click speaker icon → Sounds)
   - Go to Recording tab
   - Enable "Stereo Mix" or your sound card's loopback device
   - Set it as the default recording device

3. **Test the setup**:
   ```bash
   cd audio_radar_v10\audio_radar
   python main.py --list-devices
   ```
   
   You should see your loopback device listed.

4. **Run Audio Radar**:
   ```bash
   python main.py
   ```

## Basic Usage

### Understanding the Radar Display

The Audio Radar shows an 8-way compass:

```
      North (0°)
         |
    NW   |   NE
      \  |  /
West ----+---- East
      /  |  \
    SW   |   SE
         |
      South (180°)
```

- **Green bars**: Footsteps detected
- **Red bars**: Gunshots detected
- **Bar intensity**: Indicates sound volume (louder = brighter/larger)
- **Bar position**: Shows direction of the sound source

### Keyboard Controls

While Audio Radar is running, you can adjust the display:

| Key | Action |
|-----|--------|
| `Z` | Increase bar width |
| `X` | Decrease bar width |
| `C` | Increase bar height |
| `V` | Decrease bar height |
| `B` | Increase transparency (more opaque) |
| `N` | Decrease transparency (more transparent) |

Changes are temporary and not saved. To make permanent changes, edit `config.json`.

### Running with a Game

1. **Start your game** and ensure audio is playing
2. **Launch Audio Radar** in a separate window
3. **Position the radar** where you can see it while playing:
   - Keep it on a second monitor
   - Or resize it to fit in a corner of your screen
4. **Play normally** and watch the radar for directional cues

## Calibration

To get the best detection accuracy, use the calibration tool:

### Running Calibration

```bash
cd audio_radar_v10\audio_radar
python calibrate.py
```

### Calibration Process

1. **Start calibration** with the command above
2. **Play your game** for 1-2 minutes:
   - Walk around (to generate footsteps)
   - Fire weapons (to generate gunshots)
   - Include ambient sounds and music
3. **Watch the statistics** displayed in real-time
4. **Press Ctrl+C** when you've captured enough variety
5. **Review recommendations** - the tool will suggest optimal thresholds
6. **Apply settings** by answering 'y' when prompted

### What the Statistics Mean

- **Peak Amplitude**: Maximum audio level (used for gunshot detection)
- **RMS Level**: Average audio power
- **Standard Deviation**: Audio variation (used for footstep detection)

Higher values indicate louder or more varied audio.

## Advanced Configuration

### Configuration File Structure

Edit `audio_radar_v10\audio_radar\config.json`:

```json
{
  "input_device": null,
  "audio": {
    "samplerate": 48000,
    "blocksize": 1024,
    "channels": 2
  },
  "detection": {
    "shot_peak_threshold": 0.6,
    "footstep_std_threshold": 0.05,
    "enable_bandpass_filter": true,
    "footstep_freq_range": [2000, 8000],
    "shot_freq_range": [200, 12000]
  },
  "visualization": {
    "fade_duration": 0.5,
    "show_distance_indicator": true,
    "footstep_color": [0, 255, 0],
    "shot_color": [255, 0, 0]
  },
  "bar_width": 40,
  "bar_height": 200,
  "transparency": 180
}
```

### Tuning for Your Game

Different games have different audio characteristics. Here are game-specific tips:

#### For Tactical Shooters (CS:GO, Valorant, Rainbow Six)
```json
{
  "detection": {
    "shot_peak_threshold": 0.65,
    "footstep_std_threshold": 0.04,
    "enable_bandpass_filter": true,
    "footstep_freq_range": [2500, 7000]
  }
}
```

#### For Battle Royale (Fortnite, PUBG, Apex)
```json
{
  "detection": {
    "shot_peak_threshold": 0.55,
    "footstep_std_threshold": 0.06,
    "enable_bandpass_filter": true,
    "footstep_freq_range": [2000, 8000]
  }
}
```

#### For Horror Games (Quiet atmosphere)
```json
{
  "detection": {
    "shot_peak_threshold": 0.5,
    "footstep_std_threshold": 0.03,
    "enable_bandpass_filter": true
  }
}
```

### Multi-Channel Audio Setup

For best directional accuracy with 5.1 or 7.1 surround:

1. **Configure Windows audio**:
   - Set output device to 5.1 or 7.1 mode
   - Ensure game outputs multi-channel audio

2. **Update config.json**:
```json
{
  "audio": {
    "channels": 6  // 6 for 5.1, 8 for 7.1
  }
}
```

3. **Verify channel mapping**:
   - Front Left/Right = 30°/-30°
   - Center = 0°
   - Rear Left/Right = 150°/-150°
   - Side Left/Right (7.1) = 90°/-90°

## Tips and Tricks

### Reducing False Positives

If the radar lights up too often:

1. **Increase thresholds**:
   ```json
   {
     "shot_peak_threshold": 0.7,
     "footstep_std_threshold": 0.08
   }
   ```

2. **Enable filtering**:
   ```json
   {
     "enable_bandpass_filter": true
   }
   ```

3. **Adjust frequency ranges** to match your game's audio profile

### Catching Quiet Sounds

If you're missing footsteps:

1. **Lower thresholds**:
   ```json
   {
     "footstep_std_threshold": 0.03
   }
   ```

2. **Increase game volume** or enable in-game audio boost

3. **Use compression** (future feature)

### Optimizing Performance

If Audio Radar uses too much CPU:

1. **Increase block size**:
   ```json
   {
     "audio": {
       "blocksize": 2048  // or 4096
     }
   }
   ```

2. **Disable filtering**:
   ```json
   {
     "detection": {
       "enable_bandpass_filter": false
     }
   }
   ```

### Visual Customization

Customize colors for better visibility:

```json
{
  "visualization": {
    "footstep_color": [0, 255, 255],     // Cyan
    "shot_color": [255, 128, 0],         // Orange
    "fade_duration": 0.8                  // Longer fade
  }
}
```

## Troubleshooting

### Common Issues

#### Radar shows nothing
- Check that loopback device is enabled and set as default
- Verify game audio is playing
- Run calibration to check if audio is being received
- Lower detection thresholds

#### Too many false positives
- Increase detection thresholds
- Enable bandpass filtering
- Run calibration to find optimal values

#### Wrong directions
- Ensure game is outputting positional audio
- Try multi-channel audio (5.1/7.1) instead of stereo
- Verify loopback captures all channels

#### Performance issues
- Increase audio blocksize
- Disable bandpass filtering
- Close other audio applications
- Update audio drivers

### Debug Mode

To enable detailed logging:

1. Check the log file: `audio_radar_v10\audio_radar\log_v10.txt`
2. Look for error messages or warnings
3. Include log contents when reporting issues

## FAQ

**Q: Does Audio Radar work with headphones?**  
A: Yes! It works with any audio output (headphones, speakers, etc.). The loopback captures the audio before it reaches your audio device.

**Q: Can I use this with voice chat?**  
A: Audio Radar only processes game audio from the loopback device. Voice chat on a separate device won't interfere.

**Q: Is this considered cheating?**  
A: Audio Radar is an accessibility tool that visualizes existing game audio. It doesn't access game memory or provide information not already available through sound. However, check your game's terms of service.

**Q: Why stereo instead of multi-channel?**  
A: Many games output stereo by default. For best directional accuracy, configure your game to output 5.1 or 7.1 surround sound.

**Q: Can I run this on a second PC?**  
A: Not currently. Audio Radar needs to run on the same PC as the game to access the audio loopback.

**Q: Does it work with all games?**  
A: Audio Radar works with any game that outputs audio through Windows. Detection accuracy depends on the game's audio design.

**Q: How much CPU does it use?**  
A: Typically 1-3% on modern CPUs. Increase blocksize if experiencing issues.

**Q: Can I contribute to the project?**  
A: Yes! See the GitHub repository for contribution guidelines.

## Need More Help?

- Check [INSTALL.md](INSTALL.md) for installation issues
- Review [README.md](README.md) for technical details
- Open an issue on GitHub
- Run calibration tool for detection problems

---

**Remember**: Audio Radar is a tool to enhance your gaming experience and improve accessibility. It works best when combined with game audio knowledge and practice!
