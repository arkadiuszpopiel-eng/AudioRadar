"""Main entry point for the Audio Radar program.

This script wires together the audio capture, sound analysis and visualisation
modules. It reads configuration from ``config.json`` if present and writes
to ``log.txt`` to record important runtime events. When run on a system with
the appropriate dependencies installed (numpy, sounddevice and pygame) it
captures audio from the specified input device, analyses the stream to
determine whether footsteps or gunshots have occurred and then lights up
visual indicators on the screen accordingly.

Configuration
-------------
The configuration file is a JSON object with the following keys:

``input_device``
    Index of the audio input device to use. If ``null`` (or not present) the
    system default input device will be used. You can find available devices
    by running ``python main.py --list-devices`` on a system with
    ``sounddevice`` installed.

``output_device``
    Index of the audio output device. This setting is currently unused by
    this script but is provided for completeness should you wish to route
    audio to a specific output device. Leave as ``null`` to use the system
    default.

``bar_width``
    Width in pixels of each direction bar in the visualisation. Larger
    values result in thicker bars. The program enforces sensible limits
    internally to avoid overlapping bars.

``bar_height``
    Height in pixels of each direction bar in the visualisation. Bars extend
    from the centre of the window outwards, so increasing the height will
    cause them to reach further towards the screen edges.

``transparency``
    An integer between 0 and 255 controlling the opacity of the bars when
    activated. Lower values make the bars more transparent. Bars are not
    drawn when no sound event has been detected.

Usage
-----
On a Windows system with a Sound Blaster Z SE card you should first
configure the card to expose a loopback (e.g. "Stereo Mix" or
"What U Hear") and set that as the default recording device. Once
dependencies are installed (see ``RUN_BUILD_ALL.cmd``) you can run this
script directly with:

    python main.py

To list available input and output devices run:

    python main.py --list-devices

This will print a numbered list of devices which you can then copy into
``config.json``. Changes to the configuration are detected on restart.
"""

import argparse
import json
import logging
import threading
from pathlib import Path

try:
    import sounddevice as sd
except ImportError:
    sd = None  # sounddevice is not available in this environment

try:
    import numpy as np
except ImportError:
    np = None

# Make sibling modules importable both when running as part of the audio_radar
# package (e.g. ``python -m audio_radar.main``) and when executing this file
# directly as a script (``python main.py``). When run as a script the
# ``audio_radar`` package name will not be in ``sys.modules``, so importing
# submodules via ``audio_radar.*`` will fail. To handle both cases we
# conditionally import from ``audio_radar`` and fall back to importing from
# the current directory after adding it to ``sys.path``.
import os
import sys
sys.path.append(os.path.dirname(__file__))
try:
    # Attempt to import via the package name when running as module
    from audio_radar.audio_capture import list_audio_input_devices, list_audio_output_devices, AudioStream
    from audio_radar.sound_analysis import detect_event
    from audio_radar.visualization import Visualizer
except ImportError:
    # Fallback to local imports when running as a script
    from audio_capture import list_audio_input_devices, list_audio_output_devices, AudioStream  # type: ignore
    from sound_analysis import detect_event  # type: ignore
    from visualization import Visualizer  # type: ignore


CONFIG_FILE = Path(__file__).parent / "config.json"
# Define the version of this Audio Radar release. Update this string
# whenever you package a new version so that logs and archive names
# clearly reflect the version in use.
VERSION = "v10"

# Log file name includes the version number to avoid confusion between
# releases. For example, version ``v9`` will log to ``log_v9.txt`` in
# the ``audio_radar`` directory. When releasing a new version you
# should update ``VERSION`` above and the log will automatically
# follow the new naming.
LOG_FILE = Path(__file__).parent / f"log_{VERSION}.txt"


def load_config() -> dict:
    """Load configuration from CONFIG_FILE.

    Returns a dictionary with defaults applied when keys are missing. If
    the file does not exist an empty configuration is returned.
    """
    defaults = {
        "input_device": None,
        "output_device": None,
        "bar_width": 40,
        "bar_height": 200,
        "transparency": 180,
    }
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                user_cfg = json.load(f)
            defaults.update({k: user_cfg.get(k, v) for k, v in defaults.items()})
        except Exception as exc:
            logging.error("Failed to load configuration: %s", exc)
    return defaults


def save_config(cfg: dict) -> None:
    """Save configuration to CONFIG_FILE."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
    except Exception as exc:
        logging.error("Failed to save configuration: %s", exc)


def list_devices() -> None:
    """Print available audio input and output devices."""
    if sd is None:
        print("sounddevice library not available; cannot list devices.")
        return
    print("Audio input devices:")
    for idx, name in list_audio_input_devices():
        print(f"  {idx}: {name}")
    print("\nAudio output devices:")
    for idx, name in list_audio_output_devices():
        print(f"  {idx}: {name}")


def run(cfg: dict) -> None:
    """Run the audio processing and visualisation loop.

    The function creates an ``AudioStream`` using the selected input
    device, then passes audio chunks to ``detect_event`` and forwards
    notifications to the ``Visualizer``. A separate thread is used for
    capturing audio so that the Pygame loop remains responsive.
    """
    # Configure logging to append to the versioned log file. When releasing
    # a new version you should update ``VERSION`` at the top of this file.
    logging.basicConfig(
        filename=str(LOG_FILE),
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    # Record the version in the log before any other messages.
    logging.info("Audio Radar version %s starting", VERSION)
    logging.info("Using configuration: %s", cfg)
    try:
        # Inform the user where logs are written, including the version.
        print(f"[AudioRadar {VERSION}] Logging to {LOG_FILE.resolve()}")
    except Exception:
        # In rare cases resolve() may fail if path does not exist yet
        print(f"[AudioRadar {VERSION}] Logging to {LOG_FILE}")

    # Create visualisation
    vis = Visualizer(
        bar_width=int(cfg.get("bar_width", 40)),
        bar_height=int(cfg.get("bar_height", 200)),
        transparency=int(cfg.get("transparency", 180)),
    )

    # Instantiate audio stream
    if sd is None or np is None:
        logging.error("Required libraries not available: sounddevice=%s, numpy=%s", sd, np)
        print("Required libraries are missing. Please install dependencies before running.")
        return

    input_device = cfg.get("input_device")
    stream = AudioStream(input_device=input_device, samplerate=44100, blocksize=1024)

    # Define callback to handle audio blocks
    def on_audio_data(samples):
        event = detect_event(samples)
        if event:
            logging.info("Detected event: %s", event)
            vis.trigger_event(event)

    stream.on_data = on_audio_data

    # Start audio stream in a background thread
    def audio_thread():
        try:
            stream.start()
        except Exception as exc:
            logging.error("Audio stream error: %s", exc)
            print(f"Audio stream error: {exc}")
    t = threading.Thread(target=audio_thread, daemon=True)
    t.start()

    # Run visualisation (blocking until window closed)
    try:
        vis.run()
    finally:
        stream.stop()
        logging.info("Audio Radar stopped.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audio Radar")
    parser.add_argument(
        "--list-devices",
        action="store_true",
        help="list available audio input/output devices and exit",
    )
    args = parser.parse_args()
    if args.list_devices:
        list_devices()
        return

    cfg = load_config()
    run(cfg)


if __name__ == "__main__":
    main()