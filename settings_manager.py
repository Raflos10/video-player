from PySide6 import QtCore

from setting_keys import DEFAULTS


class SettingsManager(QtCore.QObject):
    settings_changed = QtCore.Signal(str, object)

    def __init__(self):
        super().__init__()
        self.settings = QtCore.QSettings()

    def set_value(self, key: str, value):
        old_value = self.settings.value(key)
        if old_value != value:
            self.settings.setValue(key, value)
            self.settings_changed.emit(key, value)

    def value(self, key: str):
        return self.settings.value(key, DEFAULTS[key])


# Global singleton
settings_manager = SettingsManager()
