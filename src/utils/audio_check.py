"""
Audio device detection and system check for PySide6 multimedia.
"""
import sys
import platform
from PySide6 import QtMultimedia


def check_audio_devices():
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
            with open("/etc/os-release") as f:
                os_info = f.read()
                is_arch = "arch" in os_info.lower() or "manjaro" in os_info.lower()
        except:
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


def check_audio_with_prompt():
    """
    Check audio and prompt user if there's an issue.
    Returns True if should continue, False if should exit.
    """
    has_audio, warning = check_audio_devices()

    if not has_audio and warning:
        print(warning, file=sys.stderr)
        try:
            input()
            return True
        except KeyboardInterrupt:
            print("\nExiting...")
            return False

    return True
