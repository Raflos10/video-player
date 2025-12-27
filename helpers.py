import os
from PySide6 import QtWidgets


def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}:{secs:02d}"


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
