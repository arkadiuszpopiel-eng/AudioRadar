"""Entry point for running the Audio Radar package as a module.

This file allows you to start the application by running

    python -m audio_radar

from the root of the unpacked archive. It simply imports and
executes the ``main`` function from ``audio_radar.main``. See
``README.md`` for more details.
"""

from .main import main


if __name__ == '__main__':
    main()