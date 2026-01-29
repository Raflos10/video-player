from collections.abc import Callable

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QWidget

from settings.setting_keys import SettingKeys
from settings.settings_manager import settings_manager


class MainMenuBar(QtWidgets.QMenuBar):
    def __init__(self, is_fullscreen: bool, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.is_fullscreen = is_fullscreen

        file_menu = self.addMenu("File")
        view_menu = self.addMenu("View")
        subtitles_menu = self.addMenu("Subtitles")
        options_menu = self.addMenu("Options")
        help_menu = self.addMenu("Help")

        self.open_action = file_menu.addAction("Open File")
        self.open_action.setShortcut(QtGui.QKeySequence.StandardKey.Open)
        exit_action = file_menu.addAction("Exit")
        exit_action.setShortcut(QtGui.QKeySequence.StandardKey.Quit)

        self.fullscreen_action = view_menu.addAction("Fullscreen")
        self.fullscreen_action.setCheckable(True)

        self.toggle_subtitles_action = subtitles_menu.addAction("Toggle Subtitles")
        self.toggle_subtitles_action.setCheckable(True)
        self.refresh_ui()

        self.settings_action = options_menu.addAction("Settings")
        self.about_action = help_menu.addAction("About")

        exit_action.triggered.connect(QtWidgets.QApplication.quit)

    def connect_signals(
        self,
        file_dialog_handler: Callable,
        toggle_fullscreen_handler: Callable,
        settings_handler: Callable,
        about_handler: Callable,
        fullscreen_toggled: QtCore.Signal(bool),
    ) -> None:
        settings_manager.settings_changed.connect(self.on_settings_changed)

        self.open_action.triggered.connect(file_dialog_handler)
        self.fullscreen_action.triggered.connect(toggle_fullscreen_handler)
        self.toggle_subtitles_action.triggered.connect(self._toggle_subtitles)
        self.settings_action.triggered.connect(settings_handler)
        self.about_action.triggered.connect(about_handler)
        fullscreen_toggled.connect(self.on_fullscreen_toggle)

    def _toggle_subtitles(self) -> None:
        current = settings_manager.get_bool(SettingKeys.ENABLE_SUBTITLES)
        new_value = not current
        settings_manager.set_value(SettingKeys.ENABLE_SUBTITLES, new_value)
        self.toggle_subtitles_action.setChecked(new_value)

    # TODO: consolidate these bottom two functions
    def on_settings_changed(self, key: str, value: bool) -> None:
        if key == SettingKeys.ENABLE_SUBTITLES:
            self.toggle_subtitles_action.setChecked(value)

    def refresh_ui(self) -> None:
        enable_subtitles = settings_manager.get_bool(SettingKeys.ENABLE_SUBTITLES)
        self.toggle_subtitles_action.setChecked(enable_subtitles)

    def on_fullscreen_toggle(self, is_fullscreen: bool) -> None:
        self.is_fullscreen = is_fullscreen
        self.setVisible(not is_fullscreen)
