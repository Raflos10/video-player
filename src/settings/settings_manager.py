from PySide6 import QtCore

from settings.setting_keys import DEFAULTS


class SettingsManager(QtCore.QObject):
    settings_changed = QtCore.Signal(str, object)

    def __init__(self) -> None:
        super().__init__()
        self.settings = QtCore.QSettings("VideoPlayer", "VideoPlayer")

    def set_value(self, key: str, value: object) -> None:
        current_value = self._get_value(key)
        if current_value != value:
            self.settings.setValue(key, value)
            self.settings_changed.emit(key, value)

    def _get_value(self, key: str) -> object:
        default_value = DEFAULTS[key]
        return self.settings.value(key, default_value, type=type(default_value))

    def get_float(self, key: str) -> float:
        value = self._get_value(key)
        if not isinstance(value, float):
            msg = f"Expected float for '{key}'"
            raise TypeError(msg)
        return value

    def get_bool(self, key: str) -> bool:
        value = self._get_value(key)
        if not isinstance(value, bool):
            msg = f"Expected bool for '{key}'"
            raise TypeError(msg)
        return value

    def get_str(self, key: str) -> str:
        value = self._get_value(key)
        if not isinstance(value, str):
            msg = f"Expected str for '{key}'"
            raise TypeError(msg)
        return value

    def get_int(self, key: str) -> int:
        value = self._get_value(key)
        if not isinstance(value, int):
            msg = f"Expected int for '{key}'"
            raise TypeError(msg)
        return value


# Global singleton
settings_manager = SettingsManager()
