from utils.helpers import setup_shortcuts
from settings.setting_keys import SettingKeys
from settings.settings_manager import settings_manager


class ShortcutManager:
    def __init__(self, window):
        self.window = window
        setup_shortcuts(window)

    def connect_signals(self):
        settings_manager.settings_changed.connect(self.on_settings_changed)

    def on_settings_changed(self, key: str):
        if key in [
            SettingKeys.PLAY_PAUSE_SHORTCUT,
            SettingKeys.SEEK_FORWARD_SHORTCUT,
            SettingKeys.SEEK_BACKWARD_SHORTCUT,
            SettingKeys.FULLSCREEN_SHORTCUT,
        ]:
            setup_shortcuts(self.window)
