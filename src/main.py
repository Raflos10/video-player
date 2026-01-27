import sys
from PySide6 import QtWidgets

from window.application_window import ApplicationWindow
from utils.audio_check import check_audio_with_prompt
from theme import Theme

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyleSheet(Theme.DARK)

    if not check_audio_with_prompt():
        sys.exit(1)

    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    mainWindow = ApplicationWindow(file_path)
    mainWindow.resize(1280, 720)
    mainWindow.show()

    sys.exit(app.exec())
