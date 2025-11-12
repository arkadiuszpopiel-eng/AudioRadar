# Audio Radar - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Run the Build Script
```
Double-click: RUN_BUILD_ALL.cmd
```

**What it does:**
- Installs Python packages
- Tests audio modules
- Starts the application

**Wait for:** "Build Complete!" message

---

### Step 2: Configure Audio
```
1. Click "Audio" → "Select Device..."
2. Choose your input device
3. Click "Select"
```

**Tip:** Look for "Stereo Mix" or "What U Hear" for game audio

---

### Step 3: Start Detection
```
Click the green "Start" button
```

**You're done!** Events will appear on the radar.

---

## 📊 Understanding the Display

### Radar (Left Side)

```
        N (Front)
         |
    NW   |   NE
      \  |  /
   W --- ● --- E
      /  |  \
    SW   |   SE
         |
        S (Back)
```

- **● Center** = Your position
- **Green circles** = Footsteps
- **Yellow pulsing** = Running
- **Red stars** = Gunshots

### Spectrum (Bottom)

```
[====||======||||====]
 Low  Mid   High Freq
```

Shows audio frequency levels in real-time.

---

## ⚙️ Quick Settings

### Making Detection More Sensitive

```
Configuration Panel → Detection Settings
Reduce thresholds: 30% → 20%
```

### Making Radar More/Less Visible

```
Configuration Panel → Display Settings
Adjust "Radar Transparency" slider
```

### Changing Theme

```
Configuration Panel → Display Settings
Theme: Dark ↔ Light
```

---

## 🎮 Gaming Setup

### For FPS Games

1. **Enable Loopback:**
   - Windows Sound Settings
   - Recording tab
   - Enable "Stereo Mix" or "What U Hear"
   - Set as default recording device

2. **Configure Game:**
   - Set audio output to your normal device
   - Audio Radar captures via loopback

3. **Position Window:**
   - Place on second monitor OR
   - Run in windowed mode alongside game

### Recommended Settings

```
Footstep Threshold: 30%
Running Threshold: 50%
Gunshot Threshold: 70%
Decay Time: 2 seconds
Theme: Dark
```

---

## 🔧 Common Fixes

### No Events Showing

**Try:**
1. Lower detection thresholds
2. Increase system volume
3. Test device: Audio → Test Device
4. Check correct device selected

### Wrong Direction

**Try:**
1. Use 5.1 or 7.1 audio instead of stereo
2. Check Windows speaker configuration
3. Verify game audio settings

### App Won't Start

**Try:**
1. Check log.txt for errors
2. Run: `python test_structure.py`
3. Reinstall dependencies:
   ```
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

---

## 📖 Next Steps

Once you're comfortable with basics:

1. **Read Full Documentation**
   - NEW_README.md for all features
   - INSTALL.md for detailed setup

2. **Experiment with Settings**
   - Fine-tune detection thresholds
   - Try different audio configurations
   - Test with various games

3. **Advanced Features**
   - Device quality testing
   - Custom configurations
   - Profile switching (future)

---

## 🆘 Need Help?

1. Check **log.txt** for error messages
2. Read **NEW_README.md** Troubleshooting section
3. Run **test_structure.py** to verify installation
4. Check GitHub issues for similar problems

---

## 💡 Pro Tips

### Tip 1: Audio Quality
Better audio setup = better detection
- Use surround sound (5.1/7.1) for best direction accuracy
- Enable all audio enhancements in game settings
- Keep system volume at comfortable level (50-70%)

### Tip 2: Threshold Tuning
Start high, go lower:
1. Begin with high thresholds (default)
2. If missing events, lower by 5-10%
3. If too many false positives, increase by 5-10%
4. Save config when happy

### Tip 3: Performance
For best performance:
- Close unnecessary programs
- Use dark theme
- Hide spectrum if not needed
- Reduce radar size for lower-end PCs

### Tip 4: Gaming Setup
- Second monitor: Full-screen game + radar on second screen
- Single monitor: Windowed game or overlay mode (future)
- Test in-game before competitive matches

---

## 📋 Checklist

Before Gaming:
- [ ] Audio device selected
- [ ] Device tested (good signal)
- [ ] Thresholds adjusted
- [ ] Start button clicked
- [ ] Events showing on radar
- [ ] Position visible on screen

---

## 🎯 Success Criteria

**You're ready when:**
- ✅ Radar shows events from game audio
- ✅ Direction matches game events
- ✅ No excessive false positives
- ✅ Performance is smooth
- ✅ Window positioned comfortably

---

## 🌟 Enjoy!

You're now ready to use Audio Radar!

Remember:
- Practice makes perfect
- Start with single-player/training
- Adjust settings to your preference
- Have fun and stay safe!

---

**Audio Radar v1.0.0**  
For detailed help, see NEW_README.md
