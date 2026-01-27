from PySide6 import QtCore, QtWidgets

from widgets.main_layout import MainLayout
from widgets.main_menu_bar import MainMenuBar
from widgets.video_display import VideoDisplay
from widgets.video_controls import VideoControls
from media_controller import MediaController
from utils.helpers import open_and_load_file
from shortcut_manager import ShortcutManager
from window.settings_window import SettingsWindow
from window.about_window import AboutDialog


class ApplicationWindow(QtWidgets.QMainWindow):
    fullscreen_toggled = QtCore.Signal(bool)

    def __init__(self, file_path=None):
        super().__init__()

        self.setWindowTitle("Video Player")

        self.menu_bar = MainMenuBar(self.isFullScreen())
        self.setMenuBar(self.menu_bar)

        self.video_display = VideoDisplay()
        self.video_controls = VideoControls()

        self.main_layout = MainLayout(self, self.video_display, self.video_controls, self.isFullScreen())
        self.setCentralWidget(self.main_layout)

        self.mediaController = MediaController(self.video_display.video_item)

        self.settings_window = SettingsWindow(self)
        self.about_dialog = AboutDialog(self)

        self.shortcut_manager = ShortcutManager(self)

        self.connect_signals()

        if file_path:
            self.mediaController.load_media(file_path)

    def connect_signals(self):
        self.shortcut_manager.connect_signals()
        self.mediaController.connect_signals(self.video_controls, self.video_display)
        self.video_controls.connect_signals(self.mediaController)

        file_dialog_handler = lambda: open_and_load_file(
            self, lambda file_path: self.mediaController.load_media(file_path)
        )
        self.video_display.connect_signals(
            self.mediaController, self.toggle_fullscreen, file_dialog_handler
        )
        self.menu_bar.connect_signals(
            file_dialog_handler,
            self.toggle_fullscreen,
            self.open_settings,
            self.about_dialog.exec,
            self.fullscreen_toggled
        )
        self.main_layout.connect_signals(self.fullscreen_toggled)

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == QtCore.QEvent.Type.WindowStateChange:
            self.fullscreen_toggled.emit(self.isFullScreen())

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def open_settings(self):
        self.settings_window.refresh_ui()
        self.settings_window.exec()
