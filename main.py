import sys
from PySide6 import QtWidgets, QtCore

from window.application_window import ApplicationWindow
from audio_check import check_audio_with_prompt
from theme import Theme

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setOrganizationName("VideoPlayer")
    app.setApplicationName("VideoPlayer")
    app.setStyleSheet(Theme.DARK)

    if not check_audio_with_prompt():
        sys.exit(1)

    settings = QtCore.QSettings()
    mainWindow = ApplicationWindow(settings)
    mainWindow.resize(1280, 720)
    mainWindow.show()

    sys.exit(app.exec())
