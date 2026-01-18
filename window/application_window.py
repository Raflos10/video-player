from PySide6 import QtCore, QtWidgets

from main_menu_bar import MainMenuBar
from video_display import VideoDisplay
from video_controls import VideoControls
from media_controller import MediaController
from helpers import open_and_load_file
from shortcut_manager import ShortcutManager
from window.settings_window import SettingsWindow
from window.about_window import AboutDialog


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, file_path=None):
        super().__init__()

        self.setWindowTitle("Video Player")

        self.menu_bar = MainMenuBar()
        self.setMenuBar(self.menu_bar)

        self.videoDisplay = VideoDisplay()
        self.videoControls = VideoControls()
        self.mediaController = MediaController(self.videoDisplay.video_item)

        self.settings_window = SettingsWindow(self)

        self.about_dialog = AboutDialog(self)

        self.central = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout(self.central)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.videoDisplay)
        self.main_layout.addWidget(self.videoControls)
        self.setCentralWidget(self.central)

        self.shortcut_manager = ShortcutManager(self)

        self.connect_signals()

        if file_path:
            self.mediaController.load_media(file_path)

    def connect_signals(self):
        self.shortcut_manager.connect_signals()
        self.mediaController.connect_signals(self.videoControls, self.videoDisplay)
        self.videoControls.connect_signals(self.mediaController)

        file_dialog_handler = lambda: open_and_load_file(
            self, lambda file_path: self.mediaController.load_media(file_path)
        )
        self.videoDisplay.connect_signals(
            self.mediaController, self.toggle_fullscreen, file_dialog_handler
        )
        self.menu_bar.connect_signals(
            file_dialog_handler,
            self.toggle_fullscreen,
            self.open_settings,
            self.about_dialog.exec,
        )

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
        self.settings_window.refresh_ui()
        self.settings_window.exec()
