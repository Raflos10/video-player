from typing import Optional

from PySide6 import QtCore

from primitive.graphics_outlined_text_item import GraphicsOutlinedTextItem
from settings.setting_keys import SettingKeys
from settings.settings_manager import settings_manager


class SubtitleGraphicsItem(GraphicsOutlinedTextItem):
    def __init__(self):
        super().__init__()

        self.setVisible(False)
        self._view_height = 600
        self.update_subtitle_style()

        self.connect_signals()

    def connect_signals(self):
        settings_manager.settings_changed.connect(self.on_settings_changed)

    def setPlainText(self, text: Optional[str]):
        super().setPlainText(text)
        self.setVisible(bool(text))

    def on_settings_changed(self, key: str):
        if key == SettingKeys.SUBTITLE_FONT_SCALE:
            self.update_subtitle_style()

    def set_view_height(self, height: int):
        if self._view_height != height:
            self._view_height = height
            self.update_subtitle_style()

    def _calculate_font_size(self) -> int:
        scale = settings_manager.value(SettingKeys.SUBTITLE_FONT_SCALE)
        calculated_size = int(self._view_height * (scale / 100.0))
        return max(12, min(calculated_size, 120))

    def update_subtitle_style(self, font_size=None):
        font = self.font()

        text_option = self.document().defaultTextOption()
        text_option.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.document().setDefaultTextOption(text_option)

        if font_size:
            font.setPointSize(font_size)
        else:
            font.setPointSize(self._calculate_font_size())

        font.setBold(True)
        self.setFont(font)

        if self.toPlainText():
            self.apply_outline_format()
