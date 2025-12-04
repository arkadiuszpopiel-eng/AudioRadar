# RadarSuite Changelog

## v4.1.0-Refactored (2025-11-22)

### Added
- Thread-safe `TargetTracker` with `threading.Lock` protection
- `_find_matching_target_unlocked()` and `_get_active_targets_unlocked()` internal methods
- History copy in target export to prevent concurrent modification
- RMS-based power calculation for more stable detection

### Changed
- Detection algorithm: switched from `max()` to RMS-based band energy calculation
- Frequency bands optimized:
  - Walk: 40-250 Hz (was 20-200)
  - Run: 200-1200 Hz (was 200-1500)
  - Shot: 1500-8000 Hz (was 1500-6000)
- Detection thresholds lowered for better sensitivity:
  - Walk: 0.03 (was 0.04)
  - Run: 0.025 (was 0.03)
  - Shot: 0.05 (was 0.06)

### Fixed
- **CRITICAL**: Duplicate `toggle_start_stop` function renamed to `toggle_start_stop_shortcut`
- **CRITICAL**: `setup_shortcuts` using wrong `self.tabs` instead of `self.main_tabs`
- Thread safety in `TargetTracker.update()`, `get_active_targets()`, `clear()`
- Race condition in target history access

### Removed
- Dead code in main.py (duplicate function)

---

## v3.5.3 (Previous)

### Fixed
- Language switching EN/PL with `get_language()` function
- Engine detection with game-to-engine mapping
- `MilitaryHUDRadar.update_sweep` and `update_target` methods
- Game detector connection to DevicePanel
- Audio status "Not initialized" display
- Detection from `mean()` to `max()` for frequency band power
- Detection thresholds lowered
- `sp_signal` not defined in classifier.py
- `add_target` TypeError - parameter order
- `re` not defined in launcher.py
- Numpy array truth value ambiguity
- COM initialization error 0x800401f0
- Speaker.recorder() doesn't exist error
- numpy.fromstring deprecation (pyaudiowpatch fallback)

---

## Test Cases for v4.1.0

### Unit Tests

1. **Detection Algorithm Tests**
   - Test walk detection with 100Hz tone at various amplitudes
   - Test run detection with 500Hz tone at various amplitudes
   - Test shot detection with 3000Hz tone at various amplitudes
   - Test detection with white noise (should not trigger false positives)
   - Test detection with silence (all detections should be false)

2. **Thread Safety Tests**
   - Test concurrent access to `TargetTracker.update()` from multiple threads
   - Test `get_active_targets()` during `update()` call
   - Test `clear()` during `update()` call

3. **Edge Case Tests**
   - Empty audio block (len=0)
   - Single sample audio block
   - Mono vs stereo block handling
   - Very loud signal (clipping)
   - Very quiet signal (near silence)

4. **UI Tests**
   - Keyboard shortcuts (Ctrl+1,2,3,4) switch tabs correctly
   - Ctrl+S toggles start/stop with toast notification
   - Detection labels update correctly (WALK/RUN/SHOT)
   - Hold timer decays correctly (3 frames)

5. **Integration Tests**
   - Full audio pipeline: engine -> cache -> detection -> radar
   - Target tracking: create, update, decay, remove
   - Loopback audio capture (Windows with pyaudiowpatch)

### Manual Test Procedures

1. **Test Mode Verification**
   - Enable test mode
   - Verify radar shows targets
   - Verify detection panel shows WALK/RUN/SHOT
   - Verify 3D radar updates

2. **Game Audio Capture**
   - Start game (ARC Raiders)
   - Enable loopback mode
   - Walk in-game, verify WALK detection
   - Run in-game, verify RUN detection
   - Fire weapon, verify SHOT detection

3. **Performance Test**
   - Run for 30 minutes continuous
   - Monitor memory usage (should be stable)
   - Monitor CPU usage (should be <10% idle)
   - Check for thread pool cleanup (futures cleaned)
