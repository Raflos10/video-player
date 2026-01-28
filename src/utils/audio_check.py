"""
Audio device detection and system check for PySide6 multimedia.
"""

import logging
import platform
from pathlib import Path

from PySide6 import QtMultimedia

logger = logging.getLogger(__name__)


def check_audio_devices() -> tuple[bool, str | None]:
    """
    Check if audio devices are detected by Qt.
    Returns (has_audio, warning_message)
    """
    devices = QtMultimedia.QMediaDevices.audioOutputs()
    has_audio = len(devices) > 0

    if has_audio:
        return True, None

    # No audio devices detected - provide helpful error message
    system = platform.system()

    if system == "Linux":
        # Check if we're on Arch-based system
        try:
            os_info = Path("/etc/os-release").read_text()
            is_arch = "arch" in os_info.lower() or "manjaro" in os_info.lower()
        except OSError:
            is_arch = False

        if is_arch:
            warning = """
╔════════════════════════════════════════════════════════════════╗
║                    AUDIO DEVICE WARNING                        ║
╚════════════════════════════════════════════════════════════════╝

No audio devices detected by PySide6.

This is a known issue with pip-installed PySide6 on Arch Linux.
Video will play but WITHOUT AUDIO.

SOLUTION:
1. Install system PySide6:
   sudo pacman -S pyside6

2. Recreate your venv with system packages:
   python -m venv --system-site-packages venv
   source venv/bin/activate
   pip install -r requirements.txt

OR run with system Python:
   /usr/bin/python3 main.py

Press Enter to continue without audio, or Ctrl+C to exit...
"""
        else:
            warning = """
╔════════════════════════════════════════════════════════════════╗
║                    AUDIO DEVICE WARNING                        ║
╚════════════════════════════════════════════════════════════════╝

No audio devices detected by PySide6.
Video will play but WITHOUT AUDIO.

Possible causes:
- Missing Qt6 multimedia plugins
- Audio system not running (PulseAudio/PipeWire)
- PySide6 cannot access audio devices

Press Enter to continue without audio, or Ctrl+C to exit...
"""
    else:
        warning = """
╔════════════════════════════════════════════════════════════════╗
║                    AUDIO DEVICE WARNING                        ║
╚════════════════════════════════════════════════════════════════╝

No audio devices detected by PySide6.
Video will play but WITHOUT AUDIO.

Press Enter to continue without audio, or Ctrl+C to exit...
"""

    return False, warning


def check_audio_with_prompt() -> bool:
    """
    Check audio and prompt user if there's an issue.
    Returns True if it should continue, False if it should exit.
    """
    has_audio, warning = check_audio_devices()

    if not has_audio and warning:
        logger.warning(warning)
        try:
            input()
        except KeyboardInterrupt:
            logger.info("Exiting...")
            return False
        else:
            return True

    return True
