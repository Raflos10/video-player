from PySide6 import QtCore, QtWidgets

from main_menu_bar import MainMenuBar
from video_display import VideoDisplay
from video_controls import VideoControls
from media_controller import MediaController
from helpers import open_and_load_file, setup_shortcuts
from window.settings_window import SettingsWindow


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, settings: QtCore.QSettings):
        super().__init__()

        self.settings = settings

        self.setWindowTitle("Video Player")

        self.menu_bar = MainMenuBar()
        self.setMenuBar(self.menu_bar)

        self.videoDisplay = VideoDisplay()
        self.videoControls = VideoControls()
        self.mediaController = MediaController(self.videoDisplay)

        self.central = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(self.central)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.videoDisplay)
        self.layout.addWidget(self.videoControls)
        self.setCentralWidget(self.central)

        self.mediaController.connect_signals(self.videoControls, self.videoDisplay)
        self.videoControls.connect_signals(self.mediaController)

        file_dialog_handler = \
            lambda: open_and_load_file(self, lambda file_path: self.mediaController.load_media(file_path))
        self.videoDisplay.connect_signals(self.mediaController, self.toggle_fullscreen, file_dialog_handler)
        self.menu_bar.connect_signals(file_dialog_handler, self.toggle_fullscreen, self.open_settings)

        setup_shortcuts(self, settings)

    def update_ui_visibility(self):
        is_fullscreen = self.isFullScreen()
        self.menuBar().setVisible(not is_fullscreen)
        self.videoControls.setVisible(not is_fullscreen)

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == QtCore.QEvent.Type.WindowStateChange:
            self.update_ui_visibility()

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def open_settings(self):
        settings_dialog = SettingsWindow(self.settings, self)
        settings_dialog.exec()
        setup_shortcuts(self, self.settings)
