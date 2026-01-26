import os
from typing import cast

from PySide6 import QtWidgets, QtGui

from setting_keys import SettingKeys
from settings_manager import settings_manager


def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}:{secs:02d}"


def setup_shortcuts(window):
    if hasattr(window, "shortcuts"):
        for s in window.shortcuts:
            s.deleteLater()
    window.shortcuts = []

    play_pause_key = settings_manager.value(SettingKeys.PLAY_PAUSE_SHORTCUT)
    seek_forward_key = settings_manager.value(SettingKeys.SEEK_FORWARD_SHORTCUT)
    seek_backward_key = settings_manager.value(SettingKeys.SEEK_BACKWARD_SHORTCUT)
    fullscreen_key = settings_manager.value(SettingKeys.FULLSCREEN_SHORTCUT)
    seek_step = int(cast(int, settings_manager.value(SettingKeys.SEEK_STEP)))

    play_pause_shortcut: QtGui.QShortcut = QtGui.QShortcut(QtGui.QKeySequence.fromString(str(play_pause_key)), window)
    play_pause_shortcut.activated.connect(window.mediaController.toggle_playback)
    window.shortcuts.append(play_pause_shortcut)

    seek_forward_shortcut: QtGui.QShortcut = QtGui.QShortcut(QtGui.QKeySequence.fromString(str(seek_forward_key)),
                                                             window)
    seek_forward_shortcut.activated.connect(lambda: window.mediaController.mediaPlayer.setPosition(
        window.mediaController.mediaPlayer.position() + seek_step * 1000))
    window.shortcuts.append(seek_forward_shortcut)

    seek_backward_shortcut: QtGui.QShortcut = QtGui.QShortcut(QtGui.QKeySequence.fromString(str(seek_backward_key)),
                                                              window)
    seek_backward_shortcut.activated.connect(lambda: window.mediaController.mediaPlayer.setPosition(
        window.mediaController.mediaPlayer.position() - seek_step * 1000))
    window.shortcuts.append(seek_backward_shortcut)

    fullscreen_shortcut: QtGui.QShortcut = QtGui.QShortcut(QtGui.QKeySequence.fromString(str(fullscreen_key)), window)
    fullscreen_shortcut.activated.connect(window.toggle_fullscreen)
    window.shortcuts.append(fullscreen_shortcut)


def open_and_load_file(parent, load_media):
    videos_dir = os.path.join(os.path.expanduser("~"), "Videos")
    if os.path.exists(videos_dir):
        default_dir = videos_dir
    else:
        home_dir = os.path.expanduser("~")
        if os.path.exists(home_dir):
            default_dir = home_dir
        else:
            default_dir = os.getcwd()

    file_dialog = QtWidgets.QFileDialog(parent)
    file_path, _ = file_dialog.getOpenFileName(parent, "Select Video File", default_dir,
                                               "Video files (*.mp4 *.mkv *.avi *.webm *.mov);;All files (*)")
    if file_path:
        load_media(file_path)
