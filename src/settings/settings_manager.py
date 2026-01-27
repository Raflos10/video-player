from PySide6 import QtCore

from settings.setting_keys import DEFAULTS


class SettingsManager(QtCore.QObject):
    settings_changed = QtCore.Signal(str, object)

    def __init__(self):
        super().__init__()
        self.settings = QtCore.QSettings("VideoPlayer", "VideoPlayer")

    def set_value(self, key: str, value):
        current_value = self.value(key)
        if current_value != value:
            self.settings.setValue(key, value)
            self.settings_changed.emit(key, value)

    def value(self, key: str):
        default_value = DEFAULTS[key]
        return self.settings.value(key, DEFAULTS[key], type=type(default_value))


# Global singleton
settings_manager = SettingsManager()
