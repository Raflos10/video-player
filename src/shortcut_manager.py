from typing import TYPE_CHECKING

from settings.setting_keys import SettingKeys
from settings.settings_manager import settings_manager
from utils.helpers import setup_shortcuts

if TYPE_CHECKING:
    from window.application_window import ApplicationWindow


class ShortcutManager:
    def __init__(self, window: ApplicationWindow) -> None:
        self.window = window
        setup_shortcuts(window)

    def connect_signals(self) -> None:
        settings_manager.settings_changed.connect(self.on_settings_changed)

    def on_settings_changed(self, key: str) -> None:
        if key in [
            SettingKeys.PLAY_PAUSE_SHORTCUT,
            SettingKeys.SEEK_FORWARD_SHORTCUT,
            SettingKeys.SEEK_BACKWARD_SHORTCUT,
            SettingKeys.TOGGLE_MUTE_SHORTCUT,
            SettingKeys.FULLSCREEN_SHORTCUT,
            SettingKeys.TOGGLE_SUBTITLES_SHORTCUT,
        ]:
            setup_shortcuts(self.window)
