"""
AudioRadar v10.1 - Audio Backend Support
Provides unified interface for audio device listing and capture
"""
import sys

try:
    import sounddevice as sd
    HAS_SOUNDDEVICE = True
except ImportError:
    HAS_SOUNDDEVICE = False
    sd = None

try:
    import pyaudiowpatch as pyaudio
    HAS_PYAUDIOWPATCH = True
except ImportError:
    try:
        import pyaudio
        HAS_PYAUDIOWPATCH = True
    except ImportError:
        HAS_PYAUDIOWPATCH = False
        pyaudio = None


def list_audio_devices():
    """List available audio input devices
    
    Returns:
        List of tuples (device_index, device_name)
    """
    devices = []
    
    if HAS_SOUNDDEVICE:
        try:
            device_list = sd.query_devices()
            for i, device in enumerate(device_list):
                if device['max_input_channels'] > 0:
                    devices.append((i, device['name']))
        except Exception as e:
            print(f"Error listing sounddevice devices: {e}")
    
    elif HAS_PYAUDIOWPATCH:
        try:
            p = pyaudio.PyAudio()
            for i in range(p.get_device_count()):
                try:
                    info = p.get_device_info_by_index(i)
                    if info['maxInputChannels'] > 0:
                        devices.append((i, info['name']))
                except Exception:
                    pass
            p.terminate()
        except Exception as e:
            print(f"Error listing PyAudio devices: {e}")
    
    return devices


def get_default_input_device():
    """Get the default input device index
    
    Returns:
        int: Device index or None if not available
    """
    if HAS_SOUNDDEVICE:
        try:
            return sd.default.device[0]  # Input device
        except Exception:
            pass
    
    elif HAS_PYAUDIOWPATCH:
        try:
            p = pyaudio.PyAudio()
            info = p.get_default_input_device_info()
            idx = info['index']
            p.terminate()
            return idx
        except Exception:
            pass
    
    return None


def get_device_info(device_index):
    """Get information about a specific device
    
    Args:
        device_index: Device index to query
        
    Returns:
        dict: Device information or None if not available
    """
    if HAS_SOUNDDEVICE:
        try:
            info = sd.query_devices(device_index)
            return {
                'name': info['name'],
                'channels': info['max_input_channels'],
                'sample_rate': int(info['default_samplerate']),
                'backend': 'sounddevice'
            }
        except Exception:
            pass
    
    elif HAS_PYAUDIOWPATCH:
        try:
            p = pyaudio.PyAudio()
            info = p.get_device_info_by_index(device_index)
            result = {
                'name': info['name'],
                'channels': info['maxInputChannels'],
                'sample_rate': int(info['defaultSampleRate']),
                'backend': 'pyaudio'
            }
            p.terminate()
            return result
        except Exception:
            pass
    
    return None


def check_audio_backend():
    """Check which audio backend is available
    
    Returns:
        str: 'sounddevice', 'pyaudio', or 'none'
    """
    if HAS_SOUNDDEVICE:
        return 'sounddevice'
    elif HAS_PYAUDIOWPATCH:
        return 'pyaudio'
    else:
        return 'none'


def get_backend_info():
    """Get information about available audio backends
    
    Returns:
        dict: Backend availability and versions
    """
    info = {
        'sounddevice': HAS_SOUNDDEVICE,
        'pyaudio': HAS_PYAUDIOWPATCH,
        'active_backend': check_audio_backend()
    }
    
    if HAS_SOUNDDEVICE:
        try:
            info['sounddevice_version'] = sd.__version__
        except AttributeError:
            info['sounddevice_version'] = 'unknown'
    
    if HAS_PYAUDIOWPATCH:
        try:
            info['pyaudio_version'] = pyaudio.__version__
        except AttributeError:
            info['pyaudio_version'] = 'unknown'
    
    return info


def main():
    """Test audio backend functionality"""
    print("=" * 70)
    print("  AudioRadar - Audio Backend Test")
    print("=" * 70)
    print()
    
    # Check backends
    backend_info = get_backend_info()
    print(f"Active Backend: {backend_info['active_backend']}")
    print(f"Sounddevice Available: {backend_info['sounddevice']}")
    print(f"PyAudio Available: {backend_info['pyaudio']}")
    print()
    
    if backend_info['active_backend'] == 'none':
        print("[ERROR] No audio backend available!")
        print("Install one of:")
        print("  - pip install sounddevice")
        print("  - pip install pyaudiowpatch")
        return 1
    
    # List devices
    print("Available Input Devices:")
    print("-" * 70)
    devices = list_audio_devices()
    if not devices:
        print("  [WARN] No input devices found")
    else:
        for idx, name in devices:
            print(f"  [{idx}] {name}")
            info = get_device_info(idx)
            if info:
                print(f"       Channels: {info['channels']}, Sample Rate: {info['sample_rate']} Hz")
    print()
    
    # Default device
    default_idx = get_default_input_device()
    if default_idx is not None:
        print(f"Default Input Device: [{default_idx}]")
        info = get_device_info(default_idx)
        if info:
            print(f"  Name: {info['name']}")
    else:
        print("Default Input Device: [NONE]")
    
    print()
    print("[OK] Audio backend test complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
